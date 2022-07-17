from Core.web.base import *
from Applications.load_config import *

from enum import Enum

APPEND_NORMAL_LOTS = '`N'
APPEND_ODD_LOTS = '`O'


class SidebarNavigationLinks(Enum):
    MARKET = 'Market'
    TRADE = 'Trade'
    QUOTE = 'Quote'
    TOP_STOCKS = 'Top Stocks'
    HEAT_MAP = 'Heat Map'
    NEWS = 'News'
    CHART = 'Chart'
    BROKER = 'Broker'


class AccountWidgetLinks(Enum):
    ORDER_LIST = 'Order List'
    PORTFOLIO = 'Portfolio'
    ACCOUNT_SUMMARY = 'Account Summary'
    ORDER_SEARCH = 'Order Search'


class BasePageAAAEquities(BasePage):

    def __init__(self, driver, source_id, **kwargs):
        super().__init__(driver=driver,
                         source_id=source_id,
                         apps_config_data=apps_config,
                         **kwargs)

    @find_elements(By.XPATH, "//li[@data-ember-action]//a")
    def sidebar_navigation_links(self):
        return [WebElement]

    @find_element(By.XPATH, "//a[contains(@class, 'cursor-pointer') and @data-hint='Log Out']")
    def button_logout(self):
        return WebElement

    @find_elements(By.XPATH, "//div[@data-id='inner-widget']//div[contains(@class, 'wdgttl-tab-item ')]")
    def container_widget_account_controls(self):
        return [WebElement]

    @find_elements(By.XPATH, "//div[contains(@id, 'popupId')]//a")
    def modal_popup_links(self):
        return [WebElement]

    def get_table_text_value(self, key):
        pass

    def get_table_text_indexed_column_value(self, key, index=2):
        pass

    def wait_page_to_load(self, *args):
        super().wait_page_to_load(*args)

    def did_page_load(self, *args):
        pass

    def login(self, *args):
        pass

    def navigate_to_page(self, module_name: SidebarNavigationLinks):
        link = QList(self.sidebar_navigation_links()).where(lambda x: x.text == module_name.value).first()
        link.click()
        self.wait_for_page_to_load()

    def navigate_to_account_widget(self, widget_link: AccountWidgetLinks):
        self.wait_for_page_to_load()
        link = QList(self.container_widget_account_controls()).where(lambda x: widget_link.value == x.text).first()
        link.click()
        self.wait_for_page_to_load()

    def logout(self):
        self.button_logout().click()
