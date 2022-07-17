from Core.web.api import *


class DtoBoard(JsonObject):
    id = None
    name = None
    desc = None
    desc_data = None
    closed = None
    id_organization = None
    pinned = None
    url = None
    shortUrl = None
    prefs = None
    label_names = None