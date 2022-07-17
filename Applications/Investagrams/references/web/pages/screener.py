from Applications.Investagrams.references.web.base_page_investagrams import *
from Applications.Investagrams.references.dto.stock import DtoStockInvestagrams


class PageInvestagramsScreener(BasePageInvestagrams):

    #@find_element(By.XPATH, "//select[contains(@data-ng-change, 'loadStockScreenerUserOptionsByIdAndUser')]")
    @find_element(By.XPATH, "//button[contains(.,'Saved Custom Screener')]")
    def select_my_screeners(self):
        return WebElement

    #@find_element(By.XPATH, "//button[contains(.,'Run') and @title='Run Screener']")
    @find_element(By.XPATH, "//button[contains(.,' Run Screener ')]")
    def button_run(self):
        return WebElement

    @find_elements(By.ID, "AlertNotificationPanelMessage")
    def alert_no_results(self):
        return

    def __init__(self, driver, source_id, **kwargs):
        super().__init__(driver=driver, source_id=source_id, **kwargs)
        self.driver.get(self.url + "/ProScreener/Screener/")

    def select_screener(self, name):
        self.wait_for_page_to_load(10)
        select_e = self.select_my_screeners()
        self.wait_for_element_to_be_stale_e(select_e)
        self.select_my_screeners().click()

        #self.select_by_option_value_e(name, select_e)
        xpath_dropdown = "//a[@href='#' and contains(., ' {0} ')]".format(name)
        dropdown = self.driver.find_element(By.XPATH, xpath_dropdown)
        self.wait_for_page_to_load(3)
        dropdown.click()

        #self.wait_for_page_to_load(8)
        #self.button_run().click()

    def get_all_results(self):
        self.wait_page_to_load()

        if len(self.alert_no_results()) > 0:
            if self.alert_no_results()[0].is_displayed():
                return []

        results = self.get_table_body_rows()

        try:
            check = True if len(QList(results).first()[0].text) > 0 else False
        except:
            check = False

        ret = []
        if check:
            #  use first 3 columns only
            params = ['name', 'last', 'change_percent']
        else:
            params = ['empty','name', 'last', 'change_percent']

        for item in results:
            text = []
            for i, c in enumerate(item):
                if i == 0:
                    text_i = str(c.text).split('\n')[0]
                else:
                    text_i = c.text
                text.append(text_i)

            dto = DtoStockInvestagrams(convert_kwargs=True,
                                       clean_chars=['%', '(', ')'],
                                       **dict(zip(params, text)))
            ret.append(dto)

        return ret