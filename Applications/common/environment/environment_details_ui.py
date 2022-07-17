import os

import sys

from Core.utilities.config_reader import ConfigReader
from Core.utilities.login_config_reader import LoginConfigReader


class EnvironmentDetailsUI:
    #
    # This defines the permitted busines sgroups - PLEASE do not change. Permitting a business group
    # could result in data others are using being deleted.
    #
    permitted_bgroups = {
        "iPA": ["SMS", "SS1", "A01", "A02", "A03", "HA2", "HA3", "HK4", "HK1", "HK6", "HK9", "HKS","HAS","HK2", "None"],
        "ePA": ["HKS"],
        "API": ["A01"]
    }

    def __init__(self, ):
        self.browser_name = None
        self.app = None
        self.url = None
        self.db = None
        self.core_schema_owner = 'PMSPAD'
        self.test_env = None
        self.logins = None
        self._business_group = None
        self.download_folder = None
        self.username = None
        self.letters_output_dir = None
        self.data_type = None

    @property
    def business_group(self):
        return self._business_group

    @business_group.setter
    def business_group(self, business_group):
        self._business_group = business_group

    def load_environment_details(self):
        self.test_env = os.environ.get("TESTENV")
        self.browser_name = os.environ.get("BROWSER")
        self.app = os.environ.get("APP")
        self._business_group = os.environ.get("BGROUP")
        self.data_type = os.environ.get("DATATYPE")

        temp_dl_path = os.environ.get("DOWNLOAD_PATH")
        self.download_folder = (temp_dl_path, os.path.join(os.getenv('USERPROFILE'), 'Downloads'))[
            temp_dl_path in (None, "None") or len(temp_dl_path) <= 0]
        if not os.path.exists(self.download_folder):
            os.makedirs(self.download_folder)


        if not (self.test_env and self.browser_name and
                self._business_group and self.app):
            sys.exit("Failed: You must specify TESTENV, BROWSER, APP and BGROUP to run the tests.")

        if self.business_group not in self.permitted_bgroups[self.app]:
            sys.exit("Failed: You atttempted to run in unapproved business group {}".format(self.business_group))

        config_reader = ConfigReader(self.app)
        self.url = config_reader.get_url(self.test_env)
        self.db = config_reader.get_db(self.test_env)
        self.core_schema_owner = config_reader.get_core_schema_owner(self.test_env)
        self.letters_output_dir = config_reader.get_value_for("FileServerSettings",
                                                              "path") + ":" + os.sep + self.test_env.title() + os.sep

        self.logins = LoginConfigReader()
        self.username = self.logins.get_value(self.business_group, "dbunitid")
        pwd = self.logins.get_value(self.business_group, "dbunitpwd")
        # testurl = 'oracle://DBBAND1C:DBBAND1C@dev01:1521/DSS1'
        self.dburl = "oracle://{}:{}@{}".format(self.username, pwd, self.db)
        self.bgroup_title = self.logins.get_value(self.business_group, "bgrouptitle")
