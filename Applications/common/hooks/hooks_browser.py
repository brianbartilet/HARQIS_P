import threading

from Applications.common.hooks.base_hook import *

log = custom_logger(logger_name="Browser Hooks")

class BrowserHooks(BaseHooks):

    @staticmethod
    def process_environment(context):
        pass

    @staticmethod
    def process_feature_tags(feature):
        pass

    @staticmethod
    def process_scenario_tags(scenario):
        pass

    @staticmethod
    def before_all(context):
        pass

    @staticmethod
    def before_feature(context, feature):
        pass

    @staticmethod
    def before_scenario(context, scenario):

        log.info("Starting the browser..")

        if use_threading:
            pass
        else:
            context.env_init.start_browser(context)

    @staticmethod
    def before_step(context, step):
        pass

    @staticmethod
    def after_step(context, step):
        pass

    @staticmethod
    def after_scenario(context, scenario):
        context.browser.quit()

    @staticmethod
    def after_feature(context, feature):
        pass

    @staticmethod
    def after_all(context):
        pass
