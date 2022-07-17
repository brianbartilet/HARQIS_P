from Applications.AAA.references.web.base_page_aaa import *
from Applications.AAA.references.dto import *


class PageAAATradingDeskOrders(BasePageAAAEquities):

    def __init__(self, driver, source_id, **kwargs):
        super().__init__(driver=driver, source_id=source_id, **kwargs)
        self.wait_for_page_to_load(5)

    #  region New Order
    @find_element(By.XPATH, "//div[@container-id='orderTicket']")
    def container_new_order(self):
        return WebElement

    @find_element(By.XPATH, "//div[@container-id='orderTicket']//label[contains(@for, 'orderSideToggleSwitch')]")
    def button_toggle_order(self):
        return WebElement

    @find_element(By.XPATH, "//div[@container-id='orderTicket']//input[contains(@id, 'searchField')]")
    def input_stock_search(self):
        return WebElement

    @find_element(By.XPATH, "//div[@container-id='orderTicket']//div[@class='layout-container search-row full-width search-row-hover']")
    def input_stock_search_top_result(self):
        return WebElement

    @find_element(By.XPATH, "//div[@container-id='orderTicket']//a[text()='General']")
    def tab_order(self):
        return WebElement

    @find_element(By.XPATH, "//div[@container-id='orderTicket']//a[text()='Conditional Orders']")
    def tab_order_conditional(self):
        return WebElement

    #  region  General
    @find_element(By.XPATH, "//div[@container-id='orderTicket']//form//button[@class='btn btn-dropdown h-left btn-default dropdown-solid-back-color']")
    def dropdown_order_type(self):
        return WebElement

    @find_element(By.XPATH, "//div[@container-id='orderTicket']//form//button[@class='btn btn-dropdown h-left btn-default btn-order-tif dropdown-solid-back-color']")
    def dropdown_good_till(self):
        return WebElement

    @find_element(By.XPATH, "//div[@container-id='orderTicket']//form//input[contains(@id, 'qtyField')]")
    def input_quantity(self):
        return WebElement

    @find_element(By.XPATH, "//div[@container-id='orderTicket']//form//input[contains(@id, 'orderPriceId')]")
    def input_price(self):
        return WebElement

    @find_element(By.XPATH, "//div[@container-id='orderTicket']//button[@type='submit']")
    def button_submit_order(self):
        return WebElement

    #  endregion

    #  region Conditional

    @find_element(By.XPATH, "//div[@container-id='orderTicket']//form//button[contains(.,'None') and @class='btn btn-dropdown h-left btn-default dropdown-solid-back-color']")
    def dropdown_conditional_field(self):
        return WebElement

    @find_element(By.XPATH, "//div[@container-id='orderTicket']//form//button[contains(.,'Greater') and @class='btn btn-dropdown h-left btn-default dropdown-solid-back-color']")
    def dropdown_conditional_trigger(self):
        return WebElement

    @find_element(By.XPATH, "//div[@container-id='orderTicket']//form//input[@id='conditionPriceId']")
    def input_conditional_price(self):
        return WebElement

    @find_element(By.XPATH, "//div[@container-id='orderTicket']//form//input[@class='ember-view ember-text-field search-query form-control']")
    def input_conditional_expiry_date(self):
        return WebElement

    @find_elements(By.XPATH, "//div[@class='message-box-frame messege-box-inner message-box-border' and contains(., 'Invalid Order')]")
    def div_invalid_order(self):
        return [WebElement]
    #  endregion

    #  region Confirm Order

    @find_element(By.XPATH, "//div[@container-id='orderConfirmation']//button[@data-id='orderConfirmationBtn']")
    def button_confirm_order(self):
        return WebElement

    @find_elements(By.XPATH, "//div[@id='detail-order-execute']//div[@class='font-m fore-color bold']")
    def div_order_values(self):
        return [WebElement]

    #  endregion

    #  endregion

    @find_element(By.XPATH, "//div[@container-id='orderList']//div[@class='ember-table-table-scrollable-wrapper']")
    def container_rows_orders(self):
        return WebElement

    def select_year(self, year: str):
        xpath = "//span[contains(@class, 'year') and text()={0}]".format(year)
        self.driver.find_element(By.XPATH, xpath).click()

    def select_month(self, month: str):
        xpath = "//span[contains(@class, 'month')]"
        months = self.driver.find_elements(By.XPATH, xpath)
        index = int(month)
        months[index -1].click()

    def select_day(self, day: str):
        #  cannot select date today
        index = int(day)
        xpath = "//td[@class='day' and text()={0}]".format(index)
        day = self.driver.find_element(By.XPATH, xpath)
        day.click()

    def set_date_picker(self, date_mm_dd_yyyy: str):
        self.input_conditional_expiry_date().click()
        date = date_mm_dd_yyyy.split('/')
        mm = date[0]
        dd = date[1]
        yyyy = date[2]

        xpath = "//th[@class='datepicker-switch']"
        date_picker = self.driver.find_elements(By.XPATH, xpath)
        self.wait_for_page_to_load(2)
        date_picker[0].click()
        self.wait_for_page_to_load(2)
        date_picker[1].click()

        self.select_year(yyyy)
        self.select_month(mm)
        self.select_day(dd)

    def create_order(self, order_dto: DtoCreateOrderAAA, lot_type=APPEND_NORMAL_LOTS):
        self.navigate_to_page(SidebarNavigationLinks.TRADE)
        self.wait_for_page_to_load(time_sec=30)
        self.wait_for_element_to_be_visible_e(self.button_toggle_order())

        if order_dto.transaction == Order.SELL.value:
            self.button_toggle_order().click()

        self.tab_order().click()

        self.wait_for_element_to_be_visible_e(self.input_stock_search())
        self.input_stock_search().clear()
        self.input_stock_search().send_keys('{0}{1}'.format(order_dto.stock_name, lot_type))
        self.wait_for_page_to_load(2)
        self.input_stock_search_top_result().click()
        self.wait_for_page_to_load(2)
        self.tab_order().click()
        self.wait_for_page_to_load(2)

        self.dropdown_order_type().click()
        self.wait_for_page_to_load(2)
        QList(self.modal_popup_links())\
            .first(lambda x: str(x.text).lower() == order_dto.order_type.lower())\
            .click()

        self.dropdown_good_till().click()
        self.wait_for_page_to_load(2)
        QList(self.modal_popup_links())\
            .first(lambda x: x.text.lower() == str(order_dto.good_until).lower())\
            .click()

        self.input_price().clear()
        self.wait_for_page_to_load(2)
        self.input_price().send_keys(Keys.CONTROL, 'a')
        self.input_price().send_keys(Keys.BACKSPACE)
        self.wait_for_page_to_load(2)
        self.input_price().send_keys('{0}'.format(order_dto.price))
        self.wait_for_page_to_load(2)

        self.input_quantity().clear()
        self.wait_for_page_to_load(2)
        self.input_quantity().send_keys(Keys.CONTROL, 'a')
        self.input_quantity().send_keys(Keys.BACKSPACE)
        self.input_quantity().send_keys('{0}'.format(order_dto.quantity))
        self.wait_for_page_to_load(5)

        if order_dto.condition_field is not ConditionsOrderFieldAAA.NONE.value:
            self.tab_order_conditional().click()

            self.dropdown_conditional_field().click()
            self.wait_for_page_to_load(2)
            QList(self.modal_popup_links()) \
                .first(lambda x: str(x.text).lower() == order_dto.condition_field.lower()) \
                .click()

            self.dropdown_conditional_trigger().click()
            self.wait_for_page_to_load(2)
            QList(self.modal_popup_links()) \
                .first(lambda x: str(x.text).lower() == order_dto.condition_trigger.lower()) \
                .click()

            self.wait_for_element_to_be_visible_e(self.input_conditional_price())
            self.input_conditional_price().clear()
            self.wait_for_page_to_load(2)
            self.input_conditional_price().send_keys(Keys.CONTROL, 'a')
            self.input_conditional_price().send_keys(Keys.BACKSPACE)
            self.wait_for_page_to_load(2)
            self.input_conditional_price().send_keys('{0}'.format(order_dto.condition_price))
            self.wait_for_page_to_load(2)

            if order_dto.condition_expiry_date is not None:
                self.input_conditional_expiry_date().clear()
                self.wait_for_page_to_load(2)
                self.set_date_picker(order_dto.condition_expiry_date)

        self.wait_for_page_to_load(5)
        self.tab_order().click()
        self.wait_for_page_to_load(2)

        values = self.div_order_values()
        order_dto.order_value = float(values[0].text.replace(',', ''))
        order_dto.total_fees = float(values[1].text.replace(',', ''))
        order_dto.net_value = float(values[2].text.replace(',', ''))

        if self.parameters['enable_submit']:
            self.wait_for_page_to_load(5)
            self.button_submit_order().click()

            if len(self.div_invalid_order()) > 0:
                self.button_submit_order().send_keys(Keys.ESCAPE)
            try:
                self.wait_for_page_to_load(5)
                self.button_confirm_order().click()
                order_dto.created = True
            except:
                log.warning("Order was not created.")

        return order_dto

    def get_orders(self):
        container_table_left = ".//div[contains(@id, 'ember') and contains(@class, 'ember-view lazy-list-container " \
                               "ember-table-table-block ember-table-left-table-block')]"
        container_table_right = ".//div[contains(@id, 'ember') and contains(@class, 'ember-view lazy-list-container " \
                                "ember-table-table-block ember-table-right-table-block')]"
        self.navigate_to_page(SidebarNavigationLinks.TRADE)
        self.navigate_to_account_widget(AccountWidgetLinks.ORDER_LIST)
        self.wait_page_to_load(5)

        current_orders = []

        filter_mapping = {}
        last_keys_size = 0
        while True:
            self.wait_for_page_to_load(2)
            stock_basic = self.container_rows_orders().find_element(By.XPATH, container_table_left)
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
                row_i = filter_mapping[key]
                span = row_i.find_elements(By.XPATH, ".//span")
                self.scroll_to_element_e(row_i)
                self.high_light_element(row_i)

                stock_name = str(span[2].text)\
                    .replace(APPEND_NORMAL_LOTS, '')\
                    .replace(APPEND_ODD_LOTS, '')

                stock_detailed = self.container_rows_orders().find_element(By.XPATH, container_table_right)
                values = []
                filtered_detailed = QList(stock_detailed.find_elements(By.XPATH, ".//div[contains(@class, 'panel-table-row')]")) \
                    .where(lambda x: x.text != '')
                for j, row_j in enumerate(filtered_detailed):
                    if i == j:
                        for element in row_j.find_elements(By.XPATH, ".//span"):
                            self.scroll_to_element_e(element)
                            self.high_light_element(element)
                            values.append(element.text)
                        break
                    else:
                        continue
                values.insert(0, stock_name)

                headers = ['stock_name', 'id', 'status', 'transaction', 'quantity', 'price', 'exchange',
                           'filled_quantity', 'pending_quantity', 'average_price', 'order_value', 'net_value', 'order_type',
                           'order_date', 'condition_expiry', 'good_until', 'condition', 'condition_expiry',
                           'condition_order_id']

                data = DtoOrderAAA(**dict(zip(headers, values)))
                current_orders.append(data)

        return current_orders
