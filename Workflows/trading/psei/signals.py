from Applications import *
from Workflows.trading.psei.settings import *


@app.task()
@notify_work()
@elastic_logging()
def add_cards_from_signals_screener_investagrams(investagrams_id,
                                                 trello_id,
                                                 screener_name,
                                                 board_name,
                                                 list_name,
                                                 labels_list: []):

    driver = WebDriverFactory.get_web_driver_instance(**apps_config[investagrams_id]['webdriver'])
    pl = PageInvestagramsLogin(driver=driver, source_id=investagrams_id)
    pl.login(pl.parameters['username'], pl.parameters['password'])

    sp = PageInvestagramsScreener(driver=driver, source_id=investagrams_id)
    sp.select_screener(screener_name)
    results = sp.get_all_results()

    service_trello_cards = ApiServiceCards(trello_id)
    service_trello_boards = ApiServiceBoards(trello_id)

    stock_page = PageInvestegramsStock(driver=driver, source_id=investagrams_id)
    scrape_data = []
    #  region fetch data from stock
    for i, signal in enumerate(results):
        log.info("Stock history {0} scraping in progress... {1}/{2}"
                 .format(signal.name, i + 1, len(results) + 1))
        data = stock_page.get_stock_information(signal.name,  include_history=True)
        scrape_data.append(data)
    #  endregion
    stock_page.driver.close()

    target_list = DtoList(name=list_name)
    target_board = DtoBoard(name=board_name)

    id_list = QList(service_trello_boards.get_board_lists(target_board)) \
        .first(lambda x: x.name == target_list.name).id

    for signal in scrape_data:
        parsed_labels = [l.id for l in QList(service_trello_boards.get_board_labels(target_board))
                         .where(lambda x: x.name in labels_list)]
        card_dto = DtoCard(
            name=str_stock_card_title.format(
                signal.name,
                re.search('\(([^)]+)', signal.change_percent).group(1),
                signal.last_price,
                sp.parameters['url'] + "/Stock/",
                signal.name,
                screener_name.upper(),
            ),
            desc='{0}{1}{2}'.format(
                str_stock_card.format(
                    screener_name,
                    signal.last_price,
                    signal.change_percent,
                    signal.year_to_date,
                    signal.open,
                    signal.low,
                    signal.high
                ),
                str_stock_indicators_card.format(
                    signal.technical.support_1,
                    signal.technical.support_2,
                    signal.technical.resistance_1,
                    signal.technical.resistance_2,
                    signal.technical.week_to_date,
                    signal.technical.month_to_date,
                    signal.technical.year_to_date

                ),
                str_stock_trade_card.format(
                    'NA',
                    'NA',
                    'NA',
                    'NA',
                    'NA',
                    'NA',
                    'NA',
                    'NA',
                    'NA',
                    'NA',
                    'NA',
                    'NA'
                )
            ),
            idList=id_list,
            idLabels=parsed_labels,
            pos='top'

        )

        service_trello_cards.add_card(card_dto)


