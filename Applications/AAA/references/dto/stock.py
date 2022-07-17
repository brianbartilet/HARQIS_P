from Core.web.api import *


class DtoStockAAA(JsonObject):
    symbol = str
    description = str
    last_traded = str
    bid_qty = str
    bid = str
    offer = str
    offer_qty = str
    volume = str
    value = str
    change = str
    change_percent = str
    prev_close = str
    open = str
    high = str
    low = str
    trades = str
    cash_map = str
    wk_52_hi = str
    wk_52_lo = str
