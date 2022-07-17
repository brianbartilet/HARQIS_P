from behave import *

from Applications.Trello.references.web.api import *
from Applications.Trello.references.dto import *
from Applications.load_config import *

from Core.web.api import *


@step("I have an existing board")
def step_run_api(context):
    client_config = apps_config['Trello']['client']

    context.client = BaseApiClient(**client_config)

    board_target = DtoBoard(
        name="Daily Dashboard Tests"
    )

    context.board = board_target


@step("I view all available cards")
def step_run_api(context):

    search_api = ApiServiceSearch(context.client)
    boards_api = ApiServiceBoards(context.client)
    context.boards = QList(search_api.get_boards_by_name(context.board.name))
    context.cards = boards_api.get_all_open_cards_from_board(context.board)


@step("I can view all my cards")
def step_run_api(context):
    check = ApiServiceSearch(context.client).verify
    check.common.assert_that(len(context.cards), check.common.greater_than_or_equal_to(0))


@step("I have an existing list")
def step_run_api(context):
    list_target = DtoList(
        name="CURRENT"
    )
    context.list = list_target


@step("I add a card with the following items to the {position} of list")
def step_run_api(context, position):

    cards_api = ApiServiceCards(context.client)
    boards_api = ApiServiceBoards(context.client)

    target_board = context.board
    target_list = context.list

    card_dto = DtoCard(
        name="DtoCard " + fake.uuid4(),
        idList=QList(boards_api.get_board_lists(target_board)).first(lambda x: x.name == target_list.name).id,
        pos=position

    )
    context.card = cards_api.add_card(card_dto)



@step("my card is added successfully")
def step_run_api(context):
    check = ApiServiceCards(context.client).verify
    check.common.assert_that(len(context.card.id), check.common.greater_than(0))

