from Core.web.base import *
from Applications.load_config import *
from Applications.BPI.references.dto.transaction import DtoTransaction


class BasePageBPI(BasePage):
    base_xpath_transaction = 'transaction__header'

    def __init__(self, driver, source_id, **kwargs):
        super().__init__(driver=driver,
                         source_id=source_id,
                         apps_config_data=apps_config,
                         **kwargs)

    @find_elements(By.XPATH, "//div[@class='{0}']".format(base_xpath_transaction))
    def transaction_rows(self):
        return [WebElement]

    def get_table_text_value(self, key):
        pass

    def get_table_text_indexed_column_value(self, key, index=2):
        pass

    def wait_page_to_load(self, secs=5):
        self.wait_for_page_to_load(secs)

    def did_page_load(self, *args):
        pass

    def navigate_to_page(self, *args):
        pass

    def login(self, username, password):
        pass

    def logout(self):
        pass

    def get_table_data(self):

        xpath_transaction_date = "//div[@class='transaction__header__date']"
        xpath_transaction_details = "//div[contains(@class, 'transaction__header__details_and_amount')]"
        output = []
        for item in self.transaction_rows():
            wb_date = item.find_element(By.XPATH, xpath_transaction_date)
            wb_details = item.find_element(By.XPATH, xpath_transaction_details)

            details = wb_details.text.split('\n')
            dto = DtoTransaction(date=wb_date.text.replace('\n', ' '),
                                 memo=details[0],
                                 payee=details[1],
                                 value=details[2].replace('PHP ', ''),
                                 running_balance=details[3].replace('PHP ', ''),
                                 )
            output.append(dto)

        return output