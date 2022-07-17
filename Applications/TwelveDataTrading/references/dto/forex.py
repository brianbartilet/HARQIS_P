from Core.web.api import *


class ForexPair(JsonObject):
    symbol = str
    currency_group = str
    currency_base = str
    currency_quote = str
