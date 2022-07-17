from Applications.AAA.references.web.base_page_aaa import *


class PageAAALogin(BasePageAAAEquities):

    def __init__(self, driver, source_id, **kwargs):
        super().__init__(driver=driver, source_id=source_id, **kwargs)
        self.driver.get(self.parameters['url'])
        self.wait_for_page_to_load(5)

    @find_element(By.ID, 'txtUsername')
    def textbox_username(self):
        return WebElement

    @find_element(By.ID, 'txtPassword')
    def textbox_password(self):
        return WebElement

    @find_element(By.ID, 'btnLogin')
    def button_login(self):
        return WebElement

    @find_elements(By.ID, 'message-box')
    def dialog_password(self):
        return []

    @find_element(By.XPATH, "//div[@id='message-box']//button[text()='OK']")
    def button_dialog_password_ok(self):
        return WebElement

    def login(self, **kwargs):
        username = kwargs.get('username', self.parameters['username'])
        password = kwargs.get('password', self.parameters['password'])

        self.wait_for_page_to_load(3)
        self.textbox_username().clear()
        self.textbox_username().send_keys(Keys.CONTROL + 'A' + Keys.BACKSPACE)
        self.textbox_username().send_keys(username)
        self.wait_for_page_to_load(3)
        self.textbox_password().clear()
        self.textbox_password().send_keys(Keys.CONTROL + 'A' + Keys.BACKSPACE)
        self.textbox_password().send_keys(password)
        self.wait_for_page_to_load(3)
        self.button_login().click()
        self.wait_for_page_to_load(3)

        if len(self.dialog_password()) > 0:
            try:
                self.button_dialog_password_ok().click()
            except Exception:
                pass

        self.wait_for_page_to_load(time_sec=20)