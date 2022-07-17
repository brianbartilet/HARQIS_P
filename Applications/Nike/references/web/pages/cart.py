from Applications.Nike.references.web.base_page_nike import *
import time


class PageCartNike(BasePageNike):

    def __init__(self, driver, source_id, **kwargs):
        super().__init__(driver=driver, source_id=source_id, **kwargs)
        #self.driver.get(self.url + '/en/cart')
        #self.wait_for_page_to_load()
        self.payment_details = kwargs.get("payment_details", None)
        self.enable_order = kwargs.get("enable_order", False)

    @find_element(By.XPATH, "//*[@data-automation='cart-summary']//button[text()='Member Checkout' and @data-automation='member-checkout-button']")
    def button_member_checkout(self):
        return WebElement

    @find_element(By.XPATH, "//label//span[contains(@class,'checkbox')]")
    def checkbox_shipping_consent(self):
        return WebElement

    @find_element(By.ID, 'shippingSubmit')
    def button_continue_billing(self):
        return WebElement

    @find_element(By.ID, 'billingSubmit')
    def button_continue_to_payment(self):
        return WebElement

    @find_element(By.ID, 'BtnPurchase')
    def button_place_order(self):
        return WebElement

    @find_element(By.NAME, 'CreditCardHolder')
    def text_name_on_card(self):
        return WebElement

    @find_element(By.NAME, 'KKnr')
    def text_cc_number(self):
        return WebElement

    @find_element(By.NAME, 'KKMonth')
    def dropdown_expiry_month(self):
        return WebElement

    @find_element(By.NAME, 'KKYear')
    def dropdown_expiry_year(self):
        return WebElement

    @find_element(By.NAME, 'CCCVC')
    def text_cvv(self):
        return WebElement

    @find_element(By.NAME, 'prefill')
    def checkbox_save_details(self):
        return WebElement

    @find_element(By.XPATH, "//button[@id='continue' and text()='Continue']")
    def button_submit(self):
        return WebElement

    def member_checkout(self):
        self.button_member_checkout().click()
        self.wait_for_page_to_load(5)

    def process_payment_details(self, payment_details: dict):

        self.switch_frame(None, 'paymentIFrame')

        self.text_name_on_card().send_keys(payment_details['name_on_card'])
        self.enter_keys_with_delay(self.text_cc_number(), payment_details['cc_number'])

        self.select_by_option_value_e(payment_details['expiry_month'], self.dropdown_expiry_month())
        self.select_by_option_value_e(payment_details['expiry_year'], self.dropdown_expiry_year())

        self.text_cvv().send_keys(payment_details['cvv'])

        self.checkbox_save_details().click()

        if self.enable_order:
            self.button_place_order().click()
            self.button_submit().click()
            self.wait_for_page_to_load(10000)


    def payment_checkout(self):
        """
        Pre-filled information should be made
        :return:
        """
        self.wait_for_page_to_load(5)

        self.checkbox_shipping_consent().click()
        self.button_continue_billing().click()
        self.wait_for_page_to_load(3)

        self.button_continue_to_payment().click()
        self.wait_for_page_to_load(10)

        self.process_payment_details(self.payment_details)



