from Core.web.api import *


class DtoSaveAccount(JsonObject):
    name = None
    type = 'savings'  # [ checking, savings, creditCard, cash, lineOfCredit, otherAsset, otherLiability ]
    balance = 0


class DtoSaveAccountWrapper(JsonObject):
    account = DtoSaveAccount
