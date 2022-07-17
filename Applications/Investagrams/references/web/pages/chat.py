from Applications.Investagrams.references.web.base_page_investagrams import *
from Applications.Investagrams.references.dto.stock import *


class PageInvestegramsStock(BasePageInvestagrams):

    def __init__(self, driver, source_id, **kwargs):
        super().__init__(driver=driver, source_id=source_id, **kwargs)

    #  region Chat Information

    @find_elements(By.XPATH, "//span[@data-ng-bind-html='::entity.Message | stringNewLines']")
    def text_date_chat(self):
        return WebElement

    @find_elements(By.XPATH, "//div[contains(@class, 'investaChat__message--chat')]/span[contains(@data-ng-bind-html, '::entity.Message')]")
    def text_message_chat(self):
        return WebElement

    #  endregion