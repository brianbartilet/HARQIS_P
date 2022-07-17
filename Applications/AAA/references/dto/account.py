from Business.trading.models import *


class DtoAccountAAA(JsonObject):
    cash_balance = float
    available_cash = float
    pending_cash = float
    available_to_withdraw = float
    unsettled_sales = float
    payable_amount = float
    od_limit = float
    portfolio_value = float
    total_portfolio_value = float

