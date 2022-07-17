from Core.web.api import *
from Applications.TwelveDataTrading.references.dto.timeframe import EnumTimeframe


class TechnicalIndicator(JsonObject):
    enable = str
    full_name = str
    type = str
    overlay = bool
    parameters = {}
    output_values = {}
    description = str


class IndicatorParameters(JsonObject):
    symbol = str
    interval = EnumTimeframe
    exchange = str
    country = str
    time_period = int
    type = str
    outputsize = int
    format = str
    dp = int
    timezone = str
    start_date = str
    end_date = str
