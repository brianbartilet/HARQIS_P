from Applications.StrenuousLife import *
from Applications.load_config import *

NODE_ID_NAME = 'StrenuousLife'

webdriver_config = apps_config[NODE_ID_NAME]['webdriver']
wdf = WebDriverFactory
driver = wdf.get_web_driver_instance(**webdriver_config)


class TestStrenuousLife(TestCase):

    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)

    def test_get_agons(self):
        pl = PageStrenuousLogin(driver, source_id='StrenuousLife')
        pl.login(pl.parameters['username'], pl.parameters['password'])

        pa = PageAgons(driver, source_id=NODE_ID_NAME)
        agon = pa.get_latest_agon_info()
        pa.assert_that(agon, is_not(None))
        pa.driver.close()

