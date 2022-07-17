from Applications import *
from Workflows.trading.psei.settings import *


webdriver_config = apps_config['COLFinancial']['webdriver']
wdf = WebDriverFactory


def update_cards_from_open_psei(trello_id, _board: DtoBoard, _list: DtoList, _labels: []):
    webdriver = wdf.get_web_driver_instance(webdriver_config['browser'], **webdriver_config)
    pl = PageInvestagramsLogin(webdriver)
    pl.login(webdriver_config['username_id_one'], webdriver_config['username_id_two'],
             webdriver_config['password'])
    pl.wait_page_to_load(secs=20)

    pp = PagePortfolio(webdriver)
    portfolio = pp.get_portfolio_information()
    pp.driver.close()

    trello_cards_service = ApiServiceCards(trello_id)
    trello_boards_service = ApiServiceBoards(trello_id)
    trello_lists_service = ApiServiceLists(trello_id)

    target_list = DtoList(name=_list.name)
    target_board = DtoBoard(name=_board.name)

    id_list = QList(trello_boards_service.get_board_lists(target_board)) \
        .first(lambda x: x.name == target_list.name).id
    target_list.id = id_list

    current_cards = QList(trello_lists_service.get_all_cards_from_list(target_list))\
        .where(lambda x: QList(x.labels)
        .where(lambda y: y.name == 'PSEI'))

    for stock in portfolio:

        parsed_labels = [l.id for l in QList(trello_boards_service.get_board_labels(target_board))
                         .where(lambda x: x.name in _labels)]

        found = False

        for card in current_cards:

            re_stop = re.search('Stop: (.*) Target:', card.name) \
                .group(1).strip()
            stop = "NA" if re_stop == "NA" else re_stop

            re_target = re.search('Target: (.*)\]\[', card.name) \
                .group(1).strip()
            target = "NA" if re_target == "NA" else re_target


            if stock.stock_code in card.name:
                card_dto = DtoCard(
                    id=card.id,
                    name="""**{0}**[%P/L: {1}  Price: {2}  %Port: {3}  Stop: {4}  Target: {5}][{6}{7}]
                    """.format(stock.stock_code,
                               stock.gain_loss_percentage,
                               stock.market_price,
                               stock.portfolio_percent,
                               stop,
                               target,
                               apps_config['Investagrams']['webdriver']['url'],
                               stock.stock_code).strip(),
                    idList=id_list,
                    idLabels=parsed_labels,

                )
                trello_cards_service.update_card(card_dto)
                found = True
                break
            else:
                continue

        if not found:
            card_dto = DtoCard(
                name="""**{0}**[%P/L: {1}  Price: {2}  %Port: {3}  Stop: {4}  Target: {5}][{6}{7}]
                """.format(stock.stock_code,
                           stock.gain_loss_percentage,
                           stock.market_price,
                           stock.portfolio_percent,
                           "NA",
                           "NA",
                           apps_config['Investagrams']['webdriver']['url'],
                           stock.stock_code).strip(),
                idList=id_list,
                idLabels=parsed_labels,
                pos='top'

            )
            trello_cards_service.add_card(card_dto)
