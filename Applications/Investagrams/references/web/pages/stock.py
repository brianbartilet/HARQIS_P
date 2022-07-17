from Applications.Investagrams.references.web.base_page_investagrams import *
from Applications.Investagrams.references.dto.stock import *

CLEAN_CHARS = ['%', '(', ')', ',']


class PageInvestegramsStock(BasePageInvestagrams):

    def __init__(self, driver, source_id, **kwargs):
        super().__init__(driver=driver, source_id=source_id, **kwargs)

    #  region Stock Information Basic

    #@find_element(By.ID, 'lblStockLatestLastPrice')
    @find_element(By.XPATH, '//span[@data-ng-class="ViewStockPage.Data.Stock.LatestStockHistory.LastClass"]')
    def text_last_price(self):
        return WebElement

    #@find_element(By.ID, 'lblStockLatestChange')
    @find_element(By.XPATH, '(//span[contains(@class,"stockprice")]//span)[1]')
    def text_change(self):
        return WebElement

    #@find_element(By.ID, 'lblStockLatestChangePerc')
    @find_element(By.XPATH, '(//span[contains(@class,"stockprice")]//span)[2]')
    def text_change_percent(self):
        return WebElement

    #@find_element(By.ID, 'lblStockLatestOpen')
    @find_element(By.XPATH, "((//table[@class='table stock-information-table'])[1]//td)[2]")
    def text_open(self):
        return WebElement

    #@find_element(By.ID, 'lblStockLatestLow')
    @find_element(By.XPATH, "((//table[@class='table stock-information-table'])[1]//td)[4]")
    def text_low(self):
        return WebElement

    #@find_element(By.ID, 'lblStockLatestHigh')
    @find_element(By.XPATH, "((//table[@class='table stock-information-table'])[1]//td)[6]")
    def text_high(self):
        return WebElement

    #@find_element(By.ID, 'lblStockLatestAverage')
    @find_element(By.XPATH, "((//table[@class='table stock-information-table'])[1]//td)[8]")
    def text_average_price(self):
        return WebElement

    #@find_element(By.XPATH, "((//table[@class='table stock-information-table'])[1]//td)[8]")
    @find_element(By.XPATH, "((//table[@class='table stock-information-table'])[1]//td)[10]")
    def text_sector(self):
        return WebElement

    #@find_element(By.ID, 'lblStockLatestClose')
    @find_element(By.XPATH, "((//table[@class='table stock-information-table'])[2]//td)[2]")
    def text_previous_close(self):
        return WebElement

    #@find_element(By.ID, 'lblStockLatestVolume')
    @find_element(By.XPATH, "((//table[@class='table stock-information-table'])[2]//td)[4]")
    def text_volume(self):
        return WebElement

    #@find_element(By.XPATH, "((//table[@class='table stock-information-table'])[3]//span)[5]")
    @find_element(By.XPATH, "((//table[@class='table stock-information-table'])[2]//td)[10]")
    def text_sub_sector(self):
        return WebElement

    @find_element(By.XPATH, "((//table[@class='table stock-information-table'])[3]//td)[4]")
    def text_week_hi_52(self):
        return WebElement

    @find_element(By.XPATH, "((//table[@class='table stock-information-table'])[3]//td)[2]")
    def text_week_lo_52(self):
        return WebElement

    #  endregion

    #  region Fundamental

    @find_element(By.XPATH, "(//div[@id='FundamentalAnalysisContent']//tr//td)[8]")
    def text_return_on_equity(self):
        return WebElement

    @find_element(By.XPATH, "(//div[@id='FundamentalAnalysisContent']//tr//td)[4]")
    def text_price_to_book_value(self):
        return WebElement

    #  endregion

    #  region Technical

    @find_element(By.XPATH, "(//div[@id='TechnicalAnalysisContent']//tr//td)[2]")
    def text_support_1(self):
        return WebElement

    @find_element(By.XPATH, "(//div[@id='TechnicalAnalysisContent']//tr//td)[8]")
    def text_support_2(self):
        return WebElement

    @find_element(By.XPATH, "(//div[@id='TechnicalAnalysisContent']//tr//td)[4]")
    def text_resistance_1(self):
        return WebElement

    @find_element(By.XPATH, "(//div[@id='TechnicalAnalysisContent']//tr//td)[10]")
    def text_resistance_2(self):
        return WebElement

    @find_element(By.XPATH, "(//div[@id='TechnicalAnalysisContent']//tr//td)[14]")
    def text_week_to_date(self):
        return WebElement

    @find_element(By.XPATH, "(//div[@id='TechnicalAnalysisContent']//tr//td)[16]")
    def text_month_to_date(self):
        return WebElement

    @find_element(By.XPATH, "(//div[@id='TechnicalAnalysisContent']//tr//td)[18]")
    def text_year_to_date(self):
        return WebElement

    #  region Moving Averages

    @find_element(By.XPATH, "(//div[@id='TechnicalAnalysisContent']//tr//td)[23]")
    def text_ma20_simple(self):
        return WebElement

    @find_element(By.XPATH, "(//div[@id='TechnicalAnalysisContent']//tr//td)[26]")
    def text_ma50_simple(self):
        return WebElement

    @find_element(By.XPATH, "(//div[@id='TechnicalAnalysisContent']//tr//td)[29]")
    def text_ma100_simple(self):
        return WebElement

    @find_element(By.XPATH, "(//div[@id='TechnicalAnalysisContent']//tr//td)[32]")
    def text_ma200_simple(self):
        return WebElement

    @find_element(By.XPATH, "(//div[@id='TechnicalAnalysisContent']//tr//td)[24]")
    def text_ma20_exponential(self):
        return WebElement

    @find_element(By.XPATH, "(//div[@id='TechnicalAnalysisContent']//tr//td)[27]")
    def text_ma50_exponential(self):
        return WebElement

    @find_element(By.XPATH, "(//div[@id='TechnicalAnalysisContent']//tr//td)[30]")
    def text_ma100_exponential(self):
        return WebElement

    @find_element(By.XPATH, "(//div[@id='TechnicalAnalysisContent']//tr//td)[33]")
    def text_ma200_exponential(self):
        return WebElement

    #  endregion

    #  region Indicators

    @find_element(By.XPATH, "(//div[@id='TechnicalAnalysisContent']//tr//td)[38]")
    def text_rsi(self):
        return WebElement

    @find_element(By.XPATH, "(//div[@id='TechnicalAnalysisContent']//tr//td)[41]")
    def text_macd(self):
        return WebElement

    @find_element(By.XPATH, "(//div[@id='TechnicalAnalysisContent']//tr//td)[44]")
    def text_atr(self):
        return WebElement

    @find_element(By.XPATH, "(//div[@id='TechnicalAnalysisContent']//tr//td)[47]")
    def text_cci(self):
        return WebElement

    @find_element(By.XPATH, "(//div[@id='TechnicalAnalysisContent']//tr//td)[50]")
    def text_sts(self):
        return WebElement

    @find_element(By.XPATH, "(//div[@id='TechnicalAnalysisContent']//tr//td)[53]")
    def text_williams(self):
        return WebElement

    @find_element(By.XPATH, "(//div[@id='TechnicalAnalysisContent']//tr//td)[56]")
    def text_volume_sma(self):
        return WebElement

    @find_element(By.XPATH, "(//div[@id='TechnicalAnalysisContent']//tr//td)[59]")
    def text_candlestick(self):
        return WebElement

    #  endregion

    #  endregion

    #  region Historical Data

    @find_element(By.XPATH, "//div[@id='HistoricalDataContent']//div[contains(@class,'table-responsive-md stock-panel-limit')]//table")
    def table_historical_data(self):
        return WebElement

    #  endregion

    def get_stock_information(self, stock_name: str, include_history=False, days_history=100):
        self.driver.get(self.url + "/Stock/{0}".format(stock_name.upper()))
        self.wait_for_page_to_load(1)

        text_elements_method = QList(dir(self)).where(lambda x: x.startswith('text_'))

        scrape = {}
        for method in text_elements_method:
            try:
                scrape[method.replace('text_', '')] = getattr(self, method)().text
            except NoSuchElementException:
                log.warning("Cannot find element from method {0}".format(method))
                scrape[method.replace('text_', '')] = None
                continue

        historical = []
        if include_history:
            params = ['date', 'last_price', 'change', 'change_percent', 'open', 'low', 'high', 'volume', 'net_foreign']
            data = self.get_table_body_rows(self.table_historical_data())[0:days_history]
            for row in data:
                text = []
                for cell in row:
                    text.append(cell.text)
                dto = DtoStockInvestagrams(convert_kwargs=True,
                                           clean_chars=CLEAN_CHARS,
                                           **dict(zip(params, text)))
                historical.append(dto)

        dto = DtoStockInvestagrams(convert_kwargs=True,
                                   clean_chars=CLEAN_CHARS,
                                   name=stock_name,
                                   **scrape)

        dto_fundamental = DtoAnalysisFundamental(convert_kwargs=True,
                                                 clean_chars=CLEAN_CHARS,
                                                 **scrape)
        dto_technical = DtoAnalysisTechnical(convert_kwargs=True,
                                             clean_chars=CLEAN_CHARS,
                                             **scrape)

        dto.fundamental = dto_fundamental
        dto.technical = dto_technical
        dto.historical = historical

        return dto