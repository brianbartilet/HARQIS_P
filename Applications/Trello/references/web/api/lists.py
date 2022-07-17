from Applications.Trello.references.web.base_api_service import *
from Applications.Trello.references.dto import *
from Applications.Trello.references.web.api.cards import ApiServiceCards


class ApiServiceLists(BaseApiServiceTrello):

    def initialize(self):
        super(ApiServiceLists, self).initialize()
        self.request.\
            add_uri_parameter('lists')

    @deserialized(DtoCard)
    def get_all_cards_from_list(self, list: DtoList):
        self.request\
            .add_uri_parameter(list.id)\
            .add_uri_parameter('cards')

        return self.send_get_request(self.request.build())

    def clean_cards_from_list(self, list: DtoList):

        current_cards = self.get_all_cards_from_list(list)

        for card in current_cards:
            ApiServiceCards(self.source_id).archive_card(card)
