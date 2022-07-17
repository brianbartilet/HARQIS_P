from Core.web.api import *


class DtoTransaction(JsonObject):
    date = ''
    memo = ''
    payee = ''
    value = 0
    running_balance = 0
