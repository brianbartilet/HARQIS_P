from Applications.Nike.references.web.base_page_nike import *


class PageLoginNike(BasePageNike):

    def __init__(self, driver, source_id, **kwargs):
        super().__init__(driver=driver, source_id=source_id, **kwargs)
        self.driver.get(self.url + '/login')
        self.wait_for_page_to_load()
        self.type_range_delay = kwargs.get('type_range_delay', 0.8)

    @find_element(By.XPATH, "//li[@data-qa='top-nav-user-menu']//button[text()='Sign In']")
    def button_login(self):
        return WebElement

    @find_element(By.XPATH, "//form[@id='nike-unite-loginForm']//input[@name='emailAddress']")
    def dialog_textbox_username(self):
        return WebElement

    @find_element(By.XPATH, "//form[@id='nike-unite-loginForm']//input[@name='password']")
    def dialog_textbox_password(self):
        return WebElement

    @find_element(By.XPATH, "//form[@id='nike-unite-loginForm']//input[@value='SIGN IN']")
    def dialog_textbox_sign_in(self):
        return WebElement

    @find_element(By.XPATH, "//div[@id='nike-unite-error-view']")
    def dialog_error(self):
        return WebElement

    @find_element(By.XPATH, "//div//input[@type='button' and @value='Dismiss this error']")
    def dialog_error_button_dismiss(self):
        return WebElement

    @find_element(By.XPATH, "//div[@class='hf-geomismatch-body']")
    def geo_mismatch_error_body(self):
        return WebElement

    @find_element(By.XPATH, "//div[@class='hf-geomismatch-body']//button[@data-type='click_geoMismatchDismiss']")
    def geo_mismatch_button_dismiss(self):
        return WebElement

    def enter_details(self, username, password):
        self.enter_keys_with_delay(self.dialog_textbox_username(), username)
        self.wait_for_page_to_load(5)
        self.enter_keys_with_delay(self.dialog_textbox_password(), password)
        self.wait_for_page_to_load(5)
        self.dialog_textbox_sign_in().click()
        self.wait_for_page_to_load(1)

    def login(self, username, password):
        self.wait_for_page_to_load(10)

        self.enter_details(username, password)

        try:
            if self.dialog_error().is_displayed():
                self.dialog_error_button_dismiss().click()
                self.log.warning("IP conflict detected. Waiting to change location prompt.")
                self.wait_for_page_to_load(3)
                self.enter_details(username, password)
                self.driver.get(self.url)
                self.wait_for_page_to_load(2)
                self.wait_for_page_to_load()
                self.wait_for_element_to_be_visible_e(self.geo_mismatch_error_body())

                try:
                    self.geo_mismatch_button_dismiss().click()
                    self.wait_for_page_to_load()
                except:
                    log.warning("Unable to find handling for IP conflict.")
        except:
            log.warning("Login Issues encountered")

        self.wait_for_page_to_load(5)

    def logout(self):
        self.menu_account().click()

        link = QList(self.menu_account_dropdown_links())\
            .where(lambda x: (x.text == 'Log Out'))\
            .first()

        link.click()



