from Applications.Trello.references.web.base_api_service import *
from Applications.Trello.references.dto import *


class ApiServiceLabels(BaseApiServiceTrello):

    def initialize(self):
        super(ApiServiceLabels, self).initialize()
        self.request.\
            add_uri_parameter('labels')
