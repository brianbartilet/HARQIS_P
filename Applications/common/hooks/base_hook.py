import os
import shutil

from Applications.common.environment.environment_details_api import EnvironmentDetailsApi
from Applications.common.environment.environment_details_ui import EnvironmentDetailsUI

from Applications.common.environment.environment_details_proc import EnvironmentDetailsProC
# TODO:  Get from environment
from Core.utilities.custom_logger import custom_logger


# Constants
FAILED = "failed"

# Global Variables.
use_threading = True

log = custom_logger(logger_name="Base Hooks")


class BaseHooks(object):

    def __init__(self):
        pass

    @staticmethod
    def process_environment(context):
        context.env_details = EnvDetailFactory.get_env_details(os.environ.get("APP"))


    @staticmethod
    def process_feature_tags(feature):
        pass

    @staticmethod
    def process_scenario_tags(scenario):
        pass

    @staticmethod
    def before_all(context):
        #BaseHooks.process_environment(context)
        pass

    @staticmethod
    def before_feature(context, feature):
        pass

    @staticmethod
    def before_scenario(context, scenario):
        pass

    @staticmethod
    def before_step(context, step):
        pass

    @staticmethod
    def after_step(context, step):
        pass

    @staticmethod
    def after_scenario(context, scenario):
        pass

    @staticmethod
    def after_feature(context, feature):
        pass

    @staticmethod
    def after_all(context):
        context.result_dir = None



# need to abstract one more level:
class EnvDetailFactory(object):

    # defining these now, but may be unused
    APP_PROC = "ProC"
    APP_IPA = "iPA"
    APP_EPA = "ePA"
    APP_API = "API"
    APP_INTERFACES = 'Interfaces'
    APP_SANDBOX = 'Sandbox'
    environ_details = {
        APP_SANDBOX: EnvironmentDetailsApi
    }

    @staticmethod
    def get_env_details(app_name : str):

        # may change this to if, elif case, but for now this works
        env_details = EnvDetailFactory.environ_details[app_name]()
        env_details.load_environment_details()

        return env_details