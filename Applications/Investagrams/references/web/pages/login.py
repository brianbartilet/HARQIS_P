from Applications.Investagrams.references.web.base_page_investagrams import *


class PageInvestagramsLogin(BasePageInvestagrams):

    @find_element(By.XPATH, "//input[contains(@placeholder, 'Email Address')]")
    def textbox_email_address(self):
        return WebElement

    @find_element(By.XPATH, "//input[contains(@placeholder, 'Password')]")
    def textbox_password(self):
        return WebElement

    @find_element(By.XPATH, "//button[contains(., 'Log in')]")
    def button_login(self):
        return WebElement

    def __init__(self, driver, source_id, **kwargs):
        super().__init__(driver=driver, source_id=source_id, **kwargs)
        self.driver.get(self.url + "/Login")
        self.wait_for_page_to_load()

    def login(self, username, password):
        self.wait_for_page_to_load()

        username_element = self.textbox_email_address()
        self.wait_for_element_to_be_stale_e(username_element)
        username_element.send_keys(username)

        password_element = self.textbox_password()
        self.wait_for_element_to_be_stale_e(password_element)
        password_element.send_keys(password)

        button_login = self.button_login()
        self.wait_for_element_to_be_stale_e(button_login)
        button_login.click()
        self.wait_page_to_load()

    def logout(self):
        pass

