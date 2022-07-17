from Applications.Investagrams import *
from Applications.load_config import *

NODE_ID_NAME = 'Investagrams'

webdriver_config = apps_config[NODE_ID_NAME]['webdriver']
wdf = WebDriverFactory


class TestInvestagrams(TestCase):

    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)

    def test_get_screener_results(self):
        driver = wdf.get_web_driver_instance(**webdriver_config)
        pl = PageInvestagramsLogin(driver, source_id=NODE_ID_NAME)
        pl.login(pl.parameters['username'], pl.parameters['password'])

        sp = PageInvestagramsScreener(driver, source_id=NODE_ID_NAME)
        sp.select_screener("Swing Sniper V")
        data = sp.get_all_results()
        sp.assert_that(data, is_not(None))

    def test_get_stock_info(self):
        driver = wdf.get_web_driver_instance(**webdriver_config)
        sp = PageInvestegramsStock(driver, source_id=NODE_ID_NAME)
        sp.get_stock_information("APX")
        driver.close()
