import os
import sys

from Core.utilities.config_reader import ConfigReader
from Core.utilities.login_config_reader import LoginConfigReader


class EnvironmentDetailsApi():

    #
    # This defines the permitted busines sgroups - PLEASE do not change. Permitting a business group
    # could result in data others are using being deleted.
    #
    permitted_bgroups = {
        "API": ["A01","A02","HK1","HK2",'LBG',"HK7","HK8","HA2","HKS","HA3","HK3","HK4"],
        "Interfaces": ["A01", "A02", "HK1", "HK2", 'LBG', "HK7", "HK8", "HA2", "HKS", "HA3", "HK3", "HK4"],
        "Sandbox": ['HKS']
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

        # this is the best case solution at the moment - I have no idea on the number of other URL that is possible
        self.api_url = None
        self.encoding = None

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
        self.api_area = os.environ.get("API_AREA")

        if not (self.test_env and
                self._business_group and self.app and self.api_area):
            sys.exit("Failed: You must specify TESTENV, BROWSER, APP and BGROUP to run the tests.");

        # retaining this permitted business groups - but may not be useful in APIs as we need to pass bgroups
        if self.business_group not in self.permitted_bgroups[self.app]:
            sys.exit("Failed: You atttempted to run in unapproved business group {}".format(self.business_group))


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
        self.api_url = config_reader.get_value_for(self.test_env, self.api_area)
        self.encoding = config_reader.get_value_for(self.test_env, "encoding")