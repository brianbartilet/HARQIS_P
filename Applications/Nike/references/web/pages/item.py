from Applications.Nike.references.web.base_page_nike import *
import time


class PageItemNike(BasePageNike):

    def __init__(self, driver, source_id, **kwargs):
        super().__init__(driver=driver, source_id=source_id, **kwargs)
        self.driver.get(kwargs.get('item_url', self.url))
        self.wait_for_page_to_load(5)
        self.max_time_wait_mins = kwargs.get('max_time_wait_mins', 20)

    @find_elements(By.XPATH, "//div[contains(@class,'button')]//div[text()='Coming Soon']")
    def buttons_upcoming_soon(self):
        return WebElement

    @find_elements(By.XPATH, "//li[@data-qa='size-available']//button[@data-qa='size-dropdown']")
    def buttons_available_sizes(self):
        return WebElement

    @find_element(By.XPATH, "//button[@data-qa='add-to-cart' and text()='Add to Bag']")
    def button_add_to_bag(self):
        return WebElement

    @find_element(By.XPATH, "//button[@data-qa='feed-buy-cta' and contains(text(),'Buy')]")
    def button_buy_at_drop(self):
        return WebElement

    def wait_for_item_availability(self, poll_secs=2, max_tries=None):
        if max_tries is None:
            max_tries = int((self.max_time_wait_mins * 60) / poll_secs)
        else:
            max_tries = max_tries
        self.wait_for_page_to_load(poll_secs)

        trial = 0
        displayed = True
        while displayed:
            time.sleep(poll_secs)

            elements = self.buttons_upcoming_soon()
            self.wait_for_page_to_load(poll_secs)
            if len(elements) > 0:
                displayed = QList(elements).first().is_displayed()
            else:
                self.log.info("Element not found. [Coming Soon]")
                break

            trial += 1
            if trial == max_tries:
                self.log.error("Max timeout achieved for waiting for element.")
                break
            else:
                self.log.info("Waiting for element to disappear... [Coming Soon]")
                self.driver.refresh()
                self.wait_for_page_to_load(poll_secs)

    def select_order_details(self, size: str):
        self.wait_for_page_to_load(2)

        try:
            self.wait_for_element_to_appear_e(self.button_buy_at_drop())
        except:
            raise Exception("Item Out of Stock..")

        buttons_available_sizes = QList(self.buttons_available_sizes())\
            .where(lambda x: size.strip(' ') in x.text)\

        if len(buttons_available_sizes) == 0:
            raise Exception("The selected SIZE is already unavailable!")
        else:
            self.wait_for_page_to_load(2)
            buttons_available_size = buttons_available_sizes.first()
            buttons_available_size.click()

        self.button_buy_at_drop().click()
        self.wait_for_page_to_load(5)

    def go_to_cart(self):

        self.driver.refresh()
        self.wait_for_page_to_load()
        self.icon_go_to_cart().click()
        self.wait_for_page_to_load(2)


