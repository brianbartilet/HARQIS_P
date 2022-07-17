from Applications.AAA import *
from Applications.load_config import *

APP_NAME = 'AAAHeadless'
webdriver_config = apps_config[APP_NAME]['webdriver']
wdf = WebDriverFactory


class TestAAAEquities(TestCase):

    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)

    def test_login(self):
        driver = wdf.get_web_driver_instance(**webdriver_config)
        pl = PageAAALogin(driver, source_id=APP_NAME)
        pl.login()
        driver.close()

    def test_navigate(self):
        driver = wdf.get_web_driver_instance(**webdriver_config)
        pl = PageAAALogin(driver, source_id=APP_NAME)
        pl.login()

        pt = PageAAATradingDeskMarket(driver, source_id=APP_NAME)
        pt.navigate_to_page(SidebarNavigationLinks.MARKET)
        pt.navigate_to_page(SidebarNavigationLinks.QUOTE)
        pt.navigate_to_page(SidebarNavigationLinks.TOP_STOCKS)
        pt.navigate_to_page(SidebarNavigationLinks.HEAT_MAP)
        pt.navigate_to_page(SidebarNavigationLinks.NEWS)
        pt.navigate_to_page(SidebarNavigationLinks.CHART)
        pt.navigate_to_page(SidebarNavigationLinks.BROKER)

        pl.logout()
        driver.close()

    def test_get_market_info(self):
        driver = wdf.get_web_driver_instance(**webdriver_config)
        pl = PageAAALogin(driver, source_id=APP_NAME)
        pl.login()

        pt = PageAAATradingDeskMarket(driver, source_id=APP_NAME)
        obj = pt.get_instrument_market_info('APX')
        pl.assert_that(obj.symbol, equal_to('APX'))
        pl.logout()
        driver.close()

    def test_get_portfolio(self):
        driver = wdf.get_web_driver_instance(**webdriver_config)
        pl = PageAAALogin(driver, source_id=APP_NAME)
        pl.login()

        pt = PageAAATradingDeskPortfolio(driver, source_id=APP_NAME)
        data = pt.get_portfolio_information()
        pl.assert_that(len(data), greater_than_or_equal_to(0))
        pl.logout()
        driver.close()

    def test_get_orders(self):
        driver = wdf.get_web_driver_instance(**webdriver_config)
        pl = PageAAALogin(driver, source_id=APP_NAME)
        pl.login()

        pt = PageAAATradingDeskOrders(driver, source_id=APP_NAME)
        data = pt.get_orders()
        pl.assert_that(len(data), greater_than_or_equal_to(0))
        pl.logout()
        driver.close()

    def test_get_account_info(self):
        driver = wdf.get_web_driver_instance(**webdriver_config)
        pl = PageAAALogin(driver, source_id=APP_NAME)
        pl.login()

        pt = PageAAATradingDeskAccount(driver, source_id=APP_NAME)
        data = pt.get_account_information()
        pl.assert_that(data.cash_balance, greater_than_or_equal_to(0))
        pl.logout()
        driver.close()

    @pytest.mark.skip(reason=SKIP_TEST_TRANSACTION)
    def test_create_order(self):
        driver = wdf.get_web_driver_instance(**webdriver_config)

        pl = PageAAALogin(driver, source_id=APP_NAME)
        pl.login()

        order_dto = DtoCreateOrderAAA(
            stock_name='APX',
            transaction=Order.BUY,
            order_type=OrderType.LIMIT,
            quantity=1000,
            price=1.2,
            good_until=OrderValidUntil.GTC,
            condition_field=ConditionsOrderFieldAAA.LAST_PRICE,
            condition_price=1.2,
            condition_trigger=ConditionsOrderTriggerAAA.GREATER_THAN_OR_EQUAL_TO,
            condition_expiry_date='12/22/2020'
        )
        pt = PageAAATradingDeskOrders(driver, source_id=APP_NAME)
        data = pt.create_order(order_dto)
        pl.assert_that(data, equal_to(True))
        pl.logout()
        driver.close()
