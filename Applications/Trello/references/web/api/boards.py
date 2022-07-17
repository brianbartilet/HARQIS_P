from Applications.Trello.references.web.base_api_service import *
from Applications.Trello.references.dto import *
from Applications.Trello.references.web.api.search import ApiServiceSearch


class ApiServiceBoards(BaseApiServiceTrello):

    def initialize(self):
        super(ApiServiceBoards, self).initialize()
        self.request.\
            add_uri_parameter('boards')

    @deserialized(DtoBoard)
    def get_board_by_name(self, board_item: DtoBoard):
        search_api = ApiServiceSearch(source_id=self.source_id)
        target = QList(search_api.get_boards_by_name(board_item.name))\
            .first(lambda x: x.name == board_item.name)

        self.request\
            .add_uri_parameter(target.id)\

        return self.send_get_request(self.request.build())

    @deserialized(DtoCard)
    def get_all_open_cards_from_board(self, board_item: DtoBoard):
        target_board = ApiServiceBoards(source_id=self.source_id).get_board_by_name(board_item)

        short_url = str(target_board.short_url).split('/')[-1]

        self.request\
            .add_uri_parameter(short_url)\
            .add_uri_parameter('cards')

        return self.send_get_request(self.request.build())

    @deserialized(DtoList)
    def get_board_lists(self, board: DtoBoard):
        target_board = ApiServiceBoards(source_id=self.source_id).get_board_by_name(board)
        short_url = str(target_board.short_url).split('/')[-1]

        self.request\
            .add_uri_parameter(short_url)\
            .add_uri_parameter('lists')

        return self.send_get_request(self.request.build())

    @deserialized(DtoLabel)
    def get_board_labels(self, board: DtoBoard, **query):

        target_board = ApiServiceBoards(source_id=self.source_id).get_board_by_name(board)
        board_id = target_board.id

        self.request\
            .add_uri_parameter(board_id)\
            .add_uri_parameter('labels')

        self.request.add_query_strings(**query)

        return self.send_get_request(self.request.build())

