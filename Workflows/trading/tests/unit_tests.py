from Workflows.trading import *


class TestDto(JsonObject):
    number = float
    condition = bool


class UnitTests(TestCase):

    def test_add_cards_from_signals_fx(self):
        add_cards_from_signals_fx_key_levels(
            trello_id='Trello',
            oanda_id='OANDA',
            indicators_id='TwelveTrading',
            notifications_id='PushNotifications',
            signals_board_name="Daily Dashboard Trading",
            signals_list_name="SIGNALS",
            transact_list_name="PENDING",
            labels_list=['FOREX']
        )

    def test_update_orders_trailing_stop_delayed(self):
        update_orders_trailing_stop_delayed(
                                        trello_id='Trello',
                                        oanda_id='OANDA',
                                        indicators_id='TwelveTrading',
                                        open_trades_board_name='Daily Dashboard Trading',
                                        open_trades_list_name='OPEN',
                                        labels_list=['FOREX']
                                        )

    def test_add_cards_from_signals_fx_key_levels_manual(self):
        add_cards_from_signals_fx_key_levels_manual(
            trello_id='Trello',
            oanda_id='OANDA',
            indicators_id='TwelveTrading',
            notifications_id='PushNotifications',
            signals_board_name="Daily Dashboard Trading",
            signals_list_name="SIGNALS",
            labels_list=['FOREX', "MANUAL"]
        )

    def test_add_cards_from_signals_fx_key_levels_prediction(self):
        add_cards_from_signals_fx_key_levels_prediction(
            trello_id='Trello',
            oanda_id='OANDA',
            indicators_id='TwelveTrading',
            notifications_id='PushNotifications',
            signals_board_name="Daily Dashboard Trading",
            signals_list_name="UPCOMING",
            transact_list_name="PENDING",
            labels_list=['FOREX']
        )

    def test_move_cards_to_closed(self):
        move_cards_to_closed_trades(
            trello_id='Trello',
            oanda_id='OANDA',
            notifications_id='PushNotifications',
            closed_trades_board_name="Daily Dashboard Trading",
            closed_trades_list_name="CLOSED",
            open_trades_list_name="OPEN",
            labels_list=['FOREX']
        )

    def test_move_pending_to_open(self):
        move_cards_to_open_trades(
            trello_id='Trello',
            oanda_id='OANDA',
            notifications_id='PushNotifications',
            open_trades_board_name="Daily Dashboard Trading",
            open_trades_list_name="OPEN",
            pending_trades_list_name="PENDING",
            labels_list=['FOREX']
        )

    def test_create_manual_trade_open_to_cards(self):
        create_manual_trade_open_to_cards(
            trello_id='Trello',
            oanda_id='OANDA',
            open_trades_board_name="Daily Dashboard Trading",
            open_trades_list_name="OPEN",
            labels_list=['FOREX', 'MANUAL']
        )

    def test_move_cancelled_cards_to_closed_trades(self):
        move_cancelled_cards_to_closed_trades(
            trello_id='Trello',
            oanda_id='OANDA',
            notifications_id='PushNotifications',
            pending_trades_board_name="Daily Dashboard Trading",
            pending_trades_list_name="PENDING",
            closed_trades_list_name="CLOSED",
            labels_list=['FOREX']
        )

    @pytest.mark.skip(reason=SKIP_TEST_TRANSACTION)
    def test_archive_cards(self):
        archive_signals_cards(
            trello_id='Trello',
            board_name="Daily Dashboard Trading",
            list_name="SIGNALS"
        )

    @pytest.mark.skip(reason=SKIP_TEST_TRANSACTION)
    def test_remove_completed_signal_cards_from_list(self):
        remove_completed_signal_cards_from_list(
            trello_id='Trello',
            oanda_id='OANDA',
            board_name="Daily Dashboard Trading",
            list_name="SIGNALS",
        )

    def test_add_cards_from_signals_psei(self):
        add_cards_from_signals_screener_investagrams(
            "Investagrams",
            "Trello",
            "Swing Sniper B",
            "Daily Dashboard Trading",
            "SIGNALS",
            ['PSEI']

        )

    def test_add_cards_from_signals_psei_sandbox(self):
        add_cards_from_signals_screener_investagrams_sandbox(
            "Investagrams",
            "Trello",
            "Swing Sniper",
            "Daily Dashboard Trading",
            "STRATEGIES",
            ['PSEI', 'BUY']

        )

    def test_add_cards_from_signals_psei_sandbox_x(self):
        add_cards_from_signals_screener_investagrams_sandbox(
            "Investagrams",
            "Trello",
            "Swing Sniper X",
            "Daily Dashboard Trading",
            "STRATEGIES",
            ['PSEI', 'BUY']

        )

    def test_add_cards_from_signals_psei_sandbox_v(self):
        add_cards_from_signals_screener_investagrams_sandbox(
            "Investagrams",
            "Trello",
            "Swing Sniper V",
            "Daily Dashboard Trading",
            "STRATEGIES",
            ['PSEI', 'BUY']

        )

    def test_update_cards_from_signals_screener_investagrams_sandbox(self):
        update_cards_from_signals_screener_investagrams_sandbox(
            "Investagrams",
            "Trello",
            "Daily Dashboard Trading",
            "STRATEGIES",
            ['PSEI', 'BUY']
        )

    def test_load_cards_from_signals_screener_investagrams_sandbox_csv(self):
        load_signals_screener_investagrams_sandbox_csv(
            "Investagrams",
            "test_data_2021-04-20__2021-04-29.csv",
            "Trello",
            "Daily Dashboard Trading",
            "STRATEGIES",
            ['PSEI', 'BUY']
        )

    def test_load_cards_from_signals_screener_investagrams_sandbox_elastic(self):
        load_signals_screener_investagrams_sandbox_csv_to_elastic(
            "Investagrams",
            'ElasticSearch',
            "Jul_Sep2021.csv"
        )

    def test_add_cards_from_signals_screener_investagrams_sandbox_to_elastic_v(self):
        add_signals_screener_investagrams_sandbox_to_elastic(
            "Investagrams",
            'ElasticSearch',
            "Swing Sniper W"
        )

    def test_add_cards_from_signals_screener_investagrams_sandbox_to_elastic_y(self):
        add_signals_screener_investagrams_sandbox_to_elastic(
            "Investagrams",
            'ElasticSearch',
            "Swing Sniper Y"
        )

    def test_add_cards_from_signals_screener_investagrams_sandbox_to_elastic_x(self):
        add_signals_screener_investagrams_sandbox_to_elastic(
            "Investagrams",
            'ElasticSearch',
            "Swing Sniper X"
        )

    def test_add_cards_from_signals_screener_investagrams_sandbox_to_elastic_z(self):
        add_signals_screener_investagrams_sandbox_to_elastic(
            "Investagrams",
            'ElasticSearch',
            "Swing Sniper B"
        )

    def test_update_cards_from_signals_screener_investagrams_sandbox_to_elastic(self):
        update_signals_screener_investagrams_sandbox_to_elastic(
            "Investagrams",
            'ElasticSearch',
            days_to_update=5,
        )

    def test_create_offline_buy_orders_from_system_signal(self):
        create_offline_buy_orders_from_system_signal("ElasticSearch",
                                                     "Swing Sniper W",
                                                     "AAA",
                                                     )

    def test_create_offline_sell_orders_from_system_signal(self):
        create_offline_sell_orders_from_system_signal("ElasticSearch",
                                                      "AAA")

    def test_update_portfolio_index_information(self):
        update_portfolio_index_information("ElasticSearch",
                                           "AAA")

    def test_create_offline_trailing_stops(self):
        create_offline_trailing_stops(elastic_id='ElasticSearch',
                                      trading_account_id_aaa='AAA'
                                      )

    def test_add_cards_from_signals_fx_key_levels_elastic(self):
        add_signals_fx_key_levels_to_elastic(elastic_id='ElasticSearch',
                                             oanda_id='OANDA',
                                             indicators_id='TwelveTrading',
                                             notifications_id='PushNotifications',
                                             )
