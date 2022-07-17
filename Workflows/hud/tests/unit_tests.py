import configparser
from Workflows.hud import *


class UnitTests(TestCase):

    def test_config_read(self):
        update_dashboard_trello_current_cards_info("Trello", "Daily Dashboard")

    def test_update_dashboard_trello_current_cards_info_trading(self):
        update_dashboard_trello_current_cards_info_trading("OANDA")

    def test_update_dashboard_oracle_timesheet(self):
        update_dashboard_oracle_timesheet("OracleTimesheet")

    def test_update_dashboard_trello_current_cards_info_reminders(self):
        update_dashboard_trello_current_cards_info_reminders("Trello", "Daily Dashboard")

    def test_get_budget_info(self):
        get_current_budget_info("YNAB")

    def test_links_navigator(self):
        update_quick_links()

    def test_update_dashboard_messages(self):
        update_dashboard_messages('PushNotifications')

    def test_update_dashboard_messages_failed(self):
        update_dashboard_messages_failed('PushNotifications')

    def test_update_dashboard_messages_upcoming(self):
        update_dashboard_messages_upcoming(os.path.join(ENV_ROOT_DIRECTORY, 'celerybeat-schedule'))

    def test_get_psei_automated_trades(self):
        get_psei_automated_trades('ElasticSearch')

    def test_get_psei_automated_signals(self):
        get_psei_automated_signals('ElasticSearch', ['Swing Sniper W', 'Swing Sniper B'], 5)

    def test_get_psei_portfolio(self):
        get_psei_portfolio('AAAHeadless')

    def test_get_psei_orders(self):
        get_psei_orders('AAAHeadless')

    def test_get_mtg_collection_trends(self):
        get_mtg_collection_trends('EchoMTG')

    def test_get_psei_portfolio_ticker(self):
        get_psei_portfolio_ticker('AAA', 'Investagrams')