from Applications import *


class BaseApiServiceBPI(ApiService, Generic[T]):

    def __init__(self, source_id, driver: WebDriver):
        super(BaseApiServiceBPI, self)\
            .__init__(app_service_type=ServiceClientType.WEBSERVICE,
                      source_id=source_id,
                      apps_config_data=apps_config)
        self.driver = driver

    def initialize(self):
        self.set_session_data(self.driver)

    def set_session_data(self, driver):
        headers = {
            "User-Agent":
                "Mozilla/5.0 (Windows NT 6.3; WOW64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/44.0.2403.157 Safari/537.36"
        }

        self.client.set_default_headers(headers)
        #s = requests.session()
        #s.headers.update(headers)

        self.client.set_session_cookies(driver.get_cookies())



