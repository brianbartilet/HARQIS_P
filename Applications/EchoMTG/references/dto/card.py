from Core.web.api import *
from datetime import datetime


class DtoEchoMTGCard(JsonObject):
    emid = None
    mid = None
    quantity = 1
    language = 'EN'
    acquired_price = None
    acquired_date = datetime.today().strftime('%m-%d-%Y')
    condition = 'NM'
    foil = 0


class DtoDelverLensMTGCard(JsonObject):
    multiverseid = None
    foil = None
    name = None
