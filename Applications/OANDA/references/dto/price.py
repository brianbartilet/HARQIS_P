from Core.web.api import *


class DtoPrice(JsonObject):
    asks = []
    bids = []
    closeoutAsk = None
    closeoutBid = None
    data = None
    instrument = None
    quoteHomeConversionFactors = None
    status = None
    time = None
    type = None
    unitsAvailable = None
