from Applications.CitisecOnline.references.web.base_page_citisec import *
from Core.utilities.json_util import JsonObject


class DtoStockPortfolio(JsonObject):
    action = None
    stock_code = None
    stock_name = None
    portfolio_percent = None
    market_price = None
    average_price = None
    total_shares = None
    uncommitted_shares = None
    market_value = None
    gain_loss_value = None
    gain_loss_percentage = None


class PagePortfolio(BasePageCOLFinancial):

    tab_menu_trade = (By.XPATH, '//*[@id="CT"]')
    tab_menu_trade_portfolio = (By.XPATH, '//*[@id="L1_3_4"]')
    table_portfolio = (By.XPATH, '//table[contains(., "Cash Balance")]')

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver
        self.navigate_to_page()
        self.wait_for_page_to_load()

    def navigate_to_page(self):
        self.switch_frame(*self.frame_header)
        self.driver.find_element(*self.tab_menu_trade).click()
        self.driver.find_element(*self.tab_menu_trade_portfolio).click()
        self.wait_for_page_to_load()

    def get_portfolio_information(self):
        self.wait_page_to_load()
        self.reload_frame('main')
        self.switch_frame(*self.frame_main)

        self.wait_page_to_load(5)

        table = self.get_element(*self.table_portfolio)

        results = self.get_table_body_rows(table)[13:-6]
        ret = []
        params = ['action', 'stock_code','stock_name', 'portfolio_percent', 'market_price', 'average_price',
                  'total_shares', 'uncommitted_shares', 'market_value', 'gain_loss_value', 'gain_loss_percentage']

        for item in results:
            text = []
            for c in item:
                text.append(c.text)
            dto = DtoStockPortfolio(**dict(zip(params, text)))
            ret.append(dto)

        return ret