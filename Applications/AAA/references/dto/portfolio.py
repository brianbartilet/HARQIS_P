from Business.trading.models import *


class DtoPortfolioItemAAA(JsonObject):
    symbol = str
    quantity = int
    sell_pending = int
    buy_pending = int
    available_quantity = int
    average_cost = float
    market_value = float
    gain_loss_value = float
    gain_loss_percentage = float
    portfolio_percentage = float
    market_price = float
    description = str
    portfolio_id = str
    average_price = float
    cost_value = float
    currency = str
    exchange = str
