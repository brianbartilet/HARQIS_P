from Core.web.api import *


class DtoAccountProperties(JsonObject):
    mt4AccountID = None
    id = None
    tags = None


class DtoAccountDetails(JsonObject):
    guaranteedStopLossOrderMode = None
    id = None
    balance = None
    openTradeCount = None
    openPositionCount = None
    pendingOrderCount = None
    trades = None
    positions = None
    orders = None


class DtoAccountInstruments(JsonObject):
    name = None
    type = None
    displayName = None
    pipLocation = None
    displayLocation = None
    tradeUnitsPrecision = None
    minimumTradeSize = None
    maximumTrailingStopDistance = None
    minimumTrailingStopDistance = None
    maximumPositionSize = None
    maximumOrderUnits = None
    marginRate = None
    guaranteedStopLossOrderMode = None
    tags = []
    financing = {}