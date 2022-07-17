from Applications.Trello.references.web.base_api_service import *
from Applications.Trello.references.dto import *


class ApiServiceSearch(BaseApiServiceTrello):

    def initialize(self):
        super(ApiServiceSearch, self).initialize()
        self.request.\
            add_uri_parameter('search')

    @deserialized(DtoBoard, child='boards')
    def get_boards_by_name(self, search_string: str):
        self.request\
            .add_query_string('query', search_string)\
            .add_query_string('idBoards', 'mine')\

        return self.send_get_request(self.request.build())







