from Applications import *
from Workflows.trading.forex.settings import *
from typing import Callable

@app.task()
def add_cards_from_signals_fx_key_levels(trello_id,
                                         oanda_id,
                                         indicators_id,
                                         notifications_id,
                                         signals_board_name: str,
                                         signals_list_name: str,
                                         transact_list_name: str,
                                         labels_list: [],
                                         **kwargs):

    s_current_cards, s_id_list, s_target_board = get_board_data(trello_id, signals_board_name, signals_list_name)

    service_trello_cards = ApiServiceCards(trello_id)
    service_trello_boards = ApiServiceBoards(trello_id)
    service_oanda_autochartist = ApiServiceAutoChartist(oanda_id)

    #  region Filter signals criteria

    signals_raw = QList(service_oanda_autochartist.get_signals(**kwargs))
    signals_data = signals_raw\
        .where(lambda x: (x.meta.completed == 1))\
        .where(lambda y: (str(y.instrument).replace('_', '') not in except_pairs))\
        .where(lambda z: (z.type == 'keylevel'))

    #  endregion

    service_oanda_account = ApiServiceAccount(source_id=oanda_id)

    for signal in signals_data:

        #  region Search if signal id in card description from previous insertions
        exists = False
        for c in s_current_cards:
            if str('signal_id: {0}'.format(signal.id)) in c.desc:
                exists = True
                break
        if exists:
            continue
        #  endregion

        #  region Generate main trade logic
        #  check if approaching and assign action to key level,
        #  key levels can be continuing or polarizing
        instrument = str(signal.instrument).replace('_', '')
        key_level_type = str(signal.meta.pattern).lower()
        direction = 'BUY' if signal.meta.direction == 1 else 'SELL'

        #  endregion

        #  region Fetch indicators data

        indicator_service = ApiIndicatorsFeed(source_id=indicators_id,
                                              indicator_short_name='atr')

        indicator_dto = IndicatorParameters(
            symbol=str(signal.instrument).replace('_', '/'),
            interval=traded_time_frames_indicator[int(signal.meta.interval)],
        )

        indicator_data = indicator_service.get_indicator_values(indicator_dto)
        current_atr = float(QList(indicator_data['values']).first()['atr'])

        #  endregion

        # region Indicator Filtering

        indicator_filter_trade = False
        aots_trend_long = 240
        aots_trend_short = 120
        aots_current = 48
        indicator_service = ApiIndicatorsFeed(source_id=indicators_id,
                                              indicator_short_name='ma')

        aots_trend_long_indicator_dto = IndicatorParameters(
            symbol=str(signal.instrument).replace('_', '/'),
            interval=traded_time_frames_indicator[int(signal.meta.interval)],
            time_period=aots_trend_long,
            ma_type='EMA'
        )
        aots_trend_short_indicator_dto = IndicatorParameters(
            symbol=str(signal.instrument).replace('_', '/'),
            interval=traded_time_frames_indicator[int(signal.meta.interval)],
            time_period=aots_trend_short,
            ma_type='EMA'
        )
        aots_current_indicator_dto = IndicatorParameters(
            symbol=str(signal.instrument).replace('_', '/'),
            interval=traded_time_frames_indicator[int(signal.meta.interval)],
            time_period=aots_current,
            ma_type='SMA'
        )

        try:
            aots_trend_long_indicator_data = indicator_service.get_indicator_values(aots_trend_long_indicator_dto)
            aots_trend_long_indicator_value = float(QList(aots_trend_long_indicator_data['values']).first()['ma'])
            aots_trend_short_indicator_data = indicator_service.get_indicator_values(aots_trend_short_indicator_dto)
            aots_trend_short_indicator_value = float(QList(aots_trend_short_indicator_data['values']).first()['ma'])
            aots_current_indicator_data = indicator_service.get_indicator_values(aots_current_indicator_dto)
            aots_current_indicator_value = float(QList(aots_current_indicator_data['values']).first()['ma'])

            if signal.meta.direction == 1:
                if (aots_current_indicator_value > aots_trend_short_indicator_value)\
                        and (aots_trend_short_indicator_value > aots_trend_long_indicator_value)\
                        and (aots_current_indicator_value > aots_trend_long_indicator_value):
                    indicator_filter_trade = True
            else:
                if (aots_current_indicator_value < aots_trend_short_indicator_value)\
                        and (aots_trend_short_indicator_value < aots_trend_long_indicator_value)\
                        and (aots_current_indicator_value < aots_trend_long_indicator_value):
                    indicator_filter_trade = True
        except:
            log.warning("Cannot process indicator values.")
            continue

        #  endregion

        #  region Setup trade parameters

        factor_atr = (service_oanda_account.parameters['stop_atr_factor'] * current_atr)

        account_data = service_oanda_account.get_account_info()
        account_trade = QList(account_data.accounts)\
            .first(lambda x: x.mt4AccountID == service_oanda_account.parameters['mt4AccountID'])
        account_details = service_oanda_account.get_account_details(account_trade.id)
        instruments_data = service_oanda_account.get_account_instrument_details(account_trade.id, signal.instrument)
        instrument_data = QList(instruments_data).first()

        risk_amount = round(float(account_details.balance) * service_oanda_account.parameters['risk_percentage']/100, 2)
        sl_pips = factor_atr / 10 ** instrument_data.pip_location
        amount_risk_per_pip = risk_amount / sl_pips
        units = int(amount_risk_per_pip / (10 ** -4))

        round_int = abs(instrument_data.pip_location)
        units_append_str = '' if signal.meta.direction == 1 else '-'

        stop_loss_price = (signal.data.price - factor_atr) if signal.meta.direction == 1 \
            else (signal.data.price + factor_atr)

        #  endregion

        #  region Create Trades - create limit order

        transact = None
        if service_oanda_account.parameters['allow_trading'] and indicator_filter_trade:
            take_profit = signal.data.prediction.pricehigh if signal.meta.direction == 1 \
                else signal.data.prediction.pricelow
            trailing_stop = signal.data.prediction.pricelow if signal.meta.direction == 1 \
                else signal.data.prediction.pricehigh

            sl = round(stop_loss_price, round_int)
            tp = round(take_profit, round_int)
            ts = round(trailing_stop, round_int)
            ts_distance = round(2.5 * current_atr, round_int)

            dto_order = DtoOrder(
                order=DtoLimitOrderRequest(
                    price=str(round(signal.data.price, round_int)),
                    stopLossOnFill=DtoStopLossDetails(price='{0}'.format(sl)),
                    takeProfitOnFill=DtoTakeProfitDetails(price='{0}'.format(tp)),
                    trailingStopLossOnFill=DtoTrailingStopLossDetails(price='{0}'.format(ts),
                                                                      distance='{0}'.format(ts_distance)),
                    timeInForce=EnumTimeInForce.GTC.value,
                    instrument=signal.instrument,
                    units='{0}{1}'.format(units_append_str, units),
                    type=EnumOrderType.LIMIT.value,
                    positionFill=EnumOrderPositionFill.DEFAULT.value,

                )
            )
            service = ApiServiceOrders(source_id=oanda_id)
            transact = service.create_order(account_trade.id, dto_order)

        #  endregion

        #  region Setup card data to insert in lists

        time_frame = traded_time_frames[int(signal.meta.interval)]

        labels_ = [direction, time_frame, key_level_type.upper()]
        for l in labels_list:
            labels_.append(l)


        parsed_labels = [l.id for l in QList(service_trello_boards.get_board_labels(s_target_board))
                         .where(lambda x: x.name in labels_)]

        image_viewer = 'HRSPatternImage' if signal.type == 'keylevel' else 'CPPatternImage'
        image_url = str_autochartist_chart_url.format(image_viewer, signal.id)

        card_dto = DtoCard(
            name=str_card_title.format(instrument,
                                       signal.meta.probability,
                                       round(signal.data.price, round_int),
                                       round(stop_loss_price, round_int),
                                       round(signal.data.prediction.pricehigh, round_int)
                                       ),
            idList=s_id_list.id,
            idLabels=parsed_labels,
            pos='top',
            desc=str_fx_add_card_description.format(
                    instrument,
                    signal.id,
                    "TBD",
                    "TBD",
                    signal.meta.scores.quality,
                    image_url
                 ) +
                 str_indicators_values.format(
                     aots_current_indicator_value,
                     aots_trend_short_indicator_value,
                     aots_trend_long_indicator_value
                 ),

        )

        service_trello_cards.add_card(card_dto)

        try:
            confirm_transact = transact['orderCreateTransaction']
        except:
            confirm_transact = None

        if confirm_transact is not None:
            t_current_cards, t_id_list, target_board = get_board_data(trello_id, signals_board_name, transact_list_name)
            card_dto.idList = t_id_list.id
            card_dto.desc = str_fx_add_card_description.format(
                instrument,
                signal.id,
                confirm_transact['id'],
                confirm_transact['units'],
                signal.meta.scores.quality,
                image_url
            )
            service_trello_cards.add_card(card_dto)

        #  endregion

        #  region Send notification

        notification = CurlServicePushNotifications(notifications_id)
        try:
            notification.send_notification("{0} Trade Alert {1} [{2}] %P{3}"
                                           .format(direction.upper(),
                                                   time_frame,
                                                   instrument,
                                                   signal.meta.probability
                                                   )
                                           )
        except:
            log.warning("Error encountered in push notifications.")

        #  endregion


@app.task()
def add_signals_fx_key_levels_to_elastic(elastic_id,
                                         oanda_id,
                                         indicators_id,
                                         notifications_id,
                                         #strategy_func: Callable,
                                         **kwargs):

    #  region Get all existing cards in strategies

    forex_strategy_locs_filtered = []
    try:
        index_name = '{0}'.format(INDEX_ROOT_NAME_FOREX_AUTOCHARTIST_TRADER).lower()
        forex_strategy_locs = get_index_data_from_elastic(index_name=index_name,
                                                          app_config_name=elastic_id,
                                                          type_hook=DtoForexStrategy
                                                          )
        forex_strategy_locs_filtered = QList(forex_strategy_locs).where()
    except:
        pass

    #  endregion

    #  region Filter signals criteria

    service_oanda_autochartist = ApiServiceAutoChartist(oanda_id)

    signals_raw = QList(service_oanda_autochartist.get_signals(**kwargs))
    signals_data = signals_raw\
        .where(lambda x: (x.meta.completed == 1))\
        .where(lambda y: (str(y.instrument).replace('_', '') not in except_pairs))\
        .where(lambda z: (z.type == 'keylevel'))

    #  endregion

    service_oanda_account = ApiServiceAccount(source_id=oanda_id)

    for signal in signals_data:

        #  region Search if signal id in index from previous insertions
        exists = False
        for d in forex_strategy_locs_filtered:
            exists = True if signal.id == d.id else False
            break
        if exists:
            continue
        #  endregion

        #  region Generate main trade logic

        #  check if approaching and assign action to key level,
        #  key levels can be continuing or polarizing
        instrument = str(signal.instrument).replace('_', '')
        key_level_type = str(signal.meta.pattern).lower()
        direction = 'BUY' if signal.meta.direction == 1 else 'SELL'

        #  endregion

        #  region Fetch indicators data

        indicator_service = ApiIndicatorsFeed(source_id=indicators_id,
                                              indicator_short_name='atr')

        indicator_dto = IndicatorParameters(
            symbol=str(signal.instrument).replace('_', '/'),
            interval=traded_time_frames_indicator[int(signal.meta.interval)],
        )

        indicator_data = indicator_service.get_indicator_values(indicator_dto)
        current_atr = float(QList(indicator_data['values']).first()['atr'])

        #  endregion

        # region Indicator Filtering

        indicator_filter_trade = False
        aots_trend_long = 240
        aots_trend_short = 120
        aots_current = 48
        indicator_service = ApiIndicatorsFeed(source_id=indicators_id,
                                              indicator_short_name='ma')

        aots_trend_long_indicator_dto = IndicatorParameters(
            symbol=str(signal.instrument).replace('_', '/'),
            interval=traded_time_frames_indicator[int(signal.meta.interval)],
            time_period=aots_trend_long,
            ma_type='EMA'
        )
        aots_trend_short_indicator_dto = IndicatorParameters(
            symbol=str(signal.instrument).replace('_', '/'),
            interval=traded_time_frames_indicator[int(signal.meta.interval)],
            time_period=aots_trend_short,
            ma_type='EMA'
        )
        aots_current_indicator_dto = IndicatorParameters(
            symbol=str(signal.instrument).replace('_', '/'),
            interval=traded_time_frames_indicator[int(signal.meta.interval)],
            time_period=aots_current,
            ma_type='SMA'
        )

        try:
            aots_trend_long_indicator_data = indicator_service.get_indicator_values(aots_trend_long_indicator_dto)
            aots_trend_long_indicator_value = float(QList(aots_trend_long_indicator_data['values']).first()['ma'])
            aots_trend_short_indicator_data = indicator_service.get_indicator_values(aots_trend_short_indicator_dto)
            aots_trend_short_indicator_value = float(QList(aots_trend_short_indicator_data['values']).first()['ma'])
            aots_current_indicator_data = indicator_service.get_indicator_values(aots_current_indicator_dto)
            aots_current_indicator_value = float(QList(aots_current_indicator_data['values']).first()['ma'])

            if signal.meta.direction == 1:
                if (aots_current_indicator_value > aots_trend_short_indicator_value)\
                        and (aots_trend_short_indicator_value > aots_trend_long_indicator_value)\
                        and (aots_current_indicator_value > aots_trend_long_indicator_value):
                    indicator_filter_trade = True
            else:
                if (aots_current_indicator_value < aots_trend_short_indicator_value)\
                        and (aots_trend_short_indicator_value < aots_trend_long_indicator_value)\
                        and (aots_current_indicator_value < aots_trend_long_indicator_value):
                    indicator_filter_trade = True
        except:
            log.warning("Cannot process indicator values.")
            continue

        #  endregion

        #  region Setup trade parameters

        factor_atr = (service_oanda_account.parameters['stop_atr_factor'] * current_atr)

        account_data = service_oanda_account.get_account_info()
        account_trade = QList(account_data.accounts)\
            .first(lambda x: x.mt4AccountID == service_oanda_account.parameters['mt4AccountID'])
        account_details = service_oanda_account.get_account_details(account_trade.id)
        instruments_data = service_oanda_account.get_account_instrument_details(account_trade.id, signal.instrument)
        instrument_data = QList(instruments_data).first()

        risk_amount = round(float(account_details.balance) * service_oanda_account.parameters['risk_percentage']/100, 2)
        sl_pips = factor_atr / 10 ** instrument_data.pip_location
        amount_risk_per_pip = risk_amount / sl_pips
        units = int(amount_risk_per_pip / (10 ** -4))

        round_int = abs(instrument_data.pip_location)
        units_append_str = '' if signal.meta.direction == 1 else '-'

        stop_loss_price = (signal.data.price - factor_atr) if signal.meta.direction == 1 \
            else (signal.data.price + factor_atr)

        #  endregion

        #  region Create Trades - create limit order

        transact = None
        if service_oanda_account.parameters['allow_trading'] and indicator_filter_trade:
            take_profit = signal.data.prediction.pricehigh if signal.meta.direction == 1 \
                else signal.data.prediction.pricelow
            trailing_stop = signal.data.prediction.pricelow if signal.meta.direction == 1 \
                else signal.data.prediction.pricehigh

            sl = round(stop_loss_price, round_int)
            tp = round(take_profit, round_int)
            ts = round(trailing_stop, round_int)
            ts_distance = round(2.5 * current_atr, round_int)

            dto_order = DtoOrder(
                order=DtoLimitOrderRequest(
                    price=str(round(signal.data.price, round_int)),
                    stopLossOnFill=DtoStopLossDetails(price='{0}'.format(sl)),
                    takeProfitOnFill=DtoTakeProfitDetails(price='{0}'.format(tp)),
                    trailingStopLossOnFill=DtoTrailingStopLossDetails(price='{0}'.format(ts),
                                                                      distance='{0}'.format(ts_distance)),
                    timeInForce=EnumTimeInForce.GTC.value,
                    instrument=signal.instrument,
                    units='{0}{1}'.format(units_append_str, units),
                    type=EnumOrderType.LIMIT.value,
                    positionFill=EnumOrderPositionFill.DEFAULT.value,

                )
            )
            service = ApiServiceOrders(source_id=oanda_id)
            transact = service.create_order(account_trade.id, dto_order)

        #  endregion

        time_frame = traded_time_frames[int(signal.meta.interval)]

        #  region Send notification

        notification = CurlServicePushNotifications(notifications_id)
        try:
            notification.send_notification("{0} Trade Alert {1} [{2}] %P{3}"
                                           .format(direction.upper(),
                                                   time_frame,
                                                   instrument,
                                                   signal.meta.probability
                                                   )
                                           )
        except:
            log.warning("Error encountered in push notifications.")


@app.task()
def add_cards_from_signals_fx_key_levels_prediction(trello_id,
                                         oanda_id,
                                         indicators_id,
                                         notifications_id,
                                         signals_board_name: str,
                                         signals_list_name: str,
                                         transact_list_name: str,
                                         labels_list: [],
                                         **kwargs):

    t_current_cards, t_id_list, t_target_board = get_board_data(trello_id, signals_board_name, transact_list_name)

    service_trello_cards = ApiServiceCards(trello_id)
    service_trello_boards = ApiServiceBoards(trello_id)
    service_oanda_autochartist = ApiServiceAutoChartist(oanda_id)

    #  region Filter signals criteria

    signals_raw = QList(service_oanda_autochartist.get_signals(**kwargs))
    signals_data = signals_raw\
        .where(lambda x: (x.meta.completed == 0))\
        .where(lambda y: (str(y.instrument).replace('_', '') in traded_pairs))\
        .where(lambda z: (z.type == 'keylevel'))

    #  endregion

    service_oanda_account = ApiServiceAccount(source_id=oanda_id)

    for signal in signals_data:

        #  region Search if signal id in card description from previous insertions
        exists = False
        for c in t_current_cards:
            if str('signal_id: {0}'.format(signal.id)) in c.desc:
                exists = True
                break
        if exists:
            continue
        #  endregion

        #  region Generate main trade logic
        #  check if approaching and assign action to key level,
        #  key levels can be continuing or polarizing
        instrument = str(signal.instrument).replace('_', '')
        key_level_type = str(signal.meta.pattern).lower()
        direction = 'BUY' if signal.meta.direction == 1 else 'SELL'

        #  endregion

        #  region Fetch indicators data

        indicator_service = ApiIndicatorsFeed(source_id=indicators_id,
                                              indicator_short_name='atr')

        indicator_dto = IndicatorParameters(
            symbol=str(signal.instrument).replace('_', '/'),
            interval=traded_time_frames_indicator[int(signal.meta.interval)],
        )

        indicator_data = indicator_service.get_indicator_values(indicator_dto)
        current_atr = float(QList(indicator_data['values']).first()['atr'])

        #  endregion

        #  region Setup trade parameters

        factor_atr = (service_oanda_account.parameters['stop_atr_factor'] * current_atr)

        account_data = service_oanda_account.get_account_info()
        account_trade = QList(account_data.accounts)\
            .first(lambda x: x.mt4AccountID == service_oanda_account.parameters['mt4AccountID'])
        account_details = service_oanda_account.get_account_details(account_trade.id)
        instruments_data = service_oanda_account.get_account_instrument_details(account_trade.id, signal.instrument)
        instrument_data = QList(instruments_data).first()

        risk_amount = round(float(account_details.balance) * service_oanda_account.parameters['risk_percentage']/100, 2)
        sl_pips = factor_atr / 10 ** instrument_data.pip_location
        amount_risk_per_pip = risk_amount / sl_pips
        units = int(amount_risk_per_pip / (10 ** -4))

        round_int = abs(instrument_data.pip_location)
        units_append_str = '' if signal.meta.direction == 1 else '-'

        stop_loss_price = (signal.data.price - factor_atr) if signal.meta.direction == 1 \
            else (signal.data.price + factor_atr)

        #  endregion

        #  region Setup card data to insert in lists

        time_frame = traded_time_frames[int(signal.meta.interval)]

        labels_ = [direction, time_frame, key_level_type.upper()]
        for l in labels_list:
            labels_.append(l)

        current_cards, id_list, target_board = get_board_data(trello_id, signals_board_name, signals_list_name)
        parsed_labels = [l.id for l in QList(service_trello_boards.get_board_labels(target_board))
                         .where(lambda x: x.name in labels_)]

        image_viewer = 'HRSPatternImage' if signal.type == 'keylevel' else 'CPPatternImage'

        image_url = str_autochartist_chart_url.format(image_viewer, signal.id)

        card_dto = DtoCard(
            name=str_card_title.format(instrument,
                                       signal.meta.probability,
                                       round(signal.data.price, round_int),
                                       round(stop_loss_price, round_int),
                                       'NA'
                                       ),
            idList=id_list.id,
            idLabels=parsed_labels,
            pos='top',
            desc=str_fx_add_card_description.format(
                    instrument,
                    signal.id,
                    "TBD",
                    "TBD",
                    signal.meta.scores.quality,
                    image_url
                ),

        )

        service_trello_cards.add_card(card_dto)


@app.task()
def add_cards_from_signals_fx_key_levels_manual(trello_id,
                                                oanda_id,
                                                indicators_id,
                                                notifications_id,
                                                signals_board_name: str,
                                                signals_list_name: str,
                                                labels_list: [],
                                                **kwargs):

    current_cards, id_list, target_board = get_board_data(trello_id, signals_board_name, signals_list_name)

    service_trello_cards = ApiServiceCards(trello_id)
    service_trello_boards = ApiServiceBoards(trello_id)
    service_oanda_autochartist = ApiServiceAutoChartist(oanda_id)

    #  region Filter signals criteria

    signals_raw = QList(service_oanda_autochartist.get_signals(**kwargs))
    signals_data = signals_raw\
        .where(lambda x: (x.meta.completed == 1))\
        .where(lambda y: (str(y.instrument).replace('_', '') not in traded_pairs))\
        .where(lambda z: (z.type == 'keylevel'))

    #  endregion

    service_oanda_account = ApiServiceAccount(source_id=oanda_id)

    for signal in signals_data:

        #  region Search if signal id in card description from previous insertions
        exists = False
        for c in current_cards:
            if str('signal_id: {0}'.format(signal.id)) in c.desc:
                exists = True
                break
        if exists:
            continue
        #  endregion

        #  region Generate main trade logic
        #  check if approaching and assign action to key level,
        #  key levels can be continuing or polarizing
        instrument = str(signal.instrument).replace('_', '')
        key_level_type = str(signal.meta.pattern).lower()
        direction = 'BUY' if signal.meta.direction == 1 else 'SELL'

        #  endregion

        #  region Fetch indicators data

        indicator_service = ApiIndicatorsFeed(source_id=indicators_id,
                                              indicator_short_name='atr')

        indicator_dto = IndicatorParameters(
            symbol=str(signal.instrument).replace('_', '/'),
            interval=traded_time_frames_indicator[int(signal.meta.interval)],
        )
        try:
            indicator_data = indicator_service.get_indicator_values(indicator_dto)
            current_atr = float(QList(indicator_data['values']).first()['atr'])
        except KeyError:
            log.warning("Instrument {0} not supported by indicator service".format(instrument))
            continue

        #  endregion

        #  region Setup trade parameters

        factor_atr = (service_oanda_account.parameters['stop_atr_factor'] * current_atr)

        account_data = service_oanda_account.get_account_info()
        account_trade = QList(account_data.accounts)\
            .first(lambda x: x.mt4AccountID == service_oanda_account.parameters['mt4AccountID'])
        instruments_data = service_oanda_account.get_account_instrument_details(account_trade.id, signal.instrument)
        instrument_data = QList(instruments_data).first()

        round_int = abs(instrument_data.pip_location)

        stop_loss_price = (signal.data.price - factor_atr) if signal.meta.direction == 1 \
            else (signal.data.price + factor_atr)

        #  endregion

        #  region Setup card data to insert in lists

        time_frame = traded_time_frames[int(signal.meta.interval)]

        labels_ = [direction, time_frame, key_level_type.upper()]
        for l in labels_list:
            labels_.append(l)

        parsed_labels = [l.id for l in QList(service_trello_boards.get_board_labels(target_board))
                         .where(lambda x: x.name in labels_)]

        image_viewer = 'HRSPatternImage' if signal.type == 'keylevel' else 'CPPatternImage'

        image_url = str_autochartist_chart_url.format(image_viewer, signal.id)

        card_dto = DtoCard(
            name=str_card_title.format(instrument,
                                       signal.meta.probability,
                                       round(signal.data.price, round_int),
                                       round(stop_loss_price, round_int),
                                       round(signal.data.prediction.pricehigh, round_int)
                                       ),
            idList=id_list.id,
            idLabels=parsed_labels,
            pos='top',
            desc=str_fx_add_card_description.format(
                    instrument,
                    signal.id,
                    "TBD",
                    "TBD",
                    signal.meta.scores.quality,
                    image_url
                ),

        )

        service_trello_cards.add_card(card_dto)

        #  endregion

        #  region Send notification

        notification = CurlServicePushNotifications(notifications_id)
        try:
            notification.send_notification("{0} Manual Trade Alert {1} [{2}] %P{3}"
                                           .format(direction.upper(),
                                                   time_frame,
                                                   instrument,
                                                   signal.meta.probability
                                                   )
                                           )
        except:
            log.warning("Error encountered in push notifications.")

        #  endregion


@app.task()
def remove_completed_signal_cards_from_list(trello_id,
                                            oanda_id,
                                            board_name: str,
                                            list_name: str):

    current_cards, id_list, target_board = get_board_data(trello_id, board_name, list_name)
    trello_cards_service = ApiServiceCards(trello_id)
    trello_boards_service = ApiServiceBoards(trello_id)

    #  region Get Completed Signals

    service_oanda_ac = ApiServiceAutoChartist(oanda_id)
    signals_data_completed = QList(service_oanda_ac.get_signals()) \
        .where(lambda y: (str(y.instrument).replace('_', '') in traded_pairs)) \
        .where(lambda x: (x.meta.completed == 1))

    #  endregion

    for signal in signals_data_completed:
        """
        Search if signal id in card description from previous insertions then remove

        """
        for c in current_cards:
            if str(signal.id) in c.desc:
                trello_cards_service.archive_card(c)


@app.task()
def archive_signals_cards(trello_id,
                          board_name: str,
                          list_name: str):

    current_cards, id_list, target_board = get_board_data(trello_id, board_name, list_name)
    trello_cards_service = ApiServiceCards(trello_id)

    for c in current_cards:
        trello_cards_service.archive_card(c)


