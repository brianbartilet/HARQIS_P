from Core.reporting.dashboard.data_collection.helpers.elasticsearch import *
from Core.reporting.dashboard.data_collection.models.qtest import *
from Core.utils.csv_reader import *
from Core.utils.multiprocess import *

import jsonmerge

qtest_server = RequestsQTest(**apps_config['QTest'])

INDEX_NAME_QTEST = 'qtest_issue_collection'


@multiprocess_worker()
def worker_qtest_testcases(queue, index_name):
    while True:
        item = queue.get(block=False, timeout=None)
        send_json_data_to_elastic_server(item.get_dict(), index_name, item.test_case_id)


def send_testcases_to_elastic_from_csv(csv_file_path: str, index_name=INDEX_NAME_QTEST):
    raw_test_cases = generate_objects_from_csv_data(csv_file_path, DtoQTestCase)

    filtered_unique_test_case_id = set(raw_test_cases)

    mp_client = MultiProcessingClient(filtered_unique_test_case_id, default_wait_secs=20)
    mp_client.execute_tasks(worker_qtest_testcases, (mp_client.queue, index_name))


