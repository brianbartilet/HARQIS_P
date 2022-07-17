from Core.web import *


class DtoStock(JsonObject):
    code = str
    name = str
    portfolio_percent = str
    market_price = str
    average_price = str
    total_shares = str
    uncommitted_shares = str
    market_value = str
    gain_loss_value = str
    gain_loss_percentage = str
    exchange = str
