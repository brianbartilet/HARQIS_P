from Core.web.api import *


class DtoPrice(JsonObject):
    amount = None
    currency = None


class DtoPseStock(JsonObject):
    name = None
    percent_change = None
    price = DtoPrice
    symbol = None
    volume = None

