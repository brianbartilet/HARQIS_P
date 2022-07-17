from Applications.StrenuousLife.references.web.base_page_strenouos import *


class PageStrenuousLogin(BasePageStrenousLife):

    @find_element(By.ID, 'user_login')
    def textbox_username(self):
        return WebElement

    @find_element(By.ID, 'user_pass')
    def textbox_password(self):
        return WebElement

    @find_element(By.ID, 'wp-submit')
    def button_login(self):
        return WebElement

    def __init__(self, driver, source_id, **kwargs):
        super().__init__(driver=driver, source_id=source_id, **kwargs)
        self.driver.get(self.url + "/wp-login.php")
        self.wait_for_page_to_load()

    def login(self, username, password):
        self.wait_for_page_to_load()

        username_element = self.textbox_username()
        username_element.send_keys(username)

        password_element = self.textbox_password()
        password_element.send_keys(password)

        button_login = self.button_login()
        button_login.click()
        self.wait_for_page_to_load()


    def logout(self):
        pass

