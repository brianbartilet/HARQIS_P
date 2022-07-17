from Applications.BPI.references.web.base_page_bpi import *


class PageBPILogin(BasePageBPI):

    @find_element(By.XPATH, "//input[contains(@name, 'username')]")
    def textbox_username(self):
        return WebElement

    @find_element(By.XPATH, "//input[contains(@name, 'password')]")
    def textbox_password(self):
        return WebElement

    @find_element(By.XPATH, "//button[@type='submit' and contains(., 'Login')]")
    def button_login(self):
        return WebElement

    def __init__(self, driver, source_id, **kwargs):
        super().__init__(driver=driver, source_id=source_id, **kwargs)
        self.driver.get(self.url + "/sign-in")

        try:
            self.high_light_element(self.textbox_username())
        except NoSuchElementException:
            self.log.warning('Retrying page load.')
            self.driver.refresh()
            self.wait_for_page_to_load(3)

        self.wait_for_page_to_load()

    def login(self, username, password):
        self.wait_for_page_to_load()

        username_element = self.textbox_username()
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

