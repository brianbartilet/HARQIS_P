from Applications import *
from Workflows.trading.forex.settings import *


@app.task()
def move_cards_to_closed_trades(trello_id: str,
                                oanda_id: str,
                                notifications_id: str,
                                closed_trades_board_name: str,
                                closed_trades_list_name: str,
                                open_trades_list_name: str,
                                labels_list: [],
                                **kwargs):

    #  region Get closed trades

    service_oanda_account = ApiServiceAccount(oanda_id)
    account_use = QList(service_oanda_account.get_account_info().accounts)\
        .where(lambda x: x.mt4AccountID == service_oanda_account.parameters['mt4AccountID'])\
        .first()

    open_trades_current_cards, id_list, target_board = \
        get_board_data(trello_id, closed_trades_board_name, open_trades_list_name)

    service_trello_boards = ApiServiceBoards(trello_id)
    parsed_labels = [l.id for l in
                     QList(service_trello_boards.get_board_labels(target_board)).where(lambda x: x.name in labels_list)]

    filter_open_trades_current_cards = QList(open_trades_current_cards)\
        .where(lambda x: len(set(x.id_labels).intersection(parsed_labels)) > 0)

    closed = []
    service_oanda_autochartist = ApiServiceOrders(oanda_id)
    service_oanda_trades = ApiServiceTrades(oanda_id)
    for open_trade_card in filter_open_trades_current_cards:
        match = re.search(r'```(.*?)```', open_trade_card.desc, re.DOTALL).group(1)
        try:
            config = yaml.load(match)
        except:
            log.warning("Cannot process embedded configuration")
            continue
        order = service_oanda_autochartist.get_orders(account_use.id,
                                                      ids='{0}'.format(config['TRADE']['trade_id']),
                                                      state=EnumTradeStateFilter.ALL.value)
        try:
            target = QList(order['orders']).first()
            trade_opened_id = target['tradeOpenedID']
        except:
            log.warning("Trade is still not closed: {0}".format(config['TRADE']['trade_id']))
            target = None
            trade_opened_id = config['TRADE']['trade_id']

        closed_trades = service_oanda_trades.get_trades_from_account(account_id=account_use.id,
                                                                     state=EnumTradeStateFilter.CLOSED.value,
                                                                     ids='{0}'.format(trade_opened_id))
        if len(closed_trades) == 0:
            log.warning("Trade is still not closed: {0}".format(trade_opened_id))
            continue

        closed_trade = QList(closed_trades).first()
        closed.append((open_trade_card, target, closed_trade))

    #  endregion

    service_oanda_account = ApiServiceAccount(source_id=oanda_id)

    #  region Move Cards

    trello_cards_service = ApiServiceCards(trello_id)
    closed_trades_current_cards, id_list_closed, target_board = \
        get_board_data(trello_id, closed_trades_board_name, closed_trades_list_name)

    for card_to_close, og_order, closed_trade in closed:

        #  region Move Cards To Closed

        card_dto = DtoCard(
            id=card_to_close.id,
            name=card_to_close.name + "[P/L: {0}]".format(closed_trade.realized_pl),
            idList=id_list_closed.id,
            id_labels=parsed_labels,
            pos='top',
            desc=card_to_close.desc + str_fx_closed_card_description.format(
                closed_trade.price,
                closed_trade.realized_pl,
                closed_trade.closing_transaction_ds[0],
                closed_trade.financing,
                closed_trade.close_time

            )
        )

        trello_cards_service.update_card(card_dto)

        #  endregion

        #  region Send notification

        notification = CurlServicePushNotifications(notifications_id)
        try:
            notification.send_notification("CLOSED: {0} {1}".format(closed_trade.realized_pl, card_to_close.name))
        except:
            log.warning("Error encountered in push notifications.")

        #  endregion

    #  endregion


@app.task()
def move_cancelled_cards_to_closed_trades(trello_id: str,
                                          oanda_id: str,
                                          notifications_id: str,
                                          pending_trades_board_name: str,
                                          pending_trades_list_name: str,
                                          closed_trades_list_name: str,
                                          labels_list: [],
                                          **kwargs):

    #  region Get open trades

    service_oanda_account = ApiServiceAccount(oanda_id)
    account_use = QList(service_oanda_account.get_account_info().accounts)\
        .where(lambda x: x.mt4AccountID == service_oanda_account.parameters['mt4AccountID'])\
        .first()

    pending_trades_current_cards, id_list, target_board = \
        get_board_data(trello_id, pending_trades_board_name, pending_trades_list_name)

    service_trello_boards = ApiServiceBoards(trello_id)
    parsed_labels = [l.id for l in QList(service_trello_boards.get_board_labels(target_board))
        .where(lambda x: x.name in labels_list)]

    filter_pending_trades_current_cards = QList(pending_trades_current_cards)\
        .where(lambda x: len(set(x.id_labels).intersection(parsed_labels)) > 0)

    cancelled_trading = []
    service_oanda_autochartist = ApiServiceOrders(oanda_id)

    manual_closed_already_open = False
    for pending_trade_card in filter_pending_trades_current_cards:
        match = re.search(r'```(.*?)```', pending_trade_card.desc, re.DOTALL).group(1)
        try:
            config = yaml.load(match)
        except:
            log.warning("Cannot process embedded configuration")
            continue
        order = service_oanda_autochartist.get_orders(account_use.id,
                                                      ids='{0}'.format(config['TRADE']['trade_id']),
                                                      state=EnumTradeStateFilter.ALL.value,
                                                      count=500)
        target = QList(order['orders']).first()
        if target['state'] == EnumOrderState.CANCELLED.name:
            cancelled_trading.append((pending_trade_card, target, None))
        else:
            try:
                trade_opened_id = target['tradeOpenedID']
            except KeyError:
                log.warning("Trade is now open: {0}".format(target['id']))
                continue

            service_oanda_trades = ApiServiceTrades(oanda_id)
            trades_closed = service_oanda_trades.get_trades_from_account(account_id=account_use.id,
                                                                        state=EnumTradeStateFilter.CLOSED.value,
                                                                        ids='{0}'.format(trade_opened_id))
            if len(trades_closed) > 0:
                trade_closed = QList(trades_closed).first()
                cancelled_trading.append((pending_trade_card, target, trade_closed))
                manual_closed_already_open = True

    #  endregion

    #  region Move Cards

    service_oanda_account = ApiServiceAccount(source_id=oanda_id)
    trello_cards_service = ApiServiceCards(trello_id)
    closed_trades_current_cards, id_list_close, target_board = \
        get_board_data(trello_id, pending_trades_board_name, closed_trades_list_name)

    tags = ['MANUAL_CLOSED_TRADE',] if manual_closed_already_open else ['CANCELLED']
    parsed_labels = [l.id for l in QList(service_trello_boards.get_board_labels(target_board))
        .where(lambda x: x.name in tags)]

    for card_to_close, og_order, closed_trade in cancelled_trading:

        #  region Move Cards To Closed

        if manual_closed_already_open:
            try:
                description = card_to_close.desc + str_fx_closed_card_description.format(
                        closed_trade.price,
                        closed_trade.realized_pl,
                        closed_trade.closing_transaction_ds[0],
                        closed_trade.financing,
                        closed_trade.close_time
                )
            except:
                description = card_to_close.desc
        else:
            description = card_to_close.desc

        card_dto = DtoCard(
            id=card_to_close.id,
            name=card_to_close.name,
            idList=id_list_close.id,
            idLabels=card_to_close.id_labels + parsed_labels,
            pos='top',
            desc=description
        )

        trello_cards_service.update_card(card_dto)

        #  endregion

        #  region Send notification

        notification = CurlServicePushNotifications(notifications_id)
        try:
            notification.send_notification("CANCELLED: {0}".format(card_to_close.name))
        except:
            log.warning("Error encountered in push notifications.")

        #  endregion

    #  endregion

