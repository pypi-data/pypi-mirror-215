from tinybird.ch import ch_flush_logs_on_all_replicas
import uuid
from urllib.parse import urlencode
import tornado
from datetime import date, datetime, timedelta
from tests.test_cli import TestCLI

from tests.utils import exec_sql, poll
from tests.views.base_test import TBApiProxyAsync
from tinybird.token_scope import scopes
from tinybird.user import Users, public
from tinybird.ch import HTTPClient
import json


class TestProcessedUsageMetrics(TestCLI):

    def setUp(self):
        super(TestProcessedUsageMetrics, self).setUp()
        self.tb_api_proxy_async = TBApiProxyAsync(self)
        self.public_user = public.get_public_user()
        self.processed_usage_log = self.public_user.get_datasource('distributed_processed_usage_log')
        self.billing_processed_usage_log = self.public_user.get_datasource('distributed_billing_processed_usage_log')
        self.bi_connector_log = self.public_user.get_datasource('distributed_bi_connector_log')
        self.bi_connector_stats = self.public_user.get_datasource('distributed_bi_connector_stats')

    def poll_usage_logs(self, database, user_agent=None):
        self.wait_for_metrics_table_replication('processed_usage_log')
        where = f"database = '{database}'"
        if user_agent:
            where += f" AND user_agent = '{user_agent}'"
        query = f"""SELECT * FROM {self.public_user.database}.{self.processed_usage_log.id} WHERE {where} FORMAT JSON"""

        def get_usage_response():
            usage_response = exec_sql(self.public_user.database, query)
            self.assertNotEqual(len(usage_response['data']), 0, usage_response)

        poll(get_usage_response)
        return exec_sql(self.public_user.database, query)['data']

    def assert_billing_usage_logs(self, database, read_bytes, written_bytes):
        self.wait_for_metrics_table_replication('billing_processed_usage_log')
        where = f"database = '{database}'"
        query = f"""SELECT sum(read_bytes) as read_bytes, sum(written_bytes) as written_bytes FROM
                {self.public_user.database}.{self.billing_processed_usage_log.id} WHERE {where} GROUP BY database, date FORMAT JSON"""

        def get_usage_response():
            billing_usage_response = exec_sql(self.public_user.database, query)
            self.assertNotEqual(len(billing_usage_response['data']), 0, billing_usage_response)
            self.assertEqual(billing_usage_response['data'][0]['read_bytes'], read_bytes)
            self.assertEqual(billing_usage_response['data'][0]['written_bytes'], written_bytes)

        poll(get_usage_response)

    def assert_bi_connector_log(self, database, query_bi, read_rows, result_rows):
        self.wait_for_metrics_table_replication('bi_connector_log')
        query = f"""SELECT * FROM {self.public_user.database}.{self.bi_connector_log.id} where database = '{database}' FORMAT JSON"""

        def get_usage_response():
            bi_connector_log_response = exec_sql(self.public_user.database, query)
            self.assertEqual(len(bi_connector_log_response['data']), 1, bi_connector_log_response)
            self.assertEqual(bi_connector_log_response['data'][0]['database'], database, bi_connector_log_response)
            self.assertIn(query_bi, bi_connector_log_response['data'][0]['query'], bi_connector_log_response)
            self.assertEqual(bi_connector_log_response['data'][0]['read_rows'], read_rows, bi_connector_log_response)
            self.assertEqual(bi_connector_log_response['data'][0]['result_rows'], result_rows, bi_connector_log_response)

        poll(get_usage_response)

    def assert_bi_connector_stats(self, database, view_count, read_rows, result_rows):
        self.wait_for_metrics_table_replication('bi_connector_stats')
        query = f"""SELECT date,
                           database,
                           query_normalized,
                           sum(view_count) view_count,
                           sum(error_count) error_count,
                           avgMerge(avg_duration_state) avg_duration,
                           quantilesTimingMerge(0.9, 0.95, 0.99) (quantile_timing_state) quantiles,
                           sum(read_rows_sum) read_rows,
                           avgMerge(avg_result_rows_state) result_rows
                    FROM {self.public_user.database}.{self.bi_connector_stats.id}
                    where database = '{database}'
                    GROUP by database, date, query_normalized
                    FORMAT JSON"""

        def get_usage_response():
            bi_connector_stats_response = exec_sql(self.public_user.database, query)
            self.assertEqual(len(bi_connector_stats_response['data']), 1, bi_connector_stats_response)
            self.assertEqual(bi_connector_stats_response['data'][0]['database'], database)
            self.assertEqual(bi_connector_stats_response['data'][0]['view_count'], view_count)
            self.assertEqual(bi_connector_stats_response['data'][0]['read_rows'], read_rows)
            self.assertEqual(bi_connector_stats_response['data'][0]['result_rows'], result_rows)

        poll(get_usage_response)

    @tornado.testing.gen_test
    async def test_usage_after_append(self):
        workspace_name = f"ws_processed_append_{uuid.uuid4().hex}"
        email = f'{workspace_name}@example.com'
        workspace = await self.tb_api_proxy_async.register_user_and_workspace(email, workspace_name)
        token = Users.get_token_for_scope(workspace, scopes.ADMIN)
        self.workspaces_to_delete.append(workspace)

        # create datasource
        ds_name = 'test_usage_append'
        schema = "d Int32"
        await self.tb_api_proxy_async.create_datasource(token, ds_name, schema)

        # Append
        await self.tb_api_proxy_async.append_data_to_datasource_from_url(token, ds_name, 'csv',
                                                                         self.get_url_for_sql("select 1 format CSV"))

        await self.flush_system_logs_async()

        processed_usage_logs = self.poll_usage_logs(workspace.database, "tb-insert-chunk")
        self.assertEqual(len(processed_usage_logs), 1)
        read_bytes = '4'  # Since 22.6+ landing bytes are counted as read_bytes
        self.assertEqual(processed_usage_logs[0]['read_bytes'], read_bytes,
                         processed_usage_logs[0])
        self.assertEqual(processed_usage_logs[0]['written_bytes'], '4', processed_usage_logs[0])

        self.assert_billing_usage_logs(workspace.database, '0', '4')

    @tornado.testing.gen_test
    async def test_usage_after_append_with_materialization(self):
        workspace_name = f"ws_processed_append_mat_{uuid.uuid4().hex}"
        email = f'{workspace_name}@example.com'
        workspace = await self.tb_api_proxy_async.register_user_and_workspace(email, workspace_name)
        token = Users.get_token_for_scope(workspace, scopes.ADMIN)
        self.workspaces_to_delete.append(workspace)

        # create datasource
        ds_name = 'test_usage_append_mat'
        schema = "d Int32"
        await self.tb_api_proxy_async.create_datasource(token, ds_name, schema)

        # create a pipe's node with a view to that datasource
        pipe_name = 'test_mat_view'
        view_name = 'mat_view_node'
        target_ds_name = 'mat_view_node_ds'
        query = f'select d * 2 as b from {ds_name}'
        await self.tb_api_proxy_async.create_pipe_mv(workspace, token, pipe_name, view_name,
                                                     target_ds_name, query)

        # Append
        await self.tb_api_proxy_async.append_data_to_datasource_from_url(token, ds_name, 'csv',
                                                                         self.get_url_for_sql("select 1 format CSV"))

        await self.flush_system_logs_async()

        append_processed_usage_logs = self.poll_usage_logs(workspace.database, "tb-insert-chunk")
        self.assertEqual(len(append_processed_usage_logs), 1, append_processed_usage_logs)
        # Since 22.6+ landing bytes are counted as read_bytes
        read_bytes = '8'  # Since 22.6+ landing bytes are counted as read_bytes
        read_bytes_billed = '4'  # We bill for read_bytes in MVs. Landing bytes are not billed
        self.assertEqual(append_processed_usage_logs[0]['read_bytes'], read_bytes,
                         append_processed_usage_logs[0])
        self.assertEqual(append_processed_usage_logs[0]['written_bytes'], '12', append_processed_usage_logs[0])  # includes written by MV

        mat_processed_usage_logs = self.poll_usage_logs(workspace.database, "tb-materialization")

        self.assertEqual(len(mat_processed_usage_logs), 1, mat_processed_usage_logs)
        self.assertEqual(mat_processed_usage_logs[0]['read_bytes'], '4', mat_processed_usage_logs[0])
        self.assertEqual(mat_processed_usage_logs[0]['written_bytes'], '8', mat_processed_usage_logs[0])

        self.assert_billing_usage_logs(workspace.database, read_bytes_billed, '12')

    @tornado.testing.gen_test
    async def test_usage_after_pipe_endpoint_request(self):
        workspace_name = f"ws_processed_append_mat_{uuid.uuid4().hex}"
        email = f'{workspace_name}@example.com'
        workspace = await self.tb_api_proxy_async.register_user_and_workspace(email, workspace_name)
        token = Users.get_token_for_scope(workspace, scopes.ADMIN)
        self.workspaces_to_delete.append(workspace)

        # create datasaource
        ds_name = 'test_usage_for_pipe'
        schema = "d Int32"
        data = await self.tb_api_proxy_async.create_datasource(token, ds_name, schema)

        # Append
        await self.tb_api_proxy_async.append_data_to_datasource_from_url(token, ds_name, 'csv',
                                                                         self.get_url_for_sql("select 1 format CSV"))

        # Create pipe endpoint
        await self.tb_api_proxy_async.create_pipe_endpoint(workspace, token, "test_pipe", f"select * from {ds_name}")

        # Request to pipe endpoint
        params = {
            'token': token
        }
        response = await self.fetch_async(f'/v0/pipes/test_pipe.json?{urlencode(params)}')
        self.assertEqual(response.code, 200)

        await self.flush_system_logs_async()
        self.wait_for_datasource_replication(workspace, data['datasource']['id'])

        pipe_processed_usage_logs = self.poll_usage_logs(workspace.database, "tb-api-query")

        self.assertEqual(len(pipe_processed_usage_logs), 1, pipe_processed_usage_logs)
        self.assertEqual(pipe_processed_usage_logs[0]['read_bytes'], '4', pipe_processed_usage_logs[0])
        self.assertEqual(pipe_processed_usage_logs[0]['written_bytes'], '0', pipe_processed_usage_logs[0])

        self.assert_billing_usage_logs(workspace.database, '4', '4')

    @tornado.testing.gen_test
    async def test_usage_after_populate(self):
        workspace_name = f"ws_processed_populate_{uuid.uuid4().hex}"
        email = f'{workspace_name}@example.com'
        workspace = await self.tb_api_proxy_async.register_user_and_workspace(email, workspace_name)
        token = Users.get_token_for_scope(workspace, scopes.ADMIN)
        self.workspaces_to_delete.append(workspace)

        # create datasource
        ds_name = 'test_usage_populate'
        schema = "d Int32"
        await self.tb_api_proxy_async.create_datasource(token, ds_name, schema)

        # Append
        await self.tb_api_proxy_async.append_data_to_datasource_from_url(token, ds_name, 'csv',
                                                                         self.get_url_for_sql("select 1 format CSV"))

        # create a pipe's node with a view to that datasource
        pipe_name = 'test_mat_view'
        view_name = 'mat_view_node'
        target_ds_name = 'mat_view_node_ds'
        query = f'select d * 2 as b from {ds_name}'
        populate = 'true'
        pipe_node = await self.tb_api_proxy_async.create_pipe_mv(workspace, token, pipe_name, view_name,
                                                                 target_ds_name, query, populate=populate)

        job_response = pipe_node['job']
        self.assertEqual(job_response['id'], job_response['job_id'])
        job = await self.get_finalised_job_async(job_response['id'], token=token)
        self.assertEqual(job.status, 'done', job.get('error', None))
        self.assertEqual(job.kind, 'populateview')
        self.assertEqual(len(job.queries) > 0, True)
        self.assertEqual(job.queries[0]['query_id'] is not None, True, job.queries[0])
        self.assertEqual(job.queries[0]['status'], 'done', job.queries[0])

        await self.flush_system_logs_async()

        append_processed_usage_logs = self.poll_usage_logs(workspace.database, "tb-insert-chunk")
        self.assertEqual(len(append_processed_usage_logs), 1, append_processed_usage_logs)
        # Since 22.6+ landing bytes are counted as read_bytes
        read_bytes = '4'  # Since 22.6+ landing bytes are counted as read_bytes
        self.assertEqual(append_processed_usage_logs[0]['read_bytes'], read_bytes,
                         append_processed_usage_logs[0])
        self.assertEqual(append_processed_usage_logs[0]['written_bytes'], '4', append_processed_usage_logs[0])

        mat_processed_usage_logs = self.poll_usage_logs(workspace.database, "no-tb-internal-materialization")
        self.assertEqual(len(mat_processed_usage_logs), 1, mat_processed_usage_logs)
        self.assertEqual(mat_processed_usage_logs[0]['read_bytes'], '4', mat_processed_usage_logs[0])
        self.assertEqual(mat_processed_usage_logs[0]['written_bytes'], '8', mat_processed_usage_logs[0])

        # Only append is billed. populates are not billed
        self.assert_billing_usage_logs(workspace.database, '0', '4')

    @tornado.testing.gen_test
    async def test_usage_after_append_null_engine(self):
        workspace_name = f"ws_processed_append_null_{uuid.uuid4().hex}"
        email = f'{workspace_name}@example.com'
        workspace = await self.tb_api_proxy_async.register_user_and_workspace(email, workspace_name)
        token = Users.get_token_for_scope(workspace, scopes.ADMIN)
        self.workspaces_to_delete.append(workspace)

        # create datasource
        ds_name = 'test_usage_append'
        schema = "d Int32"
        await self.tb_api_proxy_async.create_datasource(token, ds_name, schema, engine_params={'engine': 'Null'})

        # Append
        await self.tb_api_proxy_async.append_data_to_datasource_from_url(token, ds_name, 'csv',
                                                                         self.get_url_for_sql("select 1 format CSV"))

        await self.flush_system_logs_async()

        processed_usage_logs = self.poll_usage_logs(workspace.database, "tb-insert-chunk")
        self.assertEqual(len(processed_usage_logs), 1)
        read_bytes = '4'  # Since 22.6+ landing bytes are counted as read_bytes
        self.assertEqual(processed_usage_logs[0]['read_bytes'], read_bytes,
                         processed_usage_logs[0])
        self.assertEqual(processed_usage_logs[0]['written_bytes'], '4', processed_usage_logs[0])

        self.assert_billing_usage_logs(workspace.database, '0', '4')

    @tornado.testing.gen_test
    async def test_usage_after_append_in_null_engine_with_materialization(self):
        workspace_name = f"ws_processed_append_null_mat_{uuid.uuid4().hex}"
        email = f'{workspace_name}@example.com'
        workspace = await self.tb_api_proxy_async.register_user_and_workspace(email, workspace_name)
        token = Users.get_token_for_scope(workspace, scopes.ADMIN)
        self.workspaces_to_delete.append(workspace)

        # create datasource
        ds_name = 'test_usage_append_null_mat'
        schema = "d Int32"
        await self.tb_api_proxy_async.create_datasource(token, ds_name, schema,
                                                        engine_params={'engine': 'Null'})

        # create a pipe's node with a view to that datasource
        pipe_name = 'test_mat_view'
        view_name = 'mat_view_node'
        target_ds_name = 'mat_view_node_ds'
        query = f'select d * 2 as b from {ds_name}'
        await self.tb_api_proxy_async.create_pipe_mv(workspace, token, pipe_name, view_name,
                                                     target_ds_name, query)

        # Append
        await self.tb_api_proxy_async.append_data_to_datasource_from_url(token, ds_name, 'csv',
                                                                         self.get_url_for_sql("select 1 format CSV"))

        await self.flush_system_logs_async()

        append_processed_usage_logs = self.poll_usage_logs(workspace.database, "tb-insert-chunk")
        self.assertEqual(len(append_processed_usage_logs), 1, append_processed_usage_logs)
        # Since 22.6+ landing bytes are counted as read_bytes
        read_bytes = '8'  # Since 22.6+ landing bytes are counted as read_bytes
        read_bytes_billed = '4'  # We bill for read_bytes in MVs. Landing bytes are not billed
        self.assertEqual(append_processed_usage_logs[0]['read_bytes'], read_bytes,
                         append_processed_usage_logs[0])
        self.assertEqual(append_processed_usage_logs[0]['written_bytes'], '12',
                         append_processed_usage_logs[0])  # includes written by MV

        mat_processed_usage_logs = self.poll_usage_logs(workspace.database, "tb-materialization")

        self.assertEqual(len(mat_processed_usage_logs), 1, mat_processed_usage_logs)
        self.assertEqual(mat_processed_usage_logs[0]['read_bytes'], '4', mat_processed_usage_logs[0])
        self.assertEqual(mat_processed_usage_logs[0]['written_bytes'], '8', mat_processed_usage_logs[0])

        self.assert_billing_usage_logs(workspace.database, read_bytes_billed, '12')

    @tornado.testing.gen_test
    async def test_usage_after_bi_connector_request(self):
        workspace_name = f"ws_processed_bi_req_{uuid.uuid4().hex}"
        email = f'{workspace_name}@example.com'
        workspace = await self.tb_api_proxy_async.register_user_and_workspace(email, workspace_name)
        token = Users.get_token_for_scope(workspace, scopes.ADMIN)
        self.workspaces_to_delete.append(workspace)

        # create datasource
        ds_name = 'test_usage_for_pipe'
        schema = "d Int32"
        ds = await self.tb_api_proxy_async.create_datasource(token, ds_name, schema)
        # Append
        await self.tb_api_proxy_async.append_data_to_datasource_from_url(token, ds_name, 'csv',
                                                                         self.get_url_for_sql("select 1 format CSV"))
        # Fake bi connector request
        client = HTTPClient(workspace.database_server, database=workspace.database)
        query_bi = f"SELECT * FROM {workspace.database}.{ds['datasource']['id']}"
        client.query_sync(query_bi, user_agent='postgres')

        await ch_flush_logs_on_all_replicas(self.public_user.database_server, self.public_user.cluster)

        self.assert_bi_connector_log(workspace.database, query_bi, '1', '1')

        self.assert_bi_connector_stats(workspace.database, '1', '1', 1)

        # The MV is configured to start ingesting data on this date
        # We need to adapt the test to not fail until then
        materialization_date = datetime(2022, 12, 1)
        read = '4' if datetime.now() >= materialization_date else '0'
        self.assert_billing_usage_logs(workspace.database, read, '4')

    @tornado.testing.gen_test
    async def test_no_billing_for_internal_datasources(self):
        await self._auth()

        for _ in range(3):
            await self._tb(["sql", "SELECT 1"])

        self.force_flush_of_span_records()
        self.wait_for_public_table_replication('pipe_stats')
        await ch_flush_logs_on_all_replicas(self.public_user.database_server, self.public_user.cluster)
        self.wait_for_metrics_table_replication('billing_processed_usage_log')

        await self._tb(["sql", "SELECT count() FROM tinybird.pipe_stats_rt"])

        self.force_flush_of_span_records()
        self.wait_for_public_table_replication('pipe_stats')
        await ch_flush_logs_on_all_replicas(self.public_user.database_server, self.public_user.cluster)
        self.wait_for_metrics_table_replication('billing_processed_usage_log')

        params = {
            'token': self.user_token,
            'stat': 'cumulative_request_along_the_month',
            'start_date': datetime(
                datetime.utcnow().year,
                datetime.utcnow().month,
                1).strftime("%Y-%m-%d %H:%M:%S"),
            'end_date': datetime(
                datetime.utcnow().year,
                datetime.utcnow().month,
                (date(datetime.utcnow().year,
                      datetime.utcnow().month + 1,
                      1) - timedelta(days=1)).day,
                23,
                59,
                59).strftime("%Y-%m-%d %H:%M:%S")
        }
        response = await self.fetch_async(
            path=f"{self.host}/v0/billing/{self.WORKSPACE_ID}/stats?{urlencode(params)}",
            method='GET')

        self.assertEqual(response.code, 200, response.body)
        requests_per_month = json.loads(response.body)['data']
        last_month = requests_per_month[len(requests_per_month) - 1]
        self.assertEqual(last_month['sql'], 3, last_month)

        params = {
            'token': self.user_token,
            'stat': 'cumulative_processed_bytes_along_the_month',
            'start_date': datetime(
                datetime.utcnow().year,
                datetime.utcnow().month,
                1).strftime("%Y-%m-%d %H:%M:%S"),
            'end_date': datetime(
                datetime.utcnow().year,
                datetime.utcnow().month,
                (date(datetime.utcnow().year,
                      datetime.utcnow().month + 1,
                      1) - timedelta(days=1)).day,
                23,
                59,
                59).strftime("%Y-%m-%d %H:%M:%S")
        }
        response = await self.fetch_async(
            path=f"{self.host}/v0/billing/{self.WORKSPACE_ID}/stats?{urlencode(params)}",
            method='GET')

        self.assertEqual(response.code, 200, response.body)
        requests_per_month = json.loads(response.body)['data']
        last_month = requests_per_month[len(requests_per_month) - 1]
        self.assertTrue(last_month['sql'] == 3, last_month)
        self.assertTrue(last_month['read_and_write'] == 0, last_month)
        self.assertTrue(last_month['total'] == 3, last_month)
