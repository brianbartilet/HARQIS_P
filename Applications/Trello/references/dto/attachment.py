from Core.web.api import *


class DtoAttachment(JsonObject):
    name = str
    file = str
    mimeType = str
    url = str
    setCover = True
    fileName = None
    isUpload = bool