from Applications import *
from Workflows.trading.psei.settings import *
from datetime import datetime
from Core.utilities.csv_reader import generate_objects_from_csv_data


@app.task()
@notify_work()
@elastic_logging()
def add_cards_from_signals_screener_investagrams_sandbox(investagrams_id,
                                                         trello_id,
                                                         screener_name,
                                                         board_name,
                                                         list_name,
                                                         labels_list: []):

    with WebDriverFactory.create_webdriver(**apps_config[investagrams_id]['webdriver']) as driver:
        pl = PageInvestagramsLogin(driver=driver, source_id=investagrams_id)
        pl.login(pl.parameters['username'], pl.parameters['password'])

        sp = PageInvestagramsScreener(driver=driver, source_id=investagrams_id)
        sp.select_screener(screener_name)
        results = sp.get_all_results()

        service_trello_cards = ApiServiceCards(trello_id)
        service_trello_boards = ApiServiceBoards(trello_id)

        stock_page = PageInvestegramsStock(driver=driver, source_id=investagrams_id)
        scrape_data = []
        #  region Fetch data from stock

        for i, signal in enumerate(results):
            log.info("Stock history {0} scraping in progress... {1}/{2}"
                     .format(signal.name, i + 1, len(results)))
            data = stock_page.get_stock_information(signal.name,  include_history=True)
            scrape_data.append(data)
        #  endregion

    target_list = DtoList(name=list_name)
    target_board = DtoBoard(name=board_name)

    id_list = QList(service_trello_boards.get_board_lists(target_board)) \
        .first(lambda x: x.name == target_list.name).id

    for signal in scrape_data:
        parsed_labels = [l.id for l in QList(service_trello_boards.get_board_labels(target_board))
                         .where(lambda x: x.name in labels_list)]
        card_dto = DtoCard(
            name=str_stock_card_title_strategy.format(
                signal.name,
                clean_percentage_values(signal.change_percent),
                signal.last_price,
                0,
                0,
                sp.parameters['url'] + "/Stock/",
                signal.name,
                screener_name.upper(),
            ),
            desc='{0}{1}{2}'.format(
                str_stock_strategy_card.format(
                    screener_name,
                    signal.name,
                    DATETIME_FORMAT,
                    0,
                    0,
                    0,
                    0
                ),
                str_stock_card.format(
                    signal.name,
                    signal.last_price,
                    clean_percentage_values(signal.change_percent),
                    clean_percentage_values(signal.year_to_date),
                    signal.open,
                    signal.low,
                    signal.high
                ),
                str_stock_indicators_card.format(
                    signal.technical.support_1,
                    signal.technical.support_2,
                    signal.technical.resistance_1,
                    signal.technical.resistance_2,
                    clean_percentage_values(signal.technical.week_to_date),
                    clean_percentage_values(signal.technical.month_to_date),
                    clean_percentage_values(signal.technical.year_to_date)

                )
            ),
            idList=id_list,
            idLabels=parsed_labels,
            pos='top'

        )

        service_trello_cards.add_card(card_dto)


@app.task()
@notify_work()
@elastic_logging()
def update_cards_from_signals_screener_investagrams_sandbox(investagrams_id,
                                                            trello_id,
                                                            board_name,
                                                            list_name,
                                                            labels_list: []):
    #  region Get all existing cards in strategies

    stock_strategy_cards, id_list, target_board = get_board_data(trello_id, board_name, list_name, ['PSEI'])

    #  endregion

    #  region Get today's stock data

    with WebDriverFactory.create_webdriver(**apps_config[investagrams_id]['webdriver']) as driver:
        pl = PageInvestagramsLogin(driver=driver, source_id=investagrams_id)
        pl.login(pl.parameters['username'], pl.parameters['password'])

        stock_page = PageInvestegramsStock(driver=driver, source_id=investagrams_id)
        scrape_data = []

        for i, stock_card in enumerate(stock_strategy_cards):
            config_strategy = parse_configuration_from_desc(stock_card.desc)
            log.info("Stock history {0} scraping in progress... {1}/{2}"
                     .format(config_strategy['STRATEGY']['stock_name'], i + 1, len(stock_strategy_cards)))
            signal_date = config_strategy['STRATEGY']['signal_date']
            no_days_elapsed = days_between(signal_date.strftime('%Y-%m-%d'), DATETIME_FORMAT)
            if no_days_elapsed == 0:
                continue

            data = stock_page.get_stock_information(config_strategy['STRATEGY']['stock_name'],
                                                    include_history=True, days_history=no_days_elapsed)
            scrape_data.append((stock_card, config_strategy, data))

    #  endregion

    #  region Number crunching
    add_cards = []
    for stock_card, config_strategy, data in scrape_data:
        no_days_elapsed = days_between(str(config_strategy['STRATEGY']['signal_date']), DATETIME_FORMAT)
        if no_days_elapsed == 0:
            continue
        sliced_data_days_elapsed = data.historical[0: no_days_elapsed]
        total_growth = 0
        days_growth = 0
        days_stop = 0
        for index in range(0, len(sliced_data_days_elapsed)):
            computed = clean_percentage_values(sliced_data_days_elapsed[index].change_percent)
            total_growth = total_growth + computed
            if total_growth <= stock_page.parameters['risk_percentage']:
                days_stop = index + 1
            if total_growth >= stock_page.parameters['growth_percentage']:
                days_growth = index + 1

        #  region Set strategy data

        config_strategy['STRATEGY']['days_elapsed'] = no_days_elapsed
        config_strategy['STRATEGY']['growth_percent_from_signal_date'] = round(total_growth, 2)
        config_strategy['STRATEGY']['days_elapsed_to_stop'] = days_stop
        config_strategy['STRATEGY']['days_elapsed_to_target'] = days_growth

        #  endregion

        add_cards.append((stock_card, config_strategy, data))

    #  endregion

    #  region Update Cards
    service_trello_cards = ApiServiceCards(trello_id)
    service_trello_boards = ApiServiceBoards(trello_id)

    parsed_labels = [l.id for l in QList(service_trello_boards.get_board_labels(target_board))
        .where(lambda x: x.name in labels_list)]
    for stock_card, config_strategy, data in add_cards:
        card_dto = DtoCard(
            id=stock_card.id,
            name=str_stock_card_title_strategy.format(
                data.name,
                clean_percentage_values(data.change_percent),
                data.last_price,
                config_strategy['STRATEGY']['days_elapsed'],
                config_strategy['STRATEGY']['growth_percent_from_signal_date'],
                stock_page.parameters['url'] + "/Stock/",
                data.name,
                config_strategy['STRATEGY']['name'].upper(),
            ),
            desc='{0}{1}{2}'.format(
                str_stock_strategy_card.format(
                    config_strategy['STRATEGY']['name'],
                    data.name,
                    DATETIME_FORMAT,
                    config_strategy['STRATEGY']['growth_percent_from_signal_date'],
                    config_strategy['STRATEGY']['days_elapsed'],
                    config_strategy['STRATEGY']['days_elapsed_to_stop'],
                    config_strategy['STRATEGY']['days_elapsed_to_target']
                ),
                str_stock_card.format(
                    data.name,
                    data.last_price,
                    clean_percentage_values(data.change_percent),
                    clean_percentage_values(data.year_to_date),
                    data.open,
                    data.low,
                    data.high
                ),
                str_stock_indicators_card.format(
                    data.technical.support_1,
                    data.technical.support_2,
                    data.technical.resistance_1,
                    data.technical.resistance_2,
                    clean_percentage_values(data.technical.week_to_date),
                    clean_percentage_values(data.technical.month_to_date),
                    clean_percentage_values(data.technical.year_to_date)
                )
            ),
            idList=id_list.id,
            id_labels=parsed_labels,
            pos='bottom'

        )

        service_trello_cards.update_card(card_dto)

    #  endregion


@app.task()
@holidays_aware()
@notify_work(notify_success=True)
@elastic_logging()
def add_signals_screener_investagrams_sandbox_to_elastic(investagrams_id, elastic_id, index_screener_name: str):
    scrape_data = []
    with WebDriverFactory.create_webdriver(**apps_config[investagrams_id]['webdriver']) as driver:
        pl = PageInvestagramsLogin(driver=driver, source_id=investagrams_id)
        pl.login(pl.parameters['username'], pl.parameters['password'])

        sp = PageInvestagramsScreener(driver=driver, source_id=investagrams_id)
        sp.select_screener(index_screener_name)
        results = sp.get_all_results()

        stock_page = PageInvestegramsStock(driver=driver, source_id=investagrams_id)

        #  region Fetch data from stock

        for i, signal in enumerate(results):
            signal.date = DATETIME_FORMAT
            log.info("Stock history {0} scraping in progress... {1}/{2}"
                     .format(signal.name, i + 1, len(results)))
            data = stock_page.get_stock_information(signal.name, include_history=True, days_history=1)

            last_trading_date = datetime.strptime(data.historical[0].date, '%b %d, %Y').strftime('%Y-%m-%d')
            days_last_traded = days_between(last_trading_date, DATETIME_FORMAT)
            if days_last_traded > 1:
                #  detect if stock is suspended
                continue

            scrape_data.append((data, signal))
        #  endregion

    index_name = '{0}'.format(INDEX_ROOT_NAME_SCREENER).lower()

    for data, signal in scrape_data:

        strategy_push = DtoPSEIScreenerStrategy(
            strategy_name=index_screener_name,
            stock_name=signal.name,
            signal_date=signal.date,
            days_elapsed=0,
            growth_percent_from_signal_date=0,
            days_elapsed_to_stop=0,
            days_elapsed_to_target=0
        )

        try:
            send_json_data_to_elastic_server(app_config_name=elastic_id,
                                             json_dump={**data.get_dict(), **strategy_push.get_dict()},
                                             use_interval_map=False,
                                             index_name=index_name,
                                             location_key='{0}_{1}_{2}'.format(
                                                 index_name,
                                                 index_screener_name.replace(' ', '_').lower(),
                                                 signal.name),
                                             identifier=DATETIME_FORMAT)
        except AssertionError:
            log.warning('Failed to add stock: {0}'.format(signal.name))
            continue


@app.task()
@holidays_aware()
@notify_work(notify_success=True)
@elastic_logging()
def update_signals_screener_investagrams_sandbox_to_elastic(investagrams_id,
                                                            elastic_id,
                                                            days_to_update=2,
                                                            enable_fast_history=False,
                                                            days_search=90):
    #  region Get all existing cards in strategies

    index_name = '{0}'.format(INDEX_ROOT_NAME_SCREENER).lower()

    stock_strategy_locs = get_index_data_from_elastic(index_name=index_name,
                                                      app_config_name=elastic_id,
                                                      type_hook=DtoStockInvestagrams)
    stock_strategy_locs = QList(stock_strategy_locs)\
        .where(lambda x: days_between(x.signal_date[0:10], DATETIME_FORMAT) < days_to_update)
    stock_strategy_locs.sort(key=lambda x: x.days_elapsed)

    #  endregion

    with WebDriverFactory.create_webdriver(**apps_config[investagrams_id]['webdriver']) as driver:
        pl = PageInvestagramsLogin(driver=driver, source_id=investagrams_id)
        pl.login(pl.parameters['username'], pl.parameters['password'])

        stock_page = PageInvestegramsStock(driver=driver, source_id=investagrams_id)
        scrape_data = []
        for i, stock_card in enumerate(stock_strategy_locs):
            try:

                #  region Get today's stock data

                signal_date = stock_card.signal_date[0:10]
                no_days_elapsed = days_between(signal_date, DATETIME_FORMAT)

                print("Stock history {0} scraping in progress... {1}/{2}"
                         .format(stock_card.name, i + 1, len(stock_strategy_locs)))
                log.info("Stock history {0} scraping in progress... {1}/{2}"
                         .format(stock_card.name, i + 1, len(stock_strategy_locs)))
                try:
                    days_history = (no_days_elapsed + 1) if enable_fast_history else days_search
                    data = stock_page.get_stock_information(stock_card.name, include_history=True,
                                                            days_history=days_history)
                    scrape_data.append((stock_card, data))
                except:
                    log.warning("Stock history {0} scraping failed.".format(stock_card.name))
                    continue

                #  endregion

                #  region Number Crunching

                sliced_data_days_elapsed = data.historical[0: no_days_elapsed]
                total_growth = 0
                days_growth = 0
                days_stop = 0

                stop_target = False
                for index in range(0, len(sliced_data_days_elapsed)):
                    computed = sliced_data_days_elapsed[index].change_percent
                    total_growth = total_growth + computed
                    """
                    if total_growth <= stock_page.parameters['risk_percentage']:
                        days_stop = index + 1
                    if total_growth >= stock_page.parameters['growth_percentage']:
                        days_growth = index + 1
                    """
                    if not stop_target:
                        if data.technical.support_2 >= sliced_data_days_elapsed[index].last_price:
                            days_stop = index + 1
                            stop_target = True
                        if data.technical.resistance_1 <= sliced_data_days_elapsed[index].last_price:
                            days_growth = index + 1
                            stop_target = True

                #  endregion

                #  region Set strategy data

                strategy_push = DtoPSEIScreenerStrategy(
                    strategy_name=stock_card.strategy_name,
                    stock_name=stock_card.name,
                    signal_date=signal_date,
                    days_elapsed=no_days_elapsed,
                    growth_percent_from_signal_date=round(total_growth, 2),
                    days_elapsed_to_stop=days_stop,
                    days_elapsed_to_target=days_growth
                )

                #  endregion

                #  region Update Indexes

                send_json_data_to_elastic_server(app_config_name=elastic_id,
                                                 json_dump={**data.get_dict(), **strategy_push.get_dict()},
                                                 index_name=index_name,
                                                 use_interval_map=False,
                                                 location_key='{0}_{1}_{2}'.format(
                                                     index_name,
                                                     strategy_push.strategy_name.replace(' ', '_').lower(),
                                                     stock_card.name),
                                                 identifier=stock_card.signal_date)

                #  endregion

                log.info("Updated index location for {0} {1}".format(stock_card.name, stock_card.signal_date))

            except Exception:
                log.warning("Failed to update location for {0} {1}".format(stock_card.name, stock_card.signal_date))


def load_signals_screener_investagrams_sandbox_csv(investagrams_id,
                                                   csv_file,
                                                   trello_id,
                                                   board_name,
                                                   list_name,
                                                   labels_list: []):


    with WebDriverFactory.create_webdriver(**apps_config[investagrams_id]['webdriver']) as driver:
        pl = PageInvestagramsLogin(driver=driver, source_id=investagrams_id)
        pl.login(pl.parameters['username'], pl.parameters['password'])

        service_trello_cards = ApiServiceCards(trello_id)
        service_trello_boards = ApiServiceBoards(trello_id)

        stock_page = PageInvestegramsStock(driver=driver, source_id=investagrams_id)
        scrape_data = []
        #  region Fetch data from csv
        data_csv_signals = generate_objects_from_csv_data(csv_file, DtoPSEIScreenerStrategy)
        for i, signal in enumerate(data_csv_signals):
            log.info("Stock history {0} scraping in progress... {1}/{2}"
                     .format(signal.stock_name, i + 1, len(data_csv_signals)))

            data = stock_page.get_stock_information(signal.stock_name, include_history=False)
            scrape_data.append((data, signal))
        #  endregion


    target_list = DtoList(name=list_name)
    target_board = DtoBoard(name=board_name)

    id_list = QList(service_trello_boards.get_board_lists(target_board)) \
        .first(lambda x: x.name == target_list.name).id

    for signal, system in scrape_data:
        parsed_labels = [l.id for l in QList(service_trello_boards.get_board_labels(target_board))
            .where(lambda x: x.name in labels_list)]
        card_dto = DtoCard(
            name=str_stock_card_title_strategy.format(
                signal.name,
                clean_percentage_values(signal.change_percent),
                signal.last_price,
                0,
                0,
                stock_page.parameters['url'] + "/Stock/",
                signal.name,
                system.name.upper()
            ),
            desc='{0}{1}{2}'.format(
                str_stock_strategy_card.format(
                    system.name,
                    signal.name,
                    system.signal_date,
                    0,
                    0,
                    0,
                    0
                ),
                str_stock_card.format(
                    signal.name,
                    signal.last_price,
                    clean_percentage_values(signal.change_percent),
                    clean_percentage_values(signal.year_to_date),
                    signal.open,
                    signal.low,
                    signal.high
                ),
                str_stock_indicators_card.format(
                    signal.technical.support_1,
                    signal.technical.support_2,
                    signal.technical.resistance_1,
                    signal.technical.resistance_2,
                    clean_percentage_values(signal.technical.week_to_date),
                    clean_percentage_values(signal.technical.month_to_date),
                    clean_percentage_values(signal.technical.year_to_date)

                )
            ),
            idList=id_list,
            idLabels=parsed_labels,
            pos='top'

        )

        service_trello_cards.add_card(card_dto)


def load_signals_screener_investagrams_sandbox_csv_to_elastic(investagrams_id,
                                                              elastic_id,
                                                              csv_file):
    driver = WebDriverFactory.get_web_driver_instance(**apps_config[investagrams_id]['webdriver'])
    pl = PageInvestagramsLogin(driver=driver, source_id=investagrams_id)
    pl.login(pl.parameters['username'], pl.parameters['password'])

    stock_page = PageInvestegramsStock(driver=driver, source_id=investagrams_id)
    scrape_data = []
    #  region Fetch data from csv
    data_csv_signals = generate_objects_from_csv_data(csv_file, DtoPSEIScreenerStrategy)
    for i, signal in enumerate(data_csv_signals):
        log.info("Stock history {0} scraping in progress... {1}/{2}"
                 .format(signal.stock_name, i + 1, len(data_csv_signals)))

        data = stock_page.get_stock_information(signal.stock_name, include_history=False)
        scrape_data.append((data, signal))

    #  endregion
    stock_page.driver.close()

    index_name = '{0}'.format(INDEX_ROOT_NAME_SCREENER).lower()

    for signal, system in scrape_data:
        strategy_push = DtoPSEIScreenerStrategy(
            strategy_name=system.strategy_name,
            stock_name=system.stock_name,
            signal_date=system.signal_date,
            days_elapsed=0,
            growth_percent_from_signal_date=0,
            days_elapsed_to_stop=0,
            days_elapsed_to_target=0
        )
        try:
            send_json_data_to_elastic_server(app_config_name=elastic_id,
                                             json_dump={**signal.get_dict(), **strategy_push.get_dict()},
                                             index_name=index_name,
                                             use_interval_map=False,
                                             location_key='{0}_{1}_{2}'.format(
                                                 index_name,
                                                 system.strategy_name.replace(' ', '_').lower(),
                                                 signal.name),
                                             identifier=system.signal_date)
        except AssertionError:
            log.warning("Unable to add data: {0}{1}".format(index_name, system.stock_name))
