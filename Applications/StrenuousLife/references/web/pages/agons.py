from Applications.StrenuousLife.references.web.base_page_strenouos import *
from Applications.StrenuousLife.references.dto.agon import DtoAgon


class PageAgons(BasePageStrenousLife):

    @find_elements(By.XPATH, "//a[(@class='ld-item-name ld-primary-color-hover') and (contains(@href, 'requirements'))]")
    def links_agons(self):
        return WebElement

    @find_element(By.XPATH, "//button[contains(text(),'Run') and @title='Run Screener']")
    def button_run(self):
        return WebElement

    @find_element(By.XPATH, "//p//b")
    def text_bold_agon(self):
        return WebElement

    @find_element(By.XPATH, "//div[contains(@id, 'ld-tab-content-')]")
    def container_text_complete_agon(self):
        return WebElement

    def __init__(self, driver, source_id, **kwargs):
        super().__init__(driver=driver, source_id=source_id, **kwargs)
        self.driver.get(self.url + "/badges/weekly-agon/")

    def get_all_agons(self) -> List[DtoAgon]:
        agon_elements = self.links_agons()
        ret = []

        for agon in agon_elements:
            dto = DtoAgon(
                week=agon.text,
                link=agon.get_attribute('href'),
            )
            ret.append(dto)

        return ret

    def get_latest_agon_info(self):
        agon_latest = QList(self.get_all_agons()).last()
        self.driver.get(agon_latest.link)
        self.wait_for_page_to_load()

        agon_latest.name = self.text_bold_agon().text
        agon_latest.description = self.container_text_complete_agon().text

        return agon_latest
