from Applications.BPI.references.web.base_page_bpi import *


class PageBPIAccounts(BasePageBPI):

    @find_element(By.XPATH, "//input[contains(@name, 'username')]")
    def textbox_username(self):
        return WebElement

    @find_elements(By.XPATH, "//div[contains(@class, 'product-group')]")
    def accounts_heading_expand_toggle(self):
        return WebElement

    def __init__(self, driver, source_id, **kwargs):
        super().__init__(driver=driver, source_id=source_id, **kwargs)
        self.driver.get(self.url + "/my-accounts")
        self.wait_for_page_to_load(3)

    def navigate_to_page(self, *args):
        self.driver.get(self.url + "/my-accounts")

    def collapse_all_views_account(self):
        elements = self.accounts_heading_expand_toggle()
        for e in elements:
            if not 'panel-open' in e.get_attribute('class'):
                e.find_element(By.XPATH, "./div[@class='product-heading']").click()

    def select_account(self, name: str):
        xpath = "//ui-bpi-account-card-ng[contains(.,'{0}')]".format(name.upper())
        element = self.driver.find_element(By.XPATH, xpath)
        element.click()

    def get_transactions(self, account_name):
        self.select_account(account_name)

