from Core.web.api import *


class DtoPushBulletPush(JsonObject):
    iden = str
    active = bool
    created = float
    date = float
    type = str
    dismissed = bool
    guid = str
    direction = str
    sender_iden = str
    sender_email = str
    sender_email_normalized = str
    sender_name = str
    receiver_iden = str
    receiver_email = str
    receiver_email_normalized = str
    target_device_iden = str
    source_device_iden = str
    client_iden = str
    channel_iden = str
    awake_app_guids = []
    title = str
    body = str
    url = str
    file_name = str
    file_type = str
    file_url = str
    image_url = str
    image_width = int
    image_height = int