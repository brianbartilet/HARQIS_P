from Applications import *
from Workflows.trading.forex.settings import *


@app.task()
def move_cards_to_open_trades(trello_id: str,
                              oanda_id: str,
                              notifications_id: str,
                              open_trades_board_name: str,
                              open_trades_list_name: str,
                              pending_trades_list_name: str,
                              labels_list: [],
                              **kwargs):

    #  region Get open trades

    service_oanda_account = ApiServiceAccount(oanda_id)
    account_use = QList(service_oanda_account.get_account_info().accounts)\
        .where(lambda x: x.mt4AccountID == service_oanda_account.parameters['mt4AccountID'])\
        .first()

    pending_trades_current_cards, id_list, target_board = \
        get_board_data(trello_id, open_trades_board_name, pending_trades_list_name)

    service_trello_boards = ApiServiceBoards(trello_id)
    parsed_labels = [l.id for l in QList(service_trello_boards.get_board_labels(target_board))
        .where(lambda x: x.name in labels_list)]

    filter_pending_trades_current_cards = QList(pending_trades_current_cards)\
        .where(lambda x: len(set(x.id_labels).intersection(parsed_labels)) > 0)

    open_trading = []
    service_oanda_autochartist = ApiServiceOrders(oanda_id)
    service_oanda_trades = ApiServiceTrades(oanda_id)
    for pending_trade_card in filter_pending_trades_current_cards:
        match = re.search(r'```(.*?)```', pending_trade_card.desc, re.DOTALL).group(1)
        try:
            config = yaml.load(match)
        except:
            log.warning("Cannot process embedded configuration")
            continue
        order = service_oanda_autochartist.get_orders(account_use.id,
                                                      ids='{0}'.format(config['TRADE']['trade_id']),
                                                      state=EnumTradeStateFilter.ALL.value)
        target = QList(order['orders']).first()

        try:
            trade_opened_id = target['tradeOpenedID']
        except KeyError:
            log.warning("Trade is still not open: {0}".format(target['id']))
            continue

        open_trades = service_oanda_trades.get_trades_from_account(account_id=account_use.id,
                                                                   state=EnumTradeStateFilter.OPEN.value,
                                                                   ids='{0}'.format(trade_opened_id))
        if len(open_trades) == 0:
            log.warning("Trade is still not open: {0}".format(target['id']))
            continue

        open_trade = QList(open_trades).first()
        open_trading.append((pending_trade_card, target, open_trade))

    #  endregion

    #  region Move Cards

    trello_cards_service = ApiServiceCards(trello_id)
    open_trades_current_cards, id_list_opened, target_board = \
        get_board_data(trello_id, open_trades_board_name, open_trades_list_name)

    for card_to_open, og_order, opened_trade in open_trading:

        #  region Move Cards To Open

        card_dto = DtoCard(
            id=card_to_open.id,
            name=card_to_open.name,
            idList=id_list_opened.id,
            id_labels=parsed_labels,
            pos='top',
            desc=str_fx_add_card_description.replace('signal_id: {0}'.format(og_order['id']),
                                                     'signal_id: {0}'.format(opened_trade.id))
        )

        trello_cards_service.update_card(card_dto)

        #  endregion

        #  region Send notification

        notification = CurlServicePushNotifications(notifications_id)
        try:
            notification.send_notification("OPENED: {0}".format(card_to_open.name))
        except:
            log.warning("Error encountered in push notifications.")

        #  endregion

    #  endregion


@app.task()
def create_manual_trade_open_to_cards(trello_id: str,
                                      oanda_id: str,
                                      open_trades_board_name: str,
                                      open_trades_list_name: str,
                                      labels_list: [],
                                      **kwargs):
    # region Get pending trades from broker

    service_oanda_account = ApiServiceAccount(oanda_id)
    account_use = QList(service_oanda_account.get_account_info().accounts)\
        .where(lambda x: x.mt4AccountID == service_oanda_account.parameters['mt4AccountID'])\
        .first()

    service_oanda_trades = ApiServiceTrades(oanda_id)

    current_open_trades = service_oanda_trades.get_trades_from_account(account_id=account_use.id,
                                                               state=EnumTradeStateFilter.OPEN.value)
    #  endregion

    #  region Check existing open trades from card, if trade id does not then exists add

    open_trades_current_cards, id_list_opened, target_board = \
        get_board_data(trello_id, open_trades_board_name, open_trades_list_name)

    service_trello_boards = ApiServiceBoards(trello_id)
    parsed_labels = [l.id for l in QList(service_trello_boards.get_board_labels(target_board))
        .where(lambda x: x.name in labels_list)]

    filter_open_trades_current_cards = QList(open_trades_current_cards)\
        .where(lambda x: set(x.id_labels).intersection(parsed_labels))
    
    to_create_cards = []
    for current_open_trade in current_open_trades:
        open_trade_found = False
        for open_card in filter_open_trades_current_cards:
            match = re.search(r'```(.*?)```', open_card.desc, re.DOTALL).group(1)
            try:
                config = yaml.load(match)
                if int(current_open_trade.id) == config['TRADE']['trade_id']:
                    open_trade_found = True
                    break
            except:
                log.warning("Cannot process embedded configuration.")
                continue

        if not open_trade_found:
            #  insert to create card list
            to_create_cards.append(current_open_trade)
            continue

    #  endregion

    #  region Setup Card Data and Add

    service_trello_cards = ApiServiceCards(trello_id)
    for to_create_card in to_create_cards:
        direction = 'SELL' if '-' in to_create_card.current_units else 'BUY'
        labels_ = [direction]
        for l in labels_list:
            labels_.append(l)

        parsed_labels = [l.id for l in QList(service_trello_boards.get_board_labels(target_board))
                         .where(lambda x: x.name in labels_)]

        instruments_data = service_oanda_account.get_account_instrument_details(account_use.id, to_create_card.instrument)
        instrument_data = QList(instruments_data).first()

        round_int = abs(instrument_data.pip_location)
        instrument = str(to_create_card.instrument).replace('_', '')
        card_dto = DtoCard(
            name=str_card_title.format(instrument,
                                       'NA',
                                       round(float(to_create_card.price), round_int),
                                       round(float(to_create_card.stop_loss_order.price), round_int),
                                       round(float(to_create_card.take_profit_order.price), round_int)
                                       ),
            idList=id_list_opened.id,
            idLabels=parsed_labels,
            pos='top',
            desc=str_fx_add_card_description.format(
                    instrument,
                    'NA',
                    '{0}'.format(to_create_card.id),
                    '{0}'.format(to_create_card.current_units),
                    'NA',
                    'NA'
                 ),

        )
        service_trello_cards.add_card(card_dto)

    #  endregion



@app.task()
def update_orders_trailing_stop_delayed(trello_id: str,
                                        oanda_id: str,
                                        indicators_id: str,
                                        open_trades_board_name: str,
                                        open_trades_list_name: str,
                                        labels_list: [],
                                        **kwargs):

    # region Get pending trades from broker

    service_oanda_account = ApiServiceAccount(oanda_id)
    account_use = QList(service_oanda_account.get_account_info().accounts)\
        .where(lambda x: x.mt4AccountID == service_oanda_account.parameters['mt4AccountID'])\
        .first()

    service_oanda_trades = ApiServiceTrades(oanda_id)
    current_open_trades = service_oanda_trades.get_trades_from_account(account_id=account_use.id,
                                                               state=EnumTradeStateFilter.OPEN.value)
    #  endregion

    #  region Get board data
    open_trades_current_cards, id_list_opened, target_board = \
        get_board_data(trello_id, open_trades_board_name, open_trades_list_name)

    service_trello_boards = ApiServiceBoards(trello_id)
    parsed_labels = [l.id for l in QList(service_trello_boards.get_board_labels(target_board))
        .where(lambda x: x.name in labels_list)]

    filter_open_trades_current_cards = QList(open_trades_current_cards) \
        .where(lambda x: set(x.id_labels).intersection(parsed_labels))

    to_update_cards = []
    for current_open_trade in current_open_trades:
        for open_card in filter_open_trades_current_cards:
            match = re.search(r'```(.*?)```', open_card.desc, re.DOTALL).group(1)
            try:
                config = yaml.load(match)
                if int(current_open_trade.id) == int(config['TRADE']['trade_id']):
                    if config['TRADE']['signal_id'] == 'NA':
                        continue
                    to_update_cards.append((current_open_trade, config))
                    break
            except:
                log.warning("Cannot process embedded configuration.")
                continue

    #

    #  region Get trade id and trail when first price is reached, price = intial entry price, distance = 1x atr
    for trade, config in to_update_cards:

        try:
            ts_order = trade.trailing_stop_loss_order
            continue
        except AttributeError:


            instruments_data = service_oanda_account.get_account_instrument_details(account_use.id,
                                                                                    trade.instrument)
            instrument_data = QList(instruments_data).first()
            round_int = abs(instrument_data.pip_location)
            """
            dto_order = DtoOrder(
                order=DtoTrailingStopLossOrderRequest(
                    tradeID=trade.id,
                    price=str(round(signal.data.price, round_int)),
                    distance='{0}'.format(ts_distance))
                )
            service = ApiServiceOrders(source_id=oanda_id)
            service.create_order(account_use.id, dto_order)
            """

    #  endregion
