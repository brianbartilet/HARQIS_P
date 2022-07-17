import os
import sys

from Core.utilities.config_reader import ConfigReader
from Core.utilities.login_config_reader import LoginConfigReader


class EnvironmentDetailsProC():

    #
    # This defines the permitted busines sgroups - PLEASE do not change. Permitting a business group
    # could result in data others are using being deleted.
    #
    permitted_bgroups = {
        "ProC": ["A01","A02","HK1","HK2",'LBG',"HK7","HK8","HA2","HKS","HAS","HA3","HK3","HK4"]
    }

    def __init__(self, ):
        # these are read from the environment variables
        self.app = None
        self.test_env = None
        self._business_group = None

        # these are read from the config file
        # db / pro c stuff
        # this is read one way
        self.db = None
        self.db_url = None
        self.db_username = None
        self.db_password = None
        self.core_schema_owner = 'PMSPAD'

        # pms stuff. read only once - based on test_env
        self.pms_host = None
        self.pms_port = None
        self.pms_environment_id = None
        self.pms_debug_level = 0

        # the env_path is the part of the command that is fixed per environment
        # path is comprised of the following:
        # cmd_full_path = {env}/{some_variable}/CMDTYPE/bin
        # cmd_env_path = {env}/{some_variable} - is fixed for an environment
        # /CMDTYPE/bin = fixed for a command type - will be read inside the feature file
        self.cmd_env_path = None

        # this is specified in the gherkin
        # hence is read in a different way
        self.pms_user = None
        self.pms_password = None

    @property
    def business_group(self):
        return self._business_group

    @business_group.setter
    def business_group(self, business_group):
        if not self._business_group:
            self._business_group = business_group

    def load_environment_details(self):
        self.test_env = os.environ.get("TESTENV")
        self.app = os.environ.get("APP")
        self._business_group = os.environ.get("BGROUP")

        if not (self.test_env and
                self._business_group and self.app):
            sys.exit("Failed: You must specify TESTENV, BROWSER, APP and BGROUP to run the tests.");

        if self.business_group not in self.permitted_bgroups[self.app]:
            sys.exit("Failed: You atttempted to run in unapproved business group {}".format(self.business_group));


        config_reader = ConfigReader(self.app)
        self.db = config_reader.get_db(self.test_env)
        self.core_schema_owner = config_reader.get_core_schema_owner(self.test_env)

        self.logins = LoginConfigReader()
        self.db_username = self.logins.get_value(self.business_group, "dbunitid")
        self.db_password = self.logins.get_value(self.business_group, "dbunitpwd")
        #testurl = 'oracle://DBBAND1C:DBBAND1C@dev01:1521/DSS1'
        self.db_url = "oracle://{}:{}@{}".format(self.db_username,self.db_password, self.db)

        # need this for the load files
        self.dburl = self.db_url

        # load our pms stuff
        self.pms_host = config_reader.get_value_for(self.test_env, "host")
        self.pms_port = config_reader.get_value_for(self.test_env, "port")
        self.pms_environment_id = config_reader.get_value_for(self.test_env, "env_id")
        self.pms_debug_level = config_reader.get_value_for(self.test_env, "debug_level")

        #set the path
        self.cmd_env_path = config_reader.get_value_for(self.test_env, "env_path")
