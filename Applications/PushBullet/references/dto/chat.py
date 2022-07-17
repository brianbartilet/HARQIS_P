from Core.web.api import *


class DtoPushBulletWithChat(JsonObject):
    email = str
    email_normalized = str
    iden = str
    image_url = str
    type = str
    name = str


class DtoPushBulletChat(JsonObject):
    iden = str
    active = bool
    created = float
    modified = float
    muted = bool
    wth = DtoPushBulletWithChat
