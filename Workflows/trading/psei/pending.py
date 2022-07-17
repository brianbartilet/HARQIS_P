from Applications import *
from Workflows.trading.psei.settings import *
import datetime

FAST_MOVING_AVERAGE_PERIOD = 5


@app.task()
@holidays_aware()
@notify_work("Create PSEI Buy Orders", notify_success=True)
@elastic_logging()
def create_offline_buy_orders_from_system_signal(elastic_id: str,
                                                 index_screener_name: str,
                                                 trading_account_id_aaa: str,
                                                 days_signal=0):
    """
    Create pending buy orders from signals, index data should already been updated from
        strategies.add_signals_screener_investagrams_sandbox_to_elastic
        strategies.update_signals_screener_investagrams_sandbox_to_elastic

    """
    #  region Get all existing cards in target strategy

    index_name = '{0}'.format(INDEX_ROOT_NAME_SCREENER).lower()

    stock_strategy_locs = get_index_data_from_elastic(index_name=index_name,
                                                      app_config_name=elastic_id,
                                                      type_hook=DtoStockInvestagrams)

    stock_strategy_locs_filtered = QList(stock_strategy_locs) \
        .where(lambda x: x.strategy_name == index_screener_name) \
        .where(lambda z: days_between(z.signal_date, DATETIME_FORMAT) == days_signal)  # DEBUG VALUES

    #  endregion

    #  region Create pending buy orders

    webdriver_config = apps_config[trading_account_id_aaa]['webdriver']
    wdf = WebDriverFactory

    with wdf.create_webdriver(**webdriver_config) as driver:
        pl = PageAAALogin(driver, source_id=trading_account_id_aaa)
        pl.login()

        pt = PageAAATradingDeskAccount(driver, source_id=trading_account_id_aaa)
        for stock_buy in stock_strategy_locs_filtered:
            #  region Compute Indicators
            prices_ma = stock_buy.historical[0:FAST_MOVING_AVERAGE_PERIOD]
            sum_prices = 0
            for price in prices_ma:
                sum_prices = sum_prices + price['last_price']
            moving_average = sum_prices / FAST_MOVING_AVERAGE_PERIOD
            #  endregion

            pt.wait_page_to_load(2)
            account_values = pt.get_account_information()
            risk_percent = pt.parameters['risk_percentage'] / 100
            risk_target_value = risk_percent * account_values.total_portfolio_value
            #  entry_price = stock_buy.technical.support_1
            #  entry_price = stock_buy.last_price
            entry_price = moving_average
            units_size, entry_price = get_psei_units_available_from_price(entry_price, risk_target_value)
            if risk_target_value <= account_values.available_cash:
                #  atr based stop
                #  stop_range = float(str(stock_buy.technical.atr).split(' (')[0]) * pt.parameters['stop_atr_factor']
                #  stop_price = stock_buy.last_price - stop_range

                stop_price = stock_buy.technical.support_1
                units_size, stop_price = get_psei_units_available_from_price(stop_price, risk_target_value)

                target_price = stock_buy.technical.resistance_2
                units_size, target_price = get_psei_units_available_from_price(target_price, risk_target_value)

                actual_risk = (entry_price - stop_price) / entry_price
                actual_growth = (target_price - entry_price) / entry_price
                ratio = actual_growth / actual_risk
                if ratio < pt.parameters['risk_reward_factor_min']:
                    log.warning("Trade BUY parameters not met for {0} from date {1}"
                                .format(stock_buy.name, stock_buy.signal_date))
                    continue
                order_dto = DtoCreateOrderAAA(
                    stock_name=stock_buy.name,
                    transaction=Order.BUY.value,
                    order_type=OrderType.LIMIT.value,
                    quantity=units_size,
                    price=entry_price,
                    condition_price=entry_price,
                    good_until=OrderValidUntil.GTC.value,
                    total_fees=0
                )
                stop_dto = DtoCreateOrderAAA(
                    stock_name=stock_buy.name,
                    transaction=Order.SELL.value,
                    order_type=OrderType.LIMIT.value,
                    quantity=units_size,
                    price=stop_price,
                    condition_price=stop_price,
                    good_until=OrderValidUntil.GTC.value,
                    total_fees=0
                )
                profit_dto = DtoCreateOrderAAA(
                    stock_name=stock_buy.name,
                    transaction=Order.SELL.value,
                    order_type=OrderType.LIMIT.value,
                    quantity=units_size,
                    price=target_price,
                    condition_price=target_price,
                    good_until=OrderValidUntil.GTC.value,
                    total_fees=0
                )
                stop_range = float(str(stock_buy.technical.atr).split(' (')[0]) * pt.parameters['stop_atr_factor']
                trail_dto = DtoCreateOrderAAA(
                    stock_name=stock_buy.name,
                    transaction=Order.SELL.value,
                    order_type=OrderType.LIMIT.value,
                    quantity=units_size,
                    price=entry_price,
                    condition_price=entry_price,
                    good_until=OrderValidUntil.GTC.value,
                    distance=stop_range,
                    total_fees=0
                )
                pto = PageAAATradingDeskOrders(driver, source_id=trading_account_id_aaa)
                created = pto.create_order(order_dto)
                #ptd = PageAAATradingDeskPortfolio(driver, source_id=trading_account_id_aaa)
                #portfolio_update = ptd.get_portfolio_information()
                #current_orders = pto.get_orders()
                if not created.created:
                    log.warning('Failed To Create Order {0}'.format(stock_buy.name))
                    continue
                else:
                    log.info('Order Created {0}'.format(stock_buy.name))

                    #  region Add to portfolio index

                    index_dto = DtoTradeManager(
                        create_order=order_dto,
                        stop_order=stop_dto,
                        profit_order=profit_dto,
                        trailing_order=trail_dto,
                        #current_orders=current_orders,
                        #portfolio=portfolio_update,
                        status=TradingConditionsStatus.PENDING_BUY.value,
                        system_name=index_screener_name,
                        stock_data=stock,
                        net_profit=0,
                        last_success_order=created,
                        risk_reward=ratio,
                        date=DATETIME_FORMAT
                    )

                    try:
                        index_name = '{0}'.format(INDEX_ROOT_NAME_TRADES).lower()
                        send_json_data_to_elastic_server(app_config_name=elastic_id,
                                                         json_dump=index_dto.get_dict(),
                                                         index_name=index_name,
                                                         use_interval_map=False,
                                                         location_key=stock_buy.name,
                                                         identifier=stock_buy.signal_date)
                    except:
                        log.warning("Failed to add location for {0} {1}".format(stock_buy.name, stock_buy.signal_date))

                    #  endregion
            else:
                log.warning('Not enough available balance to trade {0}'.format(stock_buy.name))

        pl.wait_for_page_to_load(10)
        pl.logout()

    #  endregion


@app.task()
@holidays_aware()
@notify_work("Update PSEI Orders", notify_success=True, override=True)
@elastic_logging()
def update_portfolio_index_information(elastic_id: str,
                                       trading_account_id_aaa: str):
    """
    Update status to check if order is already in portfolio

    """
    #  region Get all existing cards in index

    index_name = '{0}'.format(INDEX_ROOT_NAME_TRADES).lower()

    stock_strategy_locs = get_index_data_from_elastic(index_name=index_name,
                                                      app_config_name=elastic_id,
                                                      type_hook=DtoTradeManager)

    webdriver_config = apps_config[trading_account_id_aaa]['webdriver']
    wdf = WebDriverFactory
    with wdf.create_webdriver(**webdriver_config) as driver:
        pl = PageAAALogin(driver, source_id=trading_account_id_aaa)
        pl.login()

        stock_orders_information = QList(stock_strategy_locs)

        #  region Pending BUY to OPEN
        #  pending buy to open
        stock_pending_buy = stock_orders_information.where(
            lambda x: x.status == TradingConditionsStatus.PENDING_BUY.value)
        #  get attached portfolio snapshot
        #  get current portfolio
        #  stock name, quantity more or exists, order id
        ptd = PageAAATradingDeskPortfolio(driver, source_id=trading_account_id_aaa)
        current_portfolio_all = ptd.get_portfolio_information()
        for pending_buy in stock_pending_buy:
            try:
                current_portfolio_target = QList(current_portfolio_all).where(
                    lambda x: x.symbol == pending_buy.create_order['stock_name'])
            except:
                log.warning('Stock in portfolio not created by system')
                continue
            previous_portfolio_target = QList(pending_buy.portfolio).where(
                lambda x: x['symbol'] == pending_buy.create_order['stock_name'])
            if len(current_portfolio_target) > 0:
                update = current_portfolio_target.first()
                skip = True
                if len(previous_portfolio_target) == 0:
                    skip = False
                elif int(update.quantity) > int(previous_portfolio_target.first()['quantity']):
                    skip = False
                if not skip:
                    pending_buy.status = TradingConditionsStatus.OPEN.value
                    pending_buy.portfolio_target = current_portfolio_target
                    index_name = '{0}'.format(INDEX_ROOT_NAME_TRADES).lower()
                    signal_date = pending_buy.date[0:10]
                    pending_buy.date = signal_date
                    send_json_data_to_elastic_server(app_config_name=elastic_id,
                                                     json_dump=pending_buy.get_dict(),
                                                     index_name=index_name,
                                                     use_interval_map=False,
                                                     location_key=pending_buy.create_order['stock_name'],
                                                     identifier=signal_date)
        #  endregion

        #  region Pending SELL to CLOSED
        #  pending sell to closed
        stock_pending_sell = stock_orders_information.where(
            lambda x: x.status == TradingConditionsStatus.PENDING_SELL.value)
        #  get attached portfolio snapshot
        #  get current portfolio
        #  stock name, quantity more or exists, order id
        ptd = PageAAATradingDeskPortfolio(driver, source_id=trading_account_id_aaa)
        current_portfolio_all = ptd.get_portfolio_information()
        for pending_sell in stock_pending_sell:
            current_portfolio_target = QList(current_portfolio_all) \
                .where(lambda x: x.symbol == pending_sell.create_order['stock_name'])
            previous_portfolio_target = QList(pending_sell.portfolio) \
                .where(lambda x: x['symbol'] == pending_sell.create_order['stock_name'])
            port_items_count = len(current_portfolio_target)
            if port_items_count >= 0:

                #  region SELL to CLOSED logic

                #  get attached portfolio snapshot
                #  get current portfolio
                #  stock name, quantity less or does not exists, order id
                #  order is removed from order list and would appear in portfolio
                #  handle multiple trades and signals, portfolio snapshot is attached, check current portfolio
                #  check units if exists or increased
                if port_items_count > 0:
                    update = current_portfolio_target.first()
                    quantity = previous_portfolio_target.first()['quantity']
                    if type(quantity) is str:
                        quantity = quantity.replace(',', '')
                    if int(update.quantity) >= int(quantity):
                        continue
                #  endregion

                #  region CLOSED - number crunching + set doc data

                #  filter orders per stock
                #  check sell orders, trailing if any is filled
                #  update fees and growth
                #  insert to last_success_order

                pto = PageAAATradingDeskOrders(driver, source_id=trading_account_id_aaa)
                current_orders = pto.get_orders()
                stock_current_orders = QList(current_orders) \
                    .where(lambda x: x.stock_name == pending_sell.create_order['stock_name']) \
                    .where(lambda y: int(y.quantity.replace(',', '')) == quantity) \
                    .where(lambda z: z.status == OrderStatusAAA.FILLED.value)

                if len(stock_current_orders) > 0:
                    last_order = stock_current_orders.first()
                else:
                    continue

                original_value = pending_sell.create_order['net_value']
                pending_sell.net_profit = ((last_order.net_value - original_value) / original_value) * 100
                pending_sell.last_success_order = last_order
                pending_sell.portfolio_target = current_portfolio_target
                pending_sell.status = TradingConditionsStatus.CLOSED.value

                #  endregion

                index_name = '{0}'.format(INDEX_ROOT_NAME_TRADES).lower()
                signal_date = pending_sell.date[0:10]
                pending_sell.date = signal_date
                send_json_data_to_elastic_server(app_config_name=elastic_id,
                                                 json_dump=pending_sell.get_dict(),
                                                 index_name=index_name,
                                                 use_interval_map=False,
                                                 location_key=pending_sell.create_order['stock_name'],
                                                 identifier=signal_date)

        #  endregion

        #  region NOT CLOSED - Update current values in portfolio

        stock_current = stock_orders_information.where(lambda x: x.status != TradingConditionsStatus.CLOSED.value)
        #  get attached portfolio snapshot
        #  get current portfolio
        #  stock name, quantity more or exists, order id
        ptd = PageAAATradingDeskPortfolio(driver, source_id=trading_account_id_aaa)
        current_portfolio_all = ptd.get_portfolio_information()
        for stock_in_portfolio in stock_current:
            current_portfolio_target = QList(current_portfolio_all) \
                .where(lambda x: x.symbol == stock_in_portfolio.create_order['stock_name'])
            if len(current_portfolio_target) > 0:
                stock_in_portfolio.portfolio_target = current_portfolio_target.first()
                index_name = '{0}'.format(INDEX_ROOT_NAME_TRADES).lower()
                signal_date = stock_in_portfolio.date[0:10]
                stock_in_portfolio.date = signal_date
                send_json_data_to_elastic_server(app_config_name=elastic_id,
                                                 json_dump=stock_in_portfolio.get_dict(),
                                                 index_name=index_name,
                                                 use_interval_map=False,
                                                 location_key=stock_in_portfolio.create_order['stock_name'],
                                                 identifier=signal_date)
        #  endregion

        pl.wait_for_page_to_load(10)
        pl.logout()


@app.task()
@holidays_aware()
@notify_work("Create PSEI Sell Orders", notify_success=True)
@elastic_logging()
def create_offline_sell_orders_from_system_signal(elastic_id: str,
                                                  trading_account_id_aaa: str,
                                                  trades_expire=30):
    #  region Get all existing cards in index

    index_name = '{0}'.format(INDEX_ROOT_NAME_TRADES).lower()

    stock_strategy_locs = get_index_data_from_elastic(index_name=index_name,
                                                      app_config_name=elastic_id,
                                                      type_hook=DtoTradeManager)

    webdriver_config = apps_config[trading_account_id_aaa]['webdriver']
    wdf = WebDriverFactory
    with wdf.create_webdriver(**webdriver_config) as driver:
        pl = PageAAALogin(driver, source_id=trading_account_id_aaa)
        pl.login()

        stock_orders_information = QList(stock_strategy_locs)
        stock_open = stock_orders_information.where(lambda x: x.status in
                                                    [
                                                        TradingConditionsStatus.OPEN.value,
                                                        TradingConditionsStatus.INCOMPLETE_PENDING_STOP_ORDERS.value,
                                                        TradingConditionsStatus.INCOMPLETE_PENDING_PROFIT_ORDERS.value
                                                    ]
                                                    )

        pto = PageAAATradingDeskOrders(driver, source_id=trading_account_id_aaa)
        created_stop_ = False
        created_take_profit_ = False
        for opened in stock_open:
            #  Process Stop Loss
            if opened.status in [TradingConditionsStatus.OPEN.value,
                                 TradingConditionsStatus.INCOMPLETE_PENDING_STOP_ORDERS.value]:
                pto.navigate_to_page(SidebarNavigationLinks.MARKET)
                pto.wait_for_page_to_load(5)
                stop_order_dto = DtoCreateOrderAAA(
                    stock_name=opened.stop_order['stock_name'],
                    transaction=Order.SELL.value,
                    order_type=OrderType.LIMIT.value,
                    quantity=opened.stop_order['quantity'],
                    price=opened.stop_order['price'],
                    good_until=OrderValidUntil.DAY.value,
                    condition_field=ConditionsOrderFieldAAA.LAST_PRICE.value,
                    condition_price=opened.stop_order['price'],
                    condition_trigger=ConditionsOrderTriggerAAA.LESS_THAN_OR_EQUAL_TO.value,
                )
                created_stop = pto.create_order(stop_order_dto, APPEND_ODD_LOTS)
                created_stop_ = created_stop.created
                if not created_stop_:
                    opened.status = TradingConditionsStatus.INCOMPLETE_PENDING_STOP_ORDERS.value

            #  Process Take Profit
            if opened.status in [TradingConditionsStatus.OPEN.value,
                                 TradingConditionsStatus.INCOMPLETE_PENDING_PROFIT_ORDERS.value]:
                pto.navigate_to_page(SidebarNavigationLinks.MARKET)
                pto.wait_for_page_to_load(5)

                ceiling_price = get_psei_ceiling_price(opened.profit_order['price'])
                tp_price = ceiling_price if opened.profit_order['price'] > ceiling_price \
                    else opened.profit_order['price']

                profit_order_dto = DtoCreateOrderAAA(
                    stock_name=opened.profit_order['stock_name'],
                    transaction=Order.SELL.value,
                    order_type=OrderType.LIMIT.value,
                    quantity=opened.profit_order['quantity'],
                    price=tp_price,
                    good_until=OrderValidUntil.DAY.value,
                    condition_field=ConditionsOrderFieldAAA.LAST_PRICE.value,
                    condition_price=tp_price,
                    condition_trigger=ConditionsOrderTriggerAAA.GREATER_THAN_OR_EQUAL_TO.value,
                )

                created_take_profit = pto.create_order(profit_order_dto, APPEND_ODD_LOTS)
                ptd = PageAAATradingDeskPortfolio(driver, source_id=trading_account_id_aaa)
                opened.direction = Order.SELL.value
                opened.portfolio = ptd.get_portfolio_information()
                opened.current_orders = pto.get_orders()
                signal_date = opened.date[0:10]
                opened.date = signal_date

                created_take_profit_ = created_take_profit.created
                if not created_take_profit_:
                    opened.status = TradingConditionsStatus.INCOMPLETE_PENDING_PROFIT_ORDERS.value
            try:
                index_name = '{0}'.format(INDEX_ROOT_NAME_TRADES).lower()

                if created_take_profit_ and created_stop_:
                    opened.status = opened.status = TradingConditionsStatus.PENDING_SELL.value

                send_json_data_to_elastic_server(app_config_name=elastic_id,
                                                 json_dump=opened.get_dict(),
                                                 index_name=index_name,
                                                 use_interval_map=False,
                                                 location_key=opened.create_order['stock_name'],
                                                 identifier=signal_date)
            except Exception:
                log.warning(
                    "Failed to update location for {0} {1}".format(opened.create_order['stock_name'], signal_date))

        pl.wait_for_page_to_load(5)
        pl.logout()


@app.task()
@holidays_aware()
@notify_work("Create PSEI Trailing Orders", notify_success=True)
@elastic_logging()
def create_offline_trailing_stops(elastic_id: str,
                                  trading_account_id_aaa: str):
    #  region Get all existing cards in index

    index_name = '{0}'.format(INDEX_ROOT_NAME_TRADES).lower()

    stock_strategy_locs = get_index_data_from_elastic(index_name=index_name,
                                                      app_config_name=elastic_id,
                                                      type_hook=DtoTradeManager)
    #  endregion

    webdriver_config = apps_config[trading_account_id_aaa]['webdriver']
    wdf = WebDriverFactory
    with wdf.create_webdriver(**webdriver_config) as driver:
        pl = PageAAALogin(driver, source_id=trading_account_id_aaa)
        pl.login()

        stock_orders_information = QList(stock_strategy_locs)
        stocks_pending_sell = stock_orders_information.where(
            lambda x: x.status in [
                                    TradingConditionsStatus.PENDING_SELL.value,
                                    TradingConditionsStatus.INCOMPLETE_PENDING_STOP_ORDERS.value,
                                    TradingConditionsStatus.INCOMPLETE_PENDING_PROFIT_ORDERS.value
                                    ]
        )

        #  get current portfolio
        ptd = PageAAATradingDeskPortfolio(driver, source_id=trading_account_id_aaa)
        current_portfolio_all = ptd.get_portfolio_information()

        for pending_sell in stocks_pending_sell:

            current_portfolio_target = QList(current_portfolio_all) \
                .where(lambda x: x.symbol == pending_sell.trailing_order['stock_name']) \
                .first()

            #  check if current stock price is more than 10% of the entry price
            #  if true create a order for a trailing stop
            #  update last order with the trailing stop
            #  check last order for continuous trailing stop

            distance_atr = pending_sell.trailing_order['distance']

            new_target_trail_price = normalize_psei_price(pending_sell.trailing_order['price'] + distance_atr)
            portfolio_current_price = current_portfolio_target.market_price

            if portfolio_current_price < new_target_trail_price:
                continue

            pto = PageAAATradingDeskOrders(driver, source_id=trading_account_id_aaa)
            pto.navigate_to_page(SidebarNavigationLinks.MARKET)
            pto.wait_for_page_to_load(5)

            trailing_order_dto = DtoCreateOrderAAA(
                stock_name=pending_sell.trailing_order['stock_name'],
                transaction=Order.SELL.value,
                order_type=OrderType.LIMIT.value,
                quantity=pending_sell.trailing_order['quantity'],
                price=new_target_trail_price,
                good_until=OrderValidUntil.DAY.value,
                condition_field=ConditionsOrderFieldAAA.LAST_PRICE.value,
                condition_price=new_target_trail_price,
                condition_trigger=ConditionsOrderTriggerAAA.LESS_THAN_OR_EQUAL_TO.value,
                distance=distance_atr,
            )
            created_trailing = pto.create_order(trailing_order_dto, APPEND_ODD_LOTS)

            signal_date = pending_sell.date[0:10]
            pending_sell.date = signal_date

            try:
                index_name = '{0}'.format(INDEX_ROOT_NAME_TRADES).lower()
                pending_sell.trailing_order = trailing_order_dto
                pending_sell.last_success_order = created_trailing

                #  update trailing stop data from index with new current price
                send_json_data_to_elastic_server(app_config_name=elastic_id,
                                                 json_dump=pending_sell.get_dict(),
                                                 index_name=index_name,
                                                 use_interval_map=False,
                                                 location_key=pending_sell.create_order['stock_name'],
                                                 identifier=signal_date)
            except:
                log.warning("Failed to update location for {0} {1}".format(created_trailing.create_order['stock_name'],
                                                                           signal_date))

        pl.wait_for_page_to_load(5)
        pl.logout()
