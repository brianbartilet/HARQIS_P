from Core.web.api import *


class DtoCard(JsonObject):
    id = None
    badges = None
    checkItemStates = None
    closed = False
    dateLastActivity = None
    desc = None
    descData = None
    due = None  # YYYY-MM-DDTHH:mm:ssZ ISO8601
    dueComplete = None
    email = None
    idAttachmentCover = None
    idCardSource = None
    idChecklists = []
    idLabels = []
    id_labels = []
    idMembers = []
    idMembersVoted = []
    id_short = None
    idList = None
    name = None
    pos = None
    shortLink = None
    shortUrl = None
    url = None
    subscribed = None
    manualCoverAttachment = None
    labels = []
