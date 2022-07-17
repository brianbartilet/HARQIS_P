from Core.web.api import *


class DtoAnalysisTechnical(JsonObject):
    support_1 = float
    support_2 = float
    resistance_1 = float
    resistance_2 = float
    week_to_date = float
    month_to_date = float
    year_to_date = float

    moving_averages = dict
    indicators = dict


class DtoAnalysisFundamental(JsonObject):
    price_to_book_value = float
    return_on_equity = float
    week_hi_52 = float
    week_lo_52 = float
    price_earnings_ratio = float


class DtoStockInvestagrams(JsonObject):
    name = str
    last_price = float
    change = float
    change_percent = float
    volume = int
    value = float
    year_to_date = float
    open = float
    low = float
    high = float
    date = float
    average_price = float
    previous_close = float
    sector = str
    sub_sector = str
    net_foreign = str
    volatility = str
    nfb_1 = str
    nfb_5 = str

    historical = []
    fundamental = DtoAnalysisFundamental
    technical = DtoAnalysisTechnical

