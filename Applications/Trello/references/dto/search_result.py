from Applications.Trello.references.dto import *
from Core.web.api import *
from typing import List as list


class DtoSearchResult(JsonObject):
    boards = list[DtoBoard]
    options = None
    cards = None
    organizations = None
    members = None
