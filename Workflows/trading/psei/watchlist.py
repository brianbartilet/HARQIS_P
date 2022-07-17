from Applications import *

tolerance = 0.05


def update_watchlist_items_psei(trello_id, psei_id, notifications_id, board: DtoBoard, list: DtoList, labels: [], **kwargs):

    trello_cards_service = ApiServiceCards(trello_id)
    trello_boards_service = ApiServiceBoards(trello_id)
    trello_lists_service = ApiServiceLists(trello_id)

    target_list = DtoList(name=list.name)
    target_board = DtoBoard(name=board.name)

    id_list = QList(trello_boards_service.get_board_lists(target_board)) \
        .first(lambda x: x.name == target_list.name).id
    target_list.id = id_list

    current_cards = QList(trello_lists_service.get_all_cards_from_list(target_list))\
        .where(lambda x: QList(x.labels)
        .where(lambda y: y.name == 'PSEI'))

    psei_price_service = ApiServiceStock(psei_id)
    for card in current_cards:


        title = card.name
        short_name = re.search('\\*\\*(.*)\\*\\*', title)\
            .group(1).strip()

        try:
            price_info = psei_price_service.get_stock_price(short_name)
        except:
            price_info = None

        re_entry = re.search('Entry: (.*) Stop:', title) \
            .group(1).strip()
        entry = "NA" if re_entry == "NA" else re_entry

        re_stop = re.search('Stop: (.*) Target:', title) \
            .group(1).strip()
        stop = "NA" if re_stop == "NA" else re_stop

        re_target = re.search('Target: (.*)\]\[', title) \
            .group(1).strip()
        target = "NA" if re_target == "NA" else re_target


        labels_ = []
        for l in labels:
            labels_.append(l)

        try:

            percent_gain = (float(target) - float(entry))/float(entry)
            percent_loss = (float(entry) - float(stop))/float(entry)
            risk_reward = str(round(percent_gain/percent_loss, 2))

            current_price = price_info[0].price.amount
            if current_price - (current_price * tolerance) <= float(entry) \
                    <= current_price + (current_price * tolerance):
                labels_.append("!!!")

                notification = CurlServicePushNotifications(notifications_id)
                notification.send_notification("Entry Alert [" + short_name + "] Price: "
                                               + str(current_price) + " RR: " + str(risk_reward))

        except:
            risk_reward = "NA"

        parsed_labels = [l.id for l in QList(trello_boards_service.get_board_labels(target_board))
            .where(lambda x: x.name in labels_)]

        if price_info is not None:
            stock = price_info[0]
            card_dto = DtoCard(
                id=card.id,
                name="""**{0}**[%Change: {1}  RR: {2}  Price: {3}  Entry: {4}  Stop: {5}  Target: {6}][{7}{8}]
                """.format(stock.symbol,
                           stock.percent_change,
                           risk_reward,
                           stock.price.amount,
                           entry,
                           stop,
                           target,
                           apps_config['Investagrams']['webdriver']['url'],
                           stock.symbol)
                    .strip(),
                idList=id_list,
                idLabels=parsed_labels,
                pos='bottom'

            )
            trello_cards_service.update_card(card_dto)


