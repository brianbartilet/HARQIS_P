from Applications.Google.references.web.base_api_service import *
from Applications.Google.references.dto import *
from datetime import datetime


class ApiServiceGoogleAuth(BaseApiServiceGoogle):

    def __init__(self, source_id):
        super(ApiServiceGoogleAuth, self).__init__(source_id)
        self.initialize()

    def initialize(self):
        super(ApiServiceGoogleAuth, self).initialize()



