from Core.web.api import *


class DtoSaveSubTransaction(JsonObject):
    amount = int
    payee_id = str
    payee_name = str
    category_id = str
    memo = str


class DtoSaveTransaction(JsonObject):
    account_id = ''
    date = str  # ISO format (e.g. 2016-12-01)
    amount = 0
    payee_id = str
    payee_name = str
    category_id = str
    memo = str
    cleared = str  # [ cleared, uncleared, reconciled ]
    approved = False
    flag_color = str  # [ red, orange, yellow, green, blue, purple, ]
    import_id = str
    subtransactions = DtoSaveSubTransaction


class DtoUpdateTransaction(DtoSaveTransaction):
    id = str


class DtoSaveTransactionsWrapper(JsonObject):
    transaction = DtoSaveTransaction
    transactions = []
