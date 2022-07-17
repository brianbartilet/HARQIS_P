from Applications.CitisecOnline import *
from Applications.load_config import *

webdriver_config = apps_config['COLFinancial']['webdriver']
wdf = WebDriverFactory
driver = wdf.get_web_driver_instance(**webdriver_config)


class TestCOLFinancial(TestCase):

    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)