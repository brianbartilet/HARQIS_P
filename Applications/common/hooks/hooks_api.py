from datetime import datetime



from Applications.common.hooks.base_hook import *
from Core.web.api.base_steps import ApiServiceManager
from Core.web.base.api_client import BaseApiClient
from Core.utilities.csv_report_generator import CsvReportGenerator
from Core.utilities.custom_logger import custom_logger
from Core.utilities.logged_assert_helper import LoggedAssertHelper

FAILED = "failed"

# Global Variables.


log = custom_logger(logger_name="Api Hooks")


class ApiHooks(BaseHooks):
    @staticmethod
    def process_environment(context):

        pass

    @staticmethod
    def before_all(context):

        # this is specific to api

        #context.evidence_base_dir = os.path.join(os.getcwd(), "evidence", os.environ.get("APP"),
        #                                         os.environ.get("TESTENV"),
        #                                         datetime.today().strftime('%d%m%y_T%H%M%S'))

        # this is specific to Api

        context.start_time = datetime.now()

        # this is all in base hook
        # generate our object
        #context.client = BaseApiClient(context.env_details.api_url, response_encoding=context.env_details.encoding)

        #ApiServiceManager.add_service(InterfaceApiServiceInherit(context.client))

    @staticmethod
    def before_feature(context, feature):
        pass
    @staticmethod
    def before_scenario(context, scenario):
        log.info("Before scenario : %s\n", scenario.name)
        context.report_generator = None
        # add this so we can use logged assert helper anywhere

        if os.environ.get("TESTEVIDENCE") == "Y":
            pass

        context.lah = LoggedAssertHelper(context.report_generator)

    @staticmethod
    def after_scenario(context, scenario):
        if os.environ.get("TESTEVIDENCE") == "Y":
            context.report_generator.set_result(str(scenario.status).upper())
            context.report_generator.write_report()

    @staticmethod
    def after_feature(context, feature):
        pass

    @staticmethod
    def after_all(context):
        end_time = datetime.now()

        #log.info("Over all run time was {}\n".format(end_time - context.start_time))
