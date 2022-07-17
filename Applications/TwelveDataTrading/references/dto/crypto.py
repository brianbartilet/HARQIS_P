from Core.web.api import *


class CryptoCurrency(JsonObject):
    symbol = str
    available_exchanges = []
    currency_base = str
    currency_quote = str
