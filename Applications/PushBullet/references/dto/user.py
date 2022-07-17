from Core.web.api import *


class DtoPushBulletUser(JsonObject):
    iden = str
    created = float
    modified = float
    email = str
    email_normalized = str
    name = str
    image_url = str
    max_upload_size = int
    referred_count = int
    referrer_iden = str
