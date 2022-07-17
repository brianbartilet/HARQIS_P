from Core.web.api import *


class DtoStatementTransaction(JsonObject):
    payee = str
    memo = str
    amount = str
    date = str

