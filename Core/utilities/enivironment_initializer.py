import os
from Core.datautils.data_set_definitition import DataSetDefinition
from Core.utilities.move_data_utils import MoveDataUtils
from Core.base.webdriver_factory import WebDriverFactory
from Core.utils.custom_logger import custom_logger
from Core.datautils.json_data_utils import JsonDataUtils
log = custom_logger(logger_name="environment")

class EnvironmentInitializer():



    def valid_filename(self,name):
        keepcharacters = (' ', '.', '_')
        return "".join(c for c in name if c.isalnum() or c in keepcharacters).rstrip()


    def get_feature_data_dir(self,name):
        return "".join(c for c in name if c.isalnum()).rstrip().lower()


    def start_browser(self,context):
        wdf = WebDriverFactory
        context.browser = wdf.get_web_driver_instance(context.env_details.browser_name, context.env_details.download_folder)
        #context.browser.maximize_window()
        try:
            # this is needed for ie.
            context.browser.implicitly_wait(5)
        except:
            ...
        finally:
            context.driver = context.browser

        log.info("Browser started and ready for use.")


    def  load_scenario_data(self,context):
        if context.dataset is not None:
            context.dataset.load_data(context.env_details.dburl, context.env_details.core_schema_owner,
                                      context.feature_data_dir, context.env_details.business_group, ['group2'])
        log.info("Data loaded and ready for use.")


    def load_feature_data(self,context, feature):

        test_data_root_dir = os.path.join('TestScripts',os.environ.get("APP"), 'testdata')
        feature_data_dir = os.path.join(test_data_root_dir, self.get_feature_data_dir(feature.name))

        test_data_def_file = os.path.join(feature_data_dir, "test_data_definition.json")
        context.dataset = None
        if os.path.isfile(test_data_def_file):
            datasetdef = DataSetDefinition.load_definition(test_data_def_file)
            ds = MoveDataUtils(datasetdef)
            ds.load_data(context.env_details.dburl, context.env_details.core_schema_owner, feature_data_dir,
                         context.env_details.business_group, ['group1'])
            context.dataset = ds
            context.feature_data_dir = feature_data_dir

    """
    Loads feature data JSON file from Application module for the given runtime environment. 
    The file sits under Application\{APP}\datafiles\{TESTENV}\{Feature_Folder}\****.json
    
    Feature_Folder is actual name of the folder where feature files reside in. 
    For example WebPMS or Workflow or Contribution or Titania
    
    The data should configured at BGROUP level inside the json file.
    
    app_data_dict : The context variable that holds the data and refreshed for every feature invocation.
    
    """
    def load_application_feature_data(self, context, feature):
        app_data_root_dir = os.path.join("Application", os.environ.get("APP"), "datafiles")
        app_data_env_dir = os.path.join(app_data_root_dir, os.environ.get("TESTENV"))
        app_data_module_dir = os.path.join(app_data_env_dir, self.get_module_from_feature_file_path(feature.filename))
        jdu = JsonDataUtils()
        app_data_file = jdu.get_test_data_json_file(app_data_module_dir, self.get_feature_data_dir(feature.name))
        if os.path.isfile(app_data_file):
            app_data_dict = jdu.get_json_data_as_dictionary(app_data_file)[os.environ.get("BGROUP")]
            context.app_data_dict = app_data_dict

    def get_module_from_feature_file_path(self, featurepath):
        return featurepath.split("\\")[2]



