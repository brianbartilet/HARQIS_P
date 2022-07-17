from Applications.AAA.references.web.base_page_aaa import *
from Applications.AAA.references.dto import *

CLEAN_CHARS = ['%', '(', ')', ',']


class PageAAATradingDeskPortfolio(BasePageAAAEquities):

    def __init__(self, driver, source_id, **kwargs):
        super().__init__(driver=driver, source_id=source_id, **kwargs)
        self.wait_for_page_to_load(5)

    @find_element(By.XPATH, "//div[@container-id='portfolio']//div[@class='ember-table-table-scrollable-wrapper']")
    def container_rows_portfolio(self):
        return WebElement

    def get_portfolio_information(self):
        container_table_left = ".//div[contains(@id, 'ember') and contains(@class, 'ember-view lazy-list-container " \
                               "ember-table-table-block ember-table-left-table-block')]"
        container_table_right = ".//div[contains(@id, 'ember') and contains(@class, 'ember-view lazy-list-container " \
                                "ember-table-table-block ember-table-right-table-block')]"
        self.navigate_to_page(SidebarNavigationLinks.TRADE)
        self.navigate_to_account_widget(AccountWidgetLinks.PORTFOLIO)

        portfolio = []
        self.wait_for_page_to_load(5)

        filter_mapping = {}
        last_keys_size = 0
        while True:
            self.wait_for_page_to_load(2)
            stock_basic = self.container_rows_portfolio().find_element(By.XPATH, container_table_left)
            filtered_basic = QList(stock_basic.find_elements(By.XPATH, ".//div[contains(@class, 'panel-table-row')]"))\
                .where(lambda x: x.text != '')

            for item in filtered_basic:
                filter_mapping[item.text] = item

            cur_size = len(filter_mapping.keys())

            last = filtered_basic[-1]
            self.scroll_to_element_e(last)

            # check if size of keys does not change exit
            if cur_size == last_keys_size:
                break
            else:
                last_keys_size = cur_size

        for i, key in enumerate(filter_mapping.keys()):
            span = filter_mapping[key].find_elements(By.XPATH, ".//span")
            stock_name = str(span[2].text)\
                .replace(APPEND_NORMAL_LOTS, '')\
                .replace(APPEND_ODD_LOTS, '')
            stock_description = span[3].text

            stock_detailed = self.container_rows_portfolio().find_element(By.XPATH, container_table_right)
            values = []
            filtered_detailed = QList(stock_detailed.find_elements(By.XPATH, ".//div[contains(@class, 'panel-table-row')]")) \
                .where(lambda x: x.text != '')
            for j, row_j in enumerate(filtered_detailed):
                self.scroll_to_element_e(row_j)
                if i == j:
                    for element in row_j.find_elements(By.XPATH, ".//span"):
                        self.scroll_to_element_e(element)
                        values.append(element.text)
                    break
                else:
                    continue
            values.insert(0, stock_name)
            values.insert(1, stock_description)

            headers = ['symbol', 'description', 'id', 'quantity', 'sell_pending', 'buy_pending', 'available_quantity',
                       'market_price', 'average_cost', 'cost_value', 'market_value', 'gain_loss_value',
                       'gain_loss_percentage', 'portfolio_percentage', 'exchange']

            portfolio.append(DtoPortfolioItemAAA(**dict(zip(headers, values)), convert_kwargs=True, clean_chars=CLEAN_CHARS))

        return portfolio



