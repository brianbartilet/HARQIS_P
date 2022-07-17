from Applications import *
from Workflows.trading.psei.settings import *
from Workflows.workday import *

from Core.utilities.celery_helper import *

from win32api import GetSystemMetrics
from datetime import datetime, timedelta
from dateutil import tz, parser
import re, itertools


@app.task()
@initialize_hud_configuration(source_id='Rainmeter', hud_item_name='Daily Dashboard')
def update_dashboard_trello_current_cards_info(trello_id, board_name, ini=ConfigHelperRainmeter()):
    board_url = "https://trello.com/b/V8NK6Wnm/daily-dashboard"

    service_board = ApiServiceBoards(source_id=trello_id)
    service_lists = ApiServiceLists(trello_id)

    list_current = QList(service_board.get_board_lists(board=DtoBoard(name=board_name)))\
        .where(lambda x: x.name == 'EXECUTE')\
        .first()

    dump = ''
    current_cards = service_lists.get_all_cards_from_list(list_current)[0:8]
    for card_ in current_cards:
        dump = dump + '- {0}\n'.format((card_.name[:25] + '..') if len(card_.name) > 25 else card_.name)

    ini['Variables']['ItemLines'] = '{0}'.format(len(current_cards))

    ini['meterLink']['text'] = "Board"
    ini['meterLink']['leftmouseupaction'] = '!Execute ["{0}" 3]'.format(board_url)
    ini['meterLink']['tooltiptext'] = board_url

    ini['MeterDisplay']['W'] = '180'
    ini['MeterDisplay']['H'] = '180'

    return dump


@app.task()
@initialize_hud_configuration(source_id='Rainmeter', hud_item_name='Reminders')
def update_dashboard_trello_current_cards_info_reminders(trello_id, board_name, ini=ConfigHelperRainmeter()):
    board_url = "https://trello.com/b/V8NK6Wnm/daily-dashboard"

    service_board = ApiServiceBoards(source_id=trello_id)
    service_lists = ApiServiceLists(trello_id)

    list_current = QList(service_board.get_board_lists(board=DtoBoard(name=board_name)))\
        .where(lambda x: x.name == 'REMINDERS')\
        .first()

    dump = ''
    current_cards = service_lists.get_all_cards_from_list(list_current)[0:8]
    for card_ in current_cards:
        dump = dump + '- {0}\n'.format((card_.desc[:25] + '..') if len(card_.desc) > 25 else card_.desc)

    ini['Variables']['ItemLines'] = '{0}'.format(len(current_cards) + 2)
    ini['meterLink']['text'] = "Board"
    ini['meterLink']['leftmouseupaction'] = '!Execute ["{0}" 3]'.format(board_url)
    ini['meterLink']['tooltiptext'] = board_url

    ini['MeterDisplay']['W'] = '180'
    ini['MeterDisplay']['H'] = '150'

    return dump


@app.task()
@initialize_hud_configuration(source_id='Rainmeter', hud_item_name='Daily Trading FOREX', play_sound=True,
                              new_sections_dict={
                                  'meterLink_broker': 17,
                                  'meterLink_news': 18,
                                  'meterLink_metrics': 19,
                                }
                              )
def update_dashboard_trello_current_cards_info_trading(oanda_id, ini=ConfigHelperRainmeter()):

    board_url = "https://trello.com/b/351MWTYe/daily-dashboard-trading"

    service = ApiServiceAccount(oanda_id)
    account_use = QList(service.get_account_info().accounts)\
        .where(lambda x: x.mt4AccountID == service.parameters['mt4AccountID'])\
        .first()

    account_details = service.get_account_details(account_use.id)

    service_trades = ApiServiceTrades(oanda_id)
    open_trades = service_trades.get_trades_from_account(account_use.id)

    ini['Variables']['ItemLines'] = '{0}'.format(len(open_trades) + 2)
    ini['meterLink']['text'] = "Board"
    ini['meterLink']['leftmouseupaction'] = '!Execute ["{0}" 3]'.format(board_url)
    ini['meterLink']['tooltiptext'] = board_url

    #  region Section: meterLink_broker
    broker_url = 'https://trade.oanda.com/'
    ini['meterLink_broker']['Meter'] = 'String'
    ini['meterLink_broker']['MeterStyle'] = 'sItemLink'
    ini['meterLink_broker']['X'] = '(40*#Scale#)'
    ini['meterLink_broker']['Y'] = '(38*#Scale#)'
    ini['meterLink_broker']['W'] = '181'
    ini['meterLink_broker']['H'] = '14'
    ini['meterLink_broker']['StringStyle'] = 'Italic'
    ini['meterLink_broker']['Text'] = '|Broker'
    ini['meterLink_broker']['LeftMouseUpAction'] = '!Execute["{0}" 3]'.format(broker_url)
    #  endregion

    #  region Section: meterLink_news
    news_url = 'https://www.myfxbook.com/forex-economic-calendar'
    ini['meterLink_news']['Meter'] = 'String'
    ini['meterLink_news']['MeterStyle'] = 'sItemLink'
    ini['meterLink_news']['X'] = '(82*#Scale#)'
    ini['meterLink_news']['Y'] = '(38*#Scale#)'
    ini['meterLink_news']['W'] = '181'
    ini['meterLink_news']['H'] = '14'
    ini['meterLink_news']['StringStyle'] = 'Italic'
    ini['meterLink_news']['Text'] = '|News'
    ini['meterLink_news']['LeftMouseUpAction'] = '!Execute["{0}" 3]'.format(news_url)
    #  endregion

    #  region Section: meterlink_metrics
    url = 'http://localhost:3001/'
    ini['meterLink_metrics']['Meter'] = 'String'
    ini['meterLink_metrics']['MeterStyle'] = 'sItemLink'
    ini['meterLink_metrics']['X'] = '(112*#Scale#)'
    ini['meterLink_metrics']['Y'] = '(38*#Scale#)'
    ini['meterLink_metrics']['W'] = '181'
    ini['meterLink_metrics']['H'] = '14'
    ini['meterLink_metrics']['StringStyle'] = 'Italic'
    ini['meterLink_metrics']['Text'] = '|Metrics'
    ini['meterLink_metrics']['LeftMouseUpAction'] = '!Execute["{0}" 3]'.format(url)
    #  endregion

    ini['MeterDisplay']['W'] = '180'
    ini['MeterDisplay']['H'] = '300'

    dump = '{0}  {1}  $ {2:>10}\n'.format("TOTAL:", "UPL ", round(float(account_details.unrealized_pl), 2))
    for trade in open_trades:
        unrealized_profit_loss = round(float(trade.unrealized_pl), 2)
        dump = dump + '{0}  {1}  $ {2:>10}\n'.format(str(trade.instrument).replace('_', ''),
                                                     'SELL'if '-' in str(trade.current_units) else 'BUY ',
                                                     '{0}{1}'.format('+' if '-' not in str(unrealized_profit_loss)
                                                                     else '',
                                                     str(round(unrealized_profit_loss, 2))),
                                               )

    return dump


@app.task()
@initialize_hud_configuration(source_id='Rainmeter', hud_item_name='Peon Stuff', reset_alerts_secs=30, always_alert=True,
                              new_sections_dict={
                                  'meterLink_site': 17,
                                  'meterLink_run': 18,
                                  'meterLink_health': 19,
                                  'meterLink_jira': 20,
                                }
                              )
def update_dashboard_oracle_timesheet(oracle_id, ini=ConfigHelperRainmeter()):

    app_url = "https://appswtwprod.willistowerswatson.com/"
    ini['meterLink']['text'] = "Site"
    ini['meterLink']['leftmouseupaction'] = '!Execute ["{0}" 3]'.format(app_url)
    ini['meterLink']['tooltiptext'] = "Site"
    ini['meterLink']['W'] = '181'
    ini['meterLink']['H'] = '14'

    #  region Section: meterLink_site
    config = apps_config[ENV_CURRENT_CONFIGURATION_FILE_PATH]
    ini['meterLink_site']['tooltiptext'] = config
    ini['meterLink_site']['Meter'] = 'String'
    ini['meterLink_site']['MeterStyle'] = 'sItemLink'
    ini['meterLink_site']['X'] = '(34*#Scale#)'
    ini['meterLink_site']['Y'] = '(38*#Scale#)'
    ini['meterLink_site']['W'] = '181'
    ini['meterLink_site']['H'] = '14'
    ini['meterLink_site']['StringStyle'] = 'Italic'
    ini['meterLink_site']['Text'] = '|Config'
    ini['meterLink_site']['LeftMouseUpAction'] = '!Execute["{0}" 3]'.format(config)
    #  endregion

    #  region Section: meterLink_run
    path = os.path.join(ENV_ROOT_DIRECTORY, 'DailyDashboard', 'hud_run_oracle.bat')
    ini['meterLink_run']['tooltiptext'] = path
    ini['meterLink_run']['Meter'] = 'String'
    ini['meterLink_run']['MeterStyle'] = 'sItemLink'
    ini['meterLink_run']['X'] = '(76*#Scale#)'
    ini['meterLink_run']['Y'] = '(38*#Scale#)'
    ini['meterLink_run']['W'] = '181'
    ini['meterLink_run']['H'] = '14'
    ini['meterLink_run']['StringStyle'] = 'Italic'
    ini['meterLink_run']['Text'] = '|Run'
    ini['meterLink_run']['LeftMouseUpAction'] = '!Execute["{0}" 3]'.format(path)
    #  endregion

    #  region Section: meterLink_health
    path = os.path.join(ENV_ROOT_DIRECTORY, 'DailyDashboard', 'hud_run_healthsheet.bat')
    ini['meterLink_health']['tooltiptext'] = path
    ini['meterLink_health']['Meter'] = 'String'
    ini['meterLink_health']['MeterStyle'] = 'sItemLink'
    ini['meterLink_health']['X'] = '(100*#Scale#)'
    ini['meterLink_health']['Y'] = '(38*#Scale#)'
    ini['meterLink_health']['W'] = '181'
    ini['meterLink_health']['H'] = '14'
    ini['meterLink_health']['StringStyle'] = 'Italic'
    ini['meterLink_health']['Text'] = '|Health'
    ini['meterLink_health']['LeftMouseUpAction'] = '!Execute["{0}" 3]'.format(path)
    #  endregion

    #  region Section: meterLink_jira
    url = "https://tasjira.internal.towerswatson.com:8443/secure/RapidBoard.jspa?rapidView=1013&useStoredSettings=true"
    ini['meterLink_jira']['tooltiptext'] = path
    ini['meterLink_jira']['Meter'] = 'String'
    ini['meterLink_jira']['MeterStyle'] = 'sItemLink'
    ini['meterLink_jira']['X'] = '(142*#Scale#)'
    ini['meterLink_jira']['Y'] = '(38*#Scale#)'
    ini['meterLink_jira']['W'] = '181'
    ini['meterLink_jira']['H'] = '14'
    ini['meterLink_jira']['StringStyle'] = 'Italic'
    ini['meterLink_jira']['Text'] = '|Jira'
    ini['meterLink_jira']['LeftMouseUpAction'] = '!Execute["{0}" 3]'.format(url)
    #  endregion

    ini['MeterDisplay']['W'] = '180'
    ini['MeterDisplay']['H'] = '220'

    oracle_config = apps_config[oracle_id]['parameters']['timesheet']
    dump = ''
    for day in oracle_config:
        dump = dump + '[{2}]\n{0} {1}hrs\n'.format(day, oracle_config[day]['hours'], oracle_config[day]['project'])

    ini['Variables']['ItemLines'] = '{0}'.format(len(oracle_config) * 2.5)

    return dump


@app.task()
@initialize_hud_configuration(source_id='Rainmeter', hud_item_name='YNAB Budget Warn')
def get_current_budget_info(ynab_id, budget_percent_warning=20, ini=ConfigHelperRainmeter()):

    budget_service = ApiServiceYNABBudgets(ynab_id)
    budgets = budget_service.get_budgets()
    budget_target = QList(budgets['budgets'])\
        .where(lambda x: x['name'] == budget_service.parameters['budget_name'])\
        .first()

    service = ApiServiceYNABCategories(ynab_id)
    category_groups = service.get_categories(budget_target['id'])['category_groups']

    dump = ''
    categories_fetched = []
    for category_group in category_groups:
        for category in category_group['categories']:
            category_name = category['name']
            budgeted = category['budgeted']
            budgeted_warning = budgeted * (budget_percent_warning/100)
            balance = category['balance']
            if balance < 0:
                category_name = (category_name[0:12] + '..') if len(category_name) > 15 else category_name
                categories_fetched.append(category_name)
                dump = dump + '{0:<15} {1:>14}\n'.format(category_name, round(balance/1000, 2))

    app_url = "https://app.youneedabudget.com/"
    ini['Variables']['ItemLines'] = '{0}'.format(len(categories_fetched) + 2)
    ini['meterLink']['text'] = "Site"
    ini['meterLink']['leftmouseupaction'] = '!Execute ["{0}" 3]'.format(app_url)
    ini['meterLink']['tooltiptext'] = app_url

    ini['MeterDisplay']['W'] = '180'
    ini['MeterDisplay']['H'] = '300'
    
    return dump


@app.task()
@initialize_hud_configuration(source_id='Rainmeter', hud_item_name='Quick Links',
                              new_sections_dict={
                                  'meterLink_kibana': 17,
                                  'meterLink_console': 18,
                                  'meterLink_harqis': 19,
                                  'meterLink_runHarqis': 20,
                                  'meterLink_runHarqisQueue': 21,
                                }
                              )
def update_quick_links(ini=ConfigHelperRainmeter()):

    dump = ''
    ini['Variables']['ItemLines'] = '10'
    ini['MeterDisplay']['W'] = '180'
    ini['MeterDisplay']['H'] = '100'

    #  region Link: Cluster Tabs
    cmd = 'chrome chrome-extension://aadahadfdmiibmdhfmpbeeebejmjnkef/manager.html#saved'
    ini['meterLink']['text'] = "Cluster Tabs"
    ini['meterLink']['leftmouseupaction'] = '{0}'.format(cmd)
    ini['meterLink']['tooltiptext'] = cmd
    #  endregion

    #  region Link: meterLink_kibana
    url = 'https://7854e3b6326545c983580dd605cf191e.eastus2.azure.elastic-cloud.com:9243/app/home#/'
    ini['meterLink_kibana']['tooltiptext'] = url
    ini['meterLink_kibana']['Meter'] = 'String'
    ini['meterLink_kibana']['MeterStyle'] = 'sItemLink'
    ini['meterLink_kibana']['X'] = '(9*#Scale#)'
    ini['meterLink_kibana']['Y'] = '(50*#Scale#)'
    ini['meterLink_kibana']['W'] = '181'
    ini['meterLink_kibana']['H'] = '14'
    ini['meterLink_kibana']['StringStyle'] = 'Italic'
    ini['meterLink_kibana']['Text'] = 'Kibana Backend'
    ini['meterLink_kibana']['LeftMouseUpAction'] = '!Execute["{0}" 3]'.format(url)
    #  endregion

    #  region Link: meterLink_console
    url = 'https://7854e3b6326545c983580dd605cf191e.eastus2.azure.elastic-cloud.com:9243/app/dev_tools#/console'
    ini['meterLink_console']['tooltiptext'] = url
    ini['meterLink_console']['Meter'] = 'String'
    ini['meterLink_console']['MeterStyle'] = 'sItemLink'
    ini['meterLink_console']['X'] = '(9*#Scale#)'
    ini['meterLink_console']['Y'] = '(64*#Scale#)'
    ini['meterLink_console']['W'] = '181'
    ini['meterLink_console']['H'] = '14'
    ini['meterLink_console']['StringStyle'] = 'Italic'
    ini['meterLink_console']['Text'] = 'Kibana Console'
    ini['meterLink_console']['LeftMouseUpAction'] = '!Execute["{0}" 3]'.format(url)
    #  endregion

    #  region Link: meterLink_harqis
    url = 'http://localhost:3001/'
    ini['meterLink_harqis']['tooltiptext'] = url
    ini['meterLink_harqis']['Meter'] = 'String'
    ini['meterLink_harqis']['MeterStyle'] = 'sItemLink'
    ini['meterLink_harqis']['X'] = '(9*#Scale#)'
    ini['meterLink_harqis']['Y'] = '(78*#Scale#)'
    ini['meterLink_harqis']['W'] = '181'
    ini['meterLink_harqis']['H'] = '14'
    ini['meterLink_harqis']['StringStyle'] = 'Italic'
    ini['meterLink_harqis']['Text'] = 'HARQIS Dashboard'
    ini['meterLink_harqis']['LeftMouseUpAction'] = '!Execute["{0}" 3]'.format(url)
    #  endregion

    #  region Section: meterLink_runHarqis
    path = os.path.join(ENV_ROOT_DIRECTORY, 'DailyDashboard/tasks/scripts', 'run.bat')
    ini['meterLink_runHarqis']['Meter'] = 'String'
    ini['meterLink_runHarqis']['MeterStyle'] = 'sItemLink'
    ini['meterLink_runHarqis']['X'] = '(9*#Scale#)'
    ini['meterLink_runHarqis']['Y'] = '(92*#Scale#)'
    ini['meterLink_runHarqis']['W'] = '181'
    ini['meterLink_runHarqis']['H'] = '14'
    ini['meterLink_runHarqis']['StringStyle'] = 'Italic'
    ini['meterLink_runHarqis']['Text'] = 'HARQIS Run'
    ini['meterLink_runHarqis']['LeftMouseUpAction'] = '!Execute["{0}" 3]'.format(path)
    #  endregion

    #  region Section: meterLink_runHarqisQueue
    url = 'http://localhost:15672/#/'
    ini['meterLink_runHarqisQueue']['Meter'] = 'String'
    ini['meterLink_runHarqisQueue']['MeterStyle'] = 'sItemLink'
    ini['meterLink_runHarqisQueue']['X'] = '(9*#Scale#)'
    ini['meterLink_runHarqisQueue']['Y'] = '(106*#Scale#)'
    ini['meterLink_runHarqisQueue']['W'] = '181'
    ini['meterLink_runHarqisQueue']['H'] = '14'
    ini['meterLink_runHarqisQueue']['StringStyle'] = 'Italic'
    ini['meterLink_runHarqisQueue']['Text'] = 'HARQIS Queue'
    ini['meterLink_runHarqisQueue']['LeftMouseUpAction'] = '!Execute["{0}" 3]'.format(url)
    #  endregion

    return dump


@app.task()
@initialize_hud_configuration(source_id='Rainmeter', hud_item_name='Upcoming')
def update_dashboard_messages_upcoming(path='celerybeat-schedule', ini=ConfigHelperRainmeter()):

    tasks_map = get_upcoming_scheduler_tasks(path=path)
    now = datetime.now()

    #upcoming = QList(tasks_map).where(lambda x: x[1] <= now + timedelta(days=2))
    #upcoming = QList(tasks_map).where(lambda x: now - timedelta(days=2) <= x[1] <= now + timedelta(days=2))
    upcoming = QList(tasks_map).where(lambda x: now <= x[1] <= now + timedelta(days=2))

    dump = ''
    channel_url = 'https://docs.celeryproject.org/en/stable/reference/celery.schedules.html'

    for job, next_run in upcoming:
        time_next_run = next_run.strftime('%Y-%m-%d %I:%M %p')
        j = (job[:25] + '..') if len(job) > 25 else job
        dump = dump + '{0}\n {1}\n'.format(time_next_run, j)

    ini['Variables']['ItemLines'] = '{0}'.format(2 + (len(upcoming) * 3))
    ini['meterLink']['text'] = "Channel"
    ini['meterLink']['leftmouseupaction'] = '!Execute ["{0}" 3]'.format(channel_url)
    ini['meterLink']['tooltiptext'] = channel_url
    ini['MeterDisplay']['W'] = '180'
    ini['MeterDisplay']['H'] = '500'

    return dump




@app.task()
@initialize_hud_configuration(source_id='Rainmeter', hud_item_name='Recent Messages')
def update_dashboard_messages(messages_id, ini=ConfigHelperRainmeter()):

    service_notifications = CurlServicePushNotifications(source_id=messages_id)

    recent_messages = service_notifications.get_notifications()['messages'][0:5]

    dump = ''
    channel_url = '{0}/{1}'.format(apps_config[messages_id]['curl']['base_url'], service_notifications.notification_id)

    for message in recent_messages:
        here = parser.parse(message['time']).strftime('%Y-%m-%d %I:%M %p')

        dump = dump + '{0}\n {1}\n'.format(here, (message['message'][:25] + '..') if len(message['message']) > 25 else message['message'])

    ini['Variables']['ItemLines'] = '{0}'.format(len(recent_messages) + 4)
    ini['meterLink']['text'] = "Channel"
    ini['meterLink']['leftmouseupaction'] = '!Execute ["{0}" 3]'.format(channel_url)
    ini['meterLink']['tooltiptext'] = channel_url
    ini['MeterDisplay']['W'] = '180'
    ini['MeterDisplay']['H'] = '500'

    return dump


@app.task()
@initialize_hud_configuration(source_id='Rainmeter', hud_item_name='Recent Failed')
def update_dashboard_messages_failed(messages_id, ini=ConfigHelperRainmeter()):

    service_notifications = CurlServicePushNotifications(source_id=messages_id)

    recent_messages = QList(service_notifications.get_notifications()['messages'])\
        .where(lambda x: 'FAILED' in x['message'])[0:5]
    #recent_messages = []

    dump = ''
    channel_url = '{0}/{1}'.format(apps_config[messages_id]['curl']['base_url'], service_notifications.notification_id)

    for message in recent_messages:
        here = parser.parse(message['time']).strftime('%Y-%m-%d %I:%M %p')

        dump = dump + '{0}\n{1}\n'.format(here, message['message'].replace('FAILED: ', '').replace('-', ''))

    ini['Variables']['ItemLines'] = '{0}'.format(2 + (len(recent_messages) * 3))
    ini['meterLink']['text'] = "Channel"
    ini['meterLink']['leftmouseupaction'] = '!Execute ["{0}" 3]'.format(channel_url)
    ini['meterLink']['tooltiptext'] = channel_url
    ini['MeterDisplay']['W'] = '180'
    ini['MeterDisplay']['H'] = '900'

    return dump


@app.task()
@holidays_aware()
@initialize_hud_configuration(source_id='Rainmeter', hud_item_name='HARQIS PSEI TRADES')
def get_psei_automated_trades(elastic_id, ini=ConfigHelperRainmeter()):

    index_name = '{0}'.format(INDEX_ROOT_NAME_TRADES).lower()

    stock_trades_locs = QList(get_index_data_from_elastic(index_name=index_name,
                                                          app_config_name=elastic_id,
                                                          type_hook=DtoTradeManager))\
        .where(lambda x: x.status not in [TradingConditionsStatus.CLOSED.value, TradingConditionsStatus.CANCELLED.value])

    dump = ''
    for trade in stock_trades_locs:
        dump = dump + '{0:<6} {1:>22}\n'.format(trade.create_order['stock_name'], trade.status)

    app_url = "https://trade.aaa-equities.com.ph/"
    ini['Variables']['ItemLines'] = '{0}'.format(len(stock_trades_locs) + 2)
    ini['meterLink']['text'] = "Trade"
    ini['meterLink']['leftmouseupaction'] = '!Execute ["{0}"pe 3]'.format(app_url)
    ini['meterLink']['tooltiptext'] = app_url

    ini['MeterDisplay']['W'] = '180'
    ini['MeterDisplay']['H'] = '300'

    return dump


@app.task()
@holidays_aware()
@initialize_hud_configuration(source_id='Rainmeter', hud_item_name='HARQIS PSEI SIGNALS')
def get_psei_automated_signals(elastic_id, screener_list, days=0, ini=ConfigHelperRainmeter()):

    #  region Get all existing cards in target strategy

    index_name = '{0}'.format(INDEX_ROOT_NAME_SCREENER).lower()

    stock_strategy_locs = get_index_data_from_elastic(index_name=index_name,
                                                      app_config_name=elastic_id,
                                                      type_hook=DtoStockInvestagrams)

    stock_strategy_locs_filtered = QList(stock_strategy_locs)\
        .where(lambda x: x.strategy_name in screener_list)\
        .where(lambda z: days_between(z.signal_date, DATETIME_FORMAT) < days)  # DEBUG VALUES

    #  endregion

    dump = ''
    for stock in stock_strategy_locs_filtered:
        dump = dump + '{0:<15} {1:>14}\n'.format(stock.strategy_name, stock.stock_name)

    app_url = "https://trade.aaa-equities.com.ph/"
    ini['Variables']['ItemLines'] = '{0}'.format(len(stock_strategy_locs_filtered) + 2)
    ini['meterLink']['text'] = "Trade"
    ini['meterLink']['leftmouseupaction'] = '!Execute ["{0}" 3]'.format(app_url)
    ini['meterLink']['tooltiptext'] = app_url

    ini['MeterDisplay']['W'] = '180'
    ini['MeterDisplay']['H'] = '300'

    return dump


@app.task()
@holidays_aware()
@initialize_hud_configuration(source_id='Rainmeter', hud_item_name='PSEI PORTFOLIO')
def get_psei_portfolio(trading_account_id_aaa, ini=ConfigHelperRainmeter()):

    webdriver_config = apps_config[trading_account_id_aaa]['webdriver']
    wdf = WebDriverFactory

    with wdf.create_webdriver(**webdriver_config) as driver:
        pl = PageAAALogin(driver, source_id=trading_account_id_aaa)
        pl.login()

        ptd = PageAAATradingDeskPortfolio(driver, source_id=trading_account_id_aaa)
        ptd.wait_page_to_load()
        portfolio_ = ptd.get_portfolio_information()

    dump = ''
    for stock_ in portfolio_:
        try:
            dump = dump + '{0:<15} {1:>13}%\n'.format(stock_.symbol, stock_.gain_loss_percentage)
        except TypeError:
            dump = dump + '{0:<15} {1:>13}\n'.format(stock_.symbol, 'NA')

    app_url = "https://trade.aaa-equities.com.ph/"
    ini['Variables']['ItemLines'] = '{0}'.format(len(portfolio_) + 2)
    ini['meterLink']['text'] = "Trade"
    ini['meterLink']['leftmouseupaction'] = '!Execute ["{0}" 3]'.format(app_url)
    ini['meterLink']['tooltiptext'] = app_url

    ini['MeterDisplay']['W'] = '180'
    ini['MeterDisplay']['H'] = '300'

    return dump


@app.task()
@holidays_aware()
@initialize_hud_configuration(source_id='Rainmeter', hud_item_name='PSEI TICKER')
def get_psei_portfolio_ticker(trading_account_id_aaa, investagrams_id, ini=ConfigHelperRainmeter()):

    webdriver_config = apps_config[trading_account_id_aaa]['webdriver']
    wdf = WebDriverFactory

    portfolio_ = []
    with wdf.create_webdriver(**webdriver_config) as driver:
        pl = PageAAALogin(driver, source_id=trading_account_id_aaa)
        pl.login()

        ptd = PageAAATradingDeskPortfolio(driver, source_id=trading_account_id_aaa)
        ptd.wait_page_to_load()
        portfolio_ = ptd.get_portfolio_information()

    dump = ''

    with WebDriverFactory.create_webdriver(**apps_config[investagrams_id]['webdriver']) as driver:
        pl = PageInvestagramsLogin(driver=driver, source_id=investagrams_id)
        pl.login(pl.parameters['username'], pl.parameters['password'])

        stock_page = PageInvestegramsStock(driver=driver, source_id=investagrams_id)

        for stock_ in portfolio_:
            try:
                data = stock_page.get_stock_information(stock_.symbol, include_history=False)

                dump = dump + '{0:<15} {1:>13}%\n'.format(stock_.symbol, data.change_percent)
            except TypeError:
                dump = dump + '{0:<15} {1:>13}\n'.format(stock_.symbol, 'NA')

    app_url = "https://trade.aaa-equities.com.ph/"
    ini['Variables']['ItemLines'] = '{0}'.format(len(portfolio_) + 2)
    ini['meterLink']['text'] = "Trade"
    ini['meterLink']['leftmouseupaction'] = '!Execute ["{0}" 3]'.format(app_url)
    ini['meterLink']['tooltiptext'] = app_url

    ini['MeterDisplay']['W'] = '180'
    ini['MeterDisplay']['H'] = '300'

    return dump


@app.task()
@holidays_aware()
@initialize_hud_configuration(source_id='Rainmeter', hud_item_name='PSEI ORDERS')
def get_psei_orders(trading_account_id_aaa, ini=ConfigHelperRainmeter()):

    webdriver_config = apps_config[trading_account_id_aaa]['webdriver']
    wdf = WebDriverFactory

    with wdf.create_webdriver(**webdriver_config) as driver:
        pl = PageAAALogin(driver, source_id=trading_account_id_aaa)
        pl.login()

        ptd = PageAAATradingDeskOrders(driver, source_id=trading_account_id_aaa)
        orders_ = ptd.get_orders()

    dump = ''
    for stock_ in orders_:
        try:
            dump = dump + '{0:<5} {1:>7} {2}\n'.format(stock_.stock_name, stock_.price, stock_.status)
        except TypeError:
            dump = dump + '{0:<5} {1:>7} {2}\n'.format(stock_.symbol, stock_.price, 'NA')

    app_url = "https://trade.aaa-equities.com.ph/"
    ini['Variables']['ItemLines'] = '{0}'.format(len(orders_) + 2)
    ini['meterLink']['text'] = "Trade"
    ini['meterLink']['leftmouseupaction'] = '!Execute ["{0}" 3]'.format(app_url)
    ini['meterLink']['tooltiptext'] = app_url

    ini['MeterDisplay']['W'] = '180'
    ini['MeterDisplay']['H'] = '300'

    return dump


@app.task()
@initialize_hud_configuration(source_id='Rainmeter', hud_item_name='MTG PORTFOLIO TODAY')
def get_mtg_collection_trends(echo_account, ini=ConfigHelperRainmeter()):

    service = ApiServiceEchoMTGInventory(source_id=echo_account)
    portfolio_ = service.get_collection()

    dump = ''

    card_info = []
    for card_mtg in portfolio_['items']:
        price_change_avg = card_mtg['market_percentage_html']
        try:
            result = re.search('>(.*)%</', price_change_avg)
            card_info.append((card_mtg['name'],  float(result.group(1))))
        except AttributeError:
            log.warning("Failed to fetch card price average for {0}".format(card_mtg['name']))
            continue

    sorted_change_ = sorted(card_info, key=lambda x: x[1], reverse=True)
    sorted_change = [k for k, _ in itertools.groupby(sorted_change_)]

    winners = QList(sorted_change).where(lambda x: x[1] > 20)
    #losers = sorted_change[-30:]
    losers = []

    for card_info in winners + losers:
        card_name = (card_info[0][:18] + '..') if len(card_info[0]) > 18 else card_info[0]
        dump = dump + '{0:<20} {1:>8}%\n'.format(card_name, card_info[1])

    app_url = "https://www.echomtg.com/inventory/"
    ini['Variables']['ItemLines'] = '{0}'.format(20)
    ini['meterLink']['text'] = "Collection"
    ini['meterLink']['leftmouseupaction'] = '!Execute ["{0}" 3]'.format(app_url)
    ini['meterLink']['tooltiptext'] = app_url

    ini['MeterDisplay']['W'] = '180'
    ini['MeterDisplay']['H'] = '500'

    return dump


