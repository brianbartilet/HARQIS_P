from Core.web.api import *


class DtoPushBulletDevice(JsonObject):
    iden = str
    active = bool
    created = float
    modified = float
    icon = str
    nickname = str
    generated_nickname = bool
    manufacturer = str
    model = str
    app_version = int
    fingerprint = str
    key_fingerprint = str
    push_token = str
    has_sms = str
    type = str
    kind = str
    pushable = bool
