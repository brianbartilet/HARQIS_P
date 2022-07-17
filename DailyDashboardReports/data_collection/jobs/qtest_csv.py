from Core.reporting.dashboard.data_collection.helpers.qtest import *
from Core.reporting.dashboard.data_collection.job_manager import *


def run_qtest_testcases_from_csv():
    send_testcases_to_elastic_from_csv(csv_file_path="QTestData.csv",
                                       index_name=run_qtest_testcases_from_csv.__name__)
