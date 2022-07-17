from Applications.BPI import *
from Applications.load_config import *

NODE_ID_NAME = 'BPI'

webdriver_config = apps_config[NODE_ID_NAME]['webdriver']
wdf = WebDriverFactory
driver = wdf.get_web_driver_instance(**webdriver_config)


class TestBPIAccounts(TestCase):

    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)

    def test_get_accounts_savings(self):
        pl = PageBPILogin(driver, source_id=NODE_ID_NAME)
        pl.login(pl.parameters['username'], pl.parameters['password'])

        pa = PageBPIAccounts(driver, source_id=NODE_ID_NAME)
        pa.collapse_all_views_account()
        pa.select_account('SAVINGS ACCOUNT')
        pa.wait_for_page_to_load(3)
        pa.get_table_data()
        pa.driver.close()

    def test_get_accounts_checkings(self):
        pl = PageBPILogin(driver, source_id=NODE_ID_NAME)
        pl.login(pl.parameters['username'], pl.parameters['password'])

        pa = PageBPIAccounts(driver, source_id=NODE_ID_NAME)
        pa.collapse_all_views_account()
        pa.select_account('CHECKING ACCOUNT')
        pa.wait_for_page_to_load(3)
        pa.get_table_data()
        pa.driver.close()

