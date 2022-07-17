from Applications.AAA.references.web.base_page_aaa import *
from Applications.AAA.references.dto import *


class PageAAATradingDeskAccount(BasePageAAAEquities):

    def __init__(self, driver, source_id, **kwargs):
        super().__init__(driver=driver, source_id=source_id, **kwargs)
        self.wait_for_page_to_load(5)

    @find_element(By.XPATH, "//div[@container-id='accountSummary']")
    def container_rows_account_details(self):
        return WebElement

    def get_account_information(self):

        self.navigate_to_page(SidebarNavigationLinks.TRADE)
        self.navigate_to_account_widget(AccountWidgetLinks.ACCOUNT_SUMMARY)

        account_details = []
        rows = self.container_rows_account_details()\
            .find_elements(By.XPATH, ".//div[@class='layout-container pad-s-tb border-bottom']")
        for row in rows:
            span_values = row.find_elements(By.XPATH, ".//span")
            element = span_values[1]
            self.scroll_to_element_e(element)
            account_details.append(element.text)

        headers = ['cash_balance', 'available_cash', 'pending_cash', 'available_to_withdraw', 'unsettled_sales',
                   'payable_amount', 'od_limit', 'portfolio_value', 'total_portfolio_value']

        dto = DtoAccountAAA(convert_kwargs=True, clean_chars=[','],
                            **dict(zip(headers, account_details)))

        return dto

