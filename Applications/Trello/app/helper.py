from Applications.Trello.references import *


def get_board_data(trello_id,
                   board_name: str,
                   list_name: str,
                   filter_labels_list: [] = None):

    service_trello_boards = ApiServiceBoards(trello_id)
    service_trello_lists = ApiServiceLists(trello_id)

    target_list = DtoList(name=list_name)
    target_board = DtoBoard(name=board_name)

    id_list = QList(service_trello_boards.get_board_lists(target_board)) \
        .first(lambda x: x.name == target_list.name).id

    target_list.id = id_list
    cards = service_trello_lists.get_all_cards_from_list(target_list)

    if filter_labels_list is not None:
        parsed_labels = [l.id for l in QList(service_trello_boards.get_board_labels(target_board))
            .where(lambda x: x.name in filter_labels_list)]
        cards = QList(cards).where(lambda x: len(set(x.id_labels).intersection(parsed_labels)) > 0)

    return cards, target_list, target_board


def parse_configuration_from_desc(description_raw: str, match_index=0) -> dict:

    try:
        match = re.findall(r'```(.*?)```', description_raw, re.DOTALL)[match_index]
        config = yaml.load(match)
    except:
        log.warning("Cannot process embedded configuration")
        config = None

    return config


def move_cards_with_title_to_target_list(trello_id,
                                         board_name: str,
                                         source_list_name: str,
                                         target_list_name: str,
                                         contains_text_input: str):

    cs, source_list, bs = get_board_data(trello_id=trello_id,
                                         board_name=board_name,
                                         list_name=source_list_name)

    ct, target_list, bc = get_board_data(trello_id=trello_id,
                                         board_name=board_name,
                                         list_name=target_list_name)

    cards_search = QList(cs).where(lambda x: contains_text_input in x.name)
    if len(cards_search) > 0:
        cards_search.reverse()

    trello_cards_service = ApiServiceCards(trello_id)
    for card_search in cards_search:

        #  region Move Cards To Closed

        card_dto = DtoCard(
            id=card_search.id,
            idList=target_list.id,
            pos='top'
        )

        trello_cards_service.update_card(card_dto)

        #  endregion
