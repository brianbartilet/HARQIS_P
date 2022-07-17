from Core.web.base import *
from Applications.load_config import *


class BasePageInvestagrams(BasePage):

    def __init__(self, driver, source_id, **kwargs):
        super().__init__(driver=driver,
                         source_id=source_id,
                         apps_config_data=apps_config,
                         **kwargs)

    def get_table_text_value(self, key):
        pass

    def get_table_text_indexed_column_value(self, key, index=2):
        pass

    def wait_page_to_load(self, secs=5):
        time.sleep(secs)

    def did_page_load(self, *args):
        pass

    def navigate_to_page(self, *args):
        pass

    def login(self, username, password):
        pass

    def logout(self):
        pass

