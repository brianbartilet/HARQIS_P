from Applications.CitisecOnline.references.web.base_page_citisec import *


class PageLogin(BasePageCOLFinancial):

    textbox_user_id_first = (By.NAME, "txtUser1")
    textbox_user_id_second = (By.NAME, "txtUser2")
    textbox_password = (By.NAME, "txtPassword")
    button_login = (By.XPATH, "//input[contains(@onclick, 'CheckSubmit')]")

    def __init__(self, driver):
        super().__init__(driver)
        self.driver.get("https://www.colfinancial.com/ape/Final2/home/HOME_NL_MAIN.asp?p=0")
        self.wait_for_page_to_load(5)

    def login(self, username_f, username_s, password):
        self.wait_for_page_to_load()
        self.driver.find_element(*self.textbox_user_id_first).send_keys(username_f)
        self.driver.find_element(*self.textbox_user_id_second).send_keys(username_s)
        self.driver.find_element(*self.textbox_password).send_keys(password)
        self.driver.find_element(*self.button_login).click()
        self.wait_for_page_to_load()

    def logout(self):
        pass

