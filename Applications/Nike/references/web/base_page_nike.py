from Core.web.base import *
from Applications.load_config import *

from random import randrange, uniform


class BasePageNike(BasePage):

    def __init__(self, driver, source_id, **kwargs):
        super().__init__(driver=driver,
                         source_id=source_id,
                         apps_config_data=apps_config,
                         **kwargs)

        self.type_range_delay = 0.5

    @find_element(By.ID, 'AccountMenu')
    def menu_account(self):
        return WebElement

    @find_element(By.ID, 'AccountMenu-Menu')
    def menu_account_dropdown(self):
        return WebElement

    @find_elements(By.XPATH, "//div[@id='AccountMenu-Menu']//li//*[@role='option']")
    def menu_account_dropdown_links(self):
        return []

    @find_element(By.XPATH, "//a[@aria-label='Bag' and contains(@class,'cart-container')]")
    def icon_go_to_cart(self):
        return WebElement

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

    def enter_keys_with_delay(self, element: WebElement, str_input):
        element.click()
        element.clear()

        delay = uniform(0.1, self.type_range_delay)
        for s in str_input:
            if str(s).istitle():
                element.send_keys(Keys.SHIFT + str(s).lower())
            else:
                element.send_keys(s)
            time.sleep(delay)

