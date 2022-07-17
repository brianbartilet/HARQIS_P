from Workflows import *
from datetime import timedelta
from celery.schedules import crontab
import datetime


"""
https://docs.celeryproject.org/en/stable/userguide/periodic-tasks.html
https://stackoverflow.com/questions/31468354/unpicklingerror-on-celerybeat-startup

"""
DAILY_TASKS = {

    #  region HUD
    """
    'run-hud-test-update_dashboard_messages_upcoming':
        {
            'task': 'Workflows.hud.hud.update_dashboard_messages_upcoming',
            'schedule': timedelta(minutes=5),
            'args': []
        },
    """
    #  endregion

    #  region FOREX
    """
    'run-trading-daily-signals-archive':
        {
            'task': 'Workflows.trading.forex.signals.archive_signals_cards',
            'schedule': crontab(hour=1, minute=10, day_of_week='sun'),
            'args': ['Trello',
                     "Daily Dashboard Trading",
                     "SIGNALS",
                     ]
        },
    
    'run-trading-daily-signals':
        {
           'task': 'Workflows.trading.forex.signals.add_cards_from_signals_fx_key_levels',
            'schedule': crontab(minute=3, day_of_week='mon,tue,wed,thu,fri'),
            'args': ['Trello',
                     'OANDA',
                     'TwelveTrading',
                     'PushNotifications',
                     "Daily Dashboard Trading",
                     "SIGNALS",
                     "PENDING",
                     ['FOREX']

                     ]
        },

    'run-trading-daily-signals-manual':
        {
            'task': 'Workflows.trading.forex.signals.add_cards_from_signals_fx_key_levels_manual',
            'schedule': crontab(minute=5, day_of_week='mon,tue,wed,thu,fri'),
            'args': ['Trello',
                     'OANDA',
                     'TwelveTrading',
                     'PushNotifications',
                     "Daily Dashboard Trading",
                     "SIGNALS",
                     ['FOREX', 'MANUAL']

                     ]
        },

    'run-trading-create_manual_trade_open_to_cards':
        {
            'task': 'Workflows.trading.forex.open.create_manual_trade_open_to_cards',
            'schedule': crontab(minute=15, day_of_week='mon,tue,wed,thu,fri'),
            'args': ['Trello',
                     'OANDA',
                     "Daily Dashboard Trading",
                     "OPEN",
                     ['FOREX', 'MANUAL']
                     ]
        },

    'run-trading-daily-signals-add_cards_from_signals_fx_key_levels_prediction':
        {
            'task': 'Workflows.trading.forex.signals.add_cards_from_signals_fx_key_levels_prediction',
            'schedule': crontab(minute=10, day_of_week='mon,tue,wed,thu,fri'),
            'args': ['Trello',
                     'OANDA',
                     'TwelveTrading',
                     'PushNotifications',
                     "Daily Dashboard Trading",
                     "UPCOMING",
                     "PENDING",
                     ['FOREX']

                     ]
        },

    'run-trading-daily-signals-move_cards_to_closed_trades':
        {
            'task': 'Workflows.trading.forex.closed.move_cards_to_closed_trades',
            'schedule': crontab(minute=5, day_of_week='mon,tue,wed,thu,fri'),
            'args': ['Trello',
                     'OANDA',
                     'PushNotifications',
                     "Daily Dashboard Trading",
                     "CLOSED",
                     "OPEN",
                     ['FOREX']

                     ]
        },

    'run-trading-daily-signals-move_cards_to_open_trades':
        {
            'task': 'Workflows.trading.forex.open.move_cards_to_open_trades',
            'schedule': crontab(minute=5, day_of_week='mon,tue,wed,thu,fri'),
            'args': ['Trello',
                     'OANDA',
                     'PushNotifications',
                     "Daily Dashboard Trading",
                     "OPEN",
                     "PENDING",
                     ['FOREX']

                     ]
        },

    'run-trading-daily-signals-move_cancelled_cards_to_closed_trades':
        {
            'task': 'Workflows.trading.forex.closed.move_cancelled_cards_to_closed_trades',
            'schedule': crontab(minute=15, day_of_week='mon,tue,wed,thu,fri'),
            'args': ['Trello',
                     'OANDA',
                     'PushNotifications',
                     "Daily Dashboard Trading",
                     "PENDING",
                     "CLOSED",
                     ['FOREX']

                     ]
        },
    """    
    
    #  endregion

    #  region PSEI Trello - Moved to Elastic Search
    """
    'run-trading-daily-signals-psei-tester-buy-add_cards_from_signals_screener_investagrams_sandbox_x':
        {
            'task': 'Workflows.trading.psei.strategies.add_cards_from_signals_screener_investagrams_sandbox',
            'schedule': crontab(hour=3, minute=40, day_of_week='mon,tue,wed,thu,fri'),
            'args': ['Investagrams',
                     'Trello',
                     'Swing Sniper X',
                     "Daily Dashboard Trading",
                     "SIGNALS",
                     ['PSEI', 'BUY']
                     ]
        },

    'run-trading-daily-signals-psei-tester-buy-add_cards_from_signals_screener_investagrams_sandbox_v':
        {
            'task': 'Workflows.trading.psei.strategies.add_cards_from_signals_screener_investagrams_sandbox',
            'schedule': crontab(hour=3, minute=45, day_of_week='mon,tue,wed,thu,fri'),
            'args': ['Investagrams',
                     'Trello',
                     'Swing Sniper V',
                     "Daily Dashboard Trading",
                     "SIGNALS",
                     ['PSEI', 'BUY']
                     ]
        },

    'run-trading-daily-signals-psei-tester-buy-update_cards_from_signals_screener_investagrams_sandbox':
        {
            'task': 'Workflows.trading.psei.strategies.update_cards_from_signals_screener_investagrams_sandbox',
            'schedule': crontab(hour=8, minute=30, day_of_week='mon,tue,wed,thu,fri'),
            'args': ['Investagrams',
                     'Trello',
                     "Daily Dashboard Trading",
                     "SIGNALS",
                     ['PSEI', 'BUY']
                     ]
        },
    """
    #  endregion
    
    
    #  region Jobs for PSEI ELK
    'run-hud-test-add_signals_screener_investagrams_sandbox_to_elastic-w':
        {
            'task': 'Workflows.trading.psei.strategies.add_signals_screener_investagrams_sandbox_to_elastic',
            'schedule': crontab(hour=16, minute=5, day_of_week='mon,tue,wed,thu,fri'),
            'args': ['Investagrams', 'ElasticSearch', 'Swing Sniper W']
        },

    'run-hud-test-add_signals_screener_investagrams_sandbox_to_elastic-z':
        {
            'task': 'Workflows.trading.psei.strategies.add_signals_screener_investagrams_sandbox_to_elastic',
            'schedule': crontab(hour=16, minute=10, day_of_week='mon,tue,wed,thu,fri'),
            'args': ['Investagrams', 'ElasticSearch', 'Swing Sniper Z']
        },

    'run-hud-test-add_signals_screener_investagrams_sandbox_to_elastic-v':
        {
            'task': 'Workflows.trading.psei.strategies.add_signals_screener_investagrams_sandbox_to_elastic',
            'schedule': crontab(hour=16, minute=15, day_of_week='mon,tue,wed,thu,fri'),
            'args': ['Investagrams', 'ElasticSearch', 'Swing Sniper V']
        },

    'run-hud-test-add_signals_screener_investagrams_sandbox_to_elastic-x':
        {
            'task': 'Workflows.trading.psei.strategies.add_signals_screener_investagrams_sandbox_to_elastic',
            'schedule': crontab(hour=16, minute=20, day_of_week='mon,tue,wed,thu,fri'),
            'args': ['Investagrams', 'ElasticSearch', 'Swing Sniper X']
        },

    'run-hud-test-add_signals_screener_investagrams_sandbox_to_elastic-y':
        {
            'task': 'Workflows.trading.psei.strategies.add_signals_screener_investagrams_sandbox_to_elastic',
            'schedule': crontab(hour=16, minute=25, day_of_week='mon,tue,wed,thu,fri'),
            'args': ['Investagrams', 'ElasticSearch', 'Swing Sniper Y']
        },

    'run-hud-test-add_signals_screener_investagrams_sandbox_to_elastic-b':
        {
            'task': 'Workflows.trading.psei.strategies.add_signals_screener_investagrams_sandbox_to_elastic',
            'schedule': crontab(hour=16, minute=30, day_of_week='mon,tue,wed,thu,fri'),
            'args': ['Investagrams', 'ElasticSearch', 'Swing Sniper B']
        },

    'run-hud-test-update_signals_screener_investagrams_sandbox_to_elastic_early':
        {
            'task': 'Workflows.trading.psei.strategies.update_signals_screener_investagrams_sandbox_to_elastic',
            'schedule': crontab(hour=16, minute=50, day_of_week='mon,tue,wed,thu,fri'),
            'args': ['Investagrams', 'ElasticSearch']
        },

    'run-hud-test-update_signals_screener_investagrams_sandbox_to_elastic_all':
        {
            'task': 'Workflows.trading.psei.strategies.update_signals_screener_investagrams_sandbox_to_elastic',
            'schedule': crontab(hour=3, minute=10, day_of_week='sun,mon,tue,wed,thu,fri'),
            'args': ['Investagrams', 'ElasticSearch', 90]
        },

    'run-hud-test-create_offline_buy_orders_from_system_signal-w':
        {
            'task': 'Workflows.trading.psei.pending.create_offline_buy_orders_from_system_signal',
            'schedule': crontab(hour=6, minute=30, day_of_week='mon,tue,wed,thu,fri'),
            'args': ['ElasticSearch', 'Swing Sniper W', 'AAA']
        },

    'run-hud-test-create_offline_buy_orders_from_system_signal-x':
        {
            'task': 'Workflows.trading.psei.pending.create_offline_buy_orders_from_system_signal',
            'schedule': crontab(hour=6, minute=40, day_of_week='mon,tue,wed,thu,fri'),
            'args': ['ElasticSearch', 'Swing Sniper X', 'AAA']
        },

    'run-hud-test-create_offline_sell_orders_from_system_signal':
        {
            'task': 'Workflows.trading.psei.pending.create_offline_sell_orders_from_system_signal',
            'schedule': crontab(hour=7, minute=30, day_of_week='mon,tue,wed,thu,fri'),
            'args': ['ElasticSearch', 'AAA']
        },

    'run-hud-test-create_offline_trailing_stops':
        {
            'task': 'Workflows.trading.psei.pending.create_offline_trailing_stops',
            'schedule': crontab(hour=8, minute=30, day_of_week='mon,tue,wed,thu,fri'),
            'args': ['ElasticSearch', 'AAA']
        },

    #  endregion

    #  region Peon
    """
    'run-peon-time-in':
        {
            'task': 'Workflows.workday.daily_punch.punch_in',
            'schedule': crontab(hour=5, minute=30, day_of_week='mon,tue,wed,thu,fri'),
            'args': ['PeonAllSec']

        },

    'run-peon-time-out':
        {
            'task': 'Workflows.workday.daily_punch.punch_out',
            'schedule': crontab(hour=17, minute=45, day_of_week='tue,wed,thu,fri,sat'),
            'args': ['PeonAllSec']

        },

    'run-peon-days-absent':
        {
            'task': 'Workflows.workday.daily_punch.check_absent_days',
            'schedule': crontab(hour=6, minute=30, day_of_week='mon,tue,wed,thu,fri'),
            'args': ['PeonAllSec', 'PushNotifications']

        },
    """
    #  endregion

    #  region Finance

    'run-finance-mtg-add':
        {
            'task': 'Workflows.finance.mtg_collection.create_budget_transactions_from_collection',
            'schedule': crontab(hour='*/2', minute=0),
            'args': ['EchoMTG', 'YNAB', 'standard']

        },

    'run-finance-mtg-add-budget':
        {
            'task': 'Workflows.finance.mtg_collection.create_budget_transactions_from_collection',
            'schedule': crontab(hour='*/2', minute=0),
            'args': ['EchoMTG', 'YNAB', 'penny']

        },

    'run-finance-mtg-update':
        {
            'task': 'Workflows.finance.mtg_collection.update_budget_transactions_from_collection',
            'schedule': crontab(hour='*/2', minute=10),
            'args': ['EchoMTG', 'YNAB', 'standard']

        },

    'run-finance-mtg-update-budget':
        {
            'task': 'Workflows.finance.mtg_collection.update_budget_transactions_from_collection',
            'schedule': crontab(hour='*/2', minute=10),
            'args': ['EchoMTG', 'YNAB', 'penny']

        },

    'run-finance-mtg-update-remove':
        {
            'task': 'Workflows.finance.mtg_collection.update_budget_transactions_from_removed_items_collection',
            'schedule': crontab(hour='*/2', minute=20),
            'args': ['EchoMTG', 'YNAB', 'standard']

        },

    'run-finance-mtg-update-remove-budget':
        {
            'task': 'Workflows.finance.mtg_collection.update_budget_transactions_from_removed_items_collection',
            'schedule': crontab(hour='*/2', minute=20),
            'args': ['EchoMTG', 'YNAB', 'penny']

        },

    'run-finance-mtg-update-uncleared-transactions-to-collection':
        {
            'task': 'Workflows.finance.mtg_collection.update_collection_notes_for_trading_from_uncleared_budget_transactions',
            'schedule': crontab(hour='*/2', minute=30),
            'args': ['EchoMTG', 'YNAB', 'standard']

        },

    """
    'run-finance-mtg-update-uncleared-transactions-to-collection-budget':
        {
            'task': 'Workflows.finance.mtg_collection.update_collection_notes_for_trading_from_uncleared_budget_transactions',
            'schedule': crontab(hour='*/2', minute=30),
            'args': ['EchoMTG', 'YNAB', 'penny']

        },

    'run-finance-mtg-update-cleared-transactions-to-collection':
        {
            'task': 'Workflows.finance.mtg_collection.update_collection_notes_for_trading_from_cleared_budget_transactions',
            'schedule': crontab(hour='*/2', minute=40),
            'args': ['EchoMTG', 'YNAB', 'standard']

        },

    'run-finance-mtg-update-cleared-transactions-to-collection-budget':
        {
            'task': 'Workflows.finance.mtg_collection.update_collection_notes_for_trading_from_cleared_budget_transactions',
            'schedule': crontab(hour='*/2', minute=40),
            'args': ['EchoMTG', 'YNAB', 'penny']

        },
    

    'run-finance-mtg-add-cards-to-echo-from-scan':
        {
            'task': 'Workflows.finance.mtg_collection.add_new_cards_from_csv_job',
            'schedule': timedelta(hours=2),
            'args': ['EchoMTG', 'YNAB', 'Daily Dashboard', 'JOBS']

        },
    """
    
    'run-finance-mtg-update-remove-range':
        {
            'task': 'Workflows.finance.mtg_collection.update_budget_transactions_from_changed_price_budget_range',
            'schedule': crontab(hour='*/2', minute=55),
            'args': ['EchoMTG', 'YNAB']

        },

    #  endregion

    #  region MTG Active Selling
    """
        Hangs the queue
    'run-finance-mtg-selling-standard-hi':
        {
            'task': 'Workflows.finance.mtg_selling.generate_collection_selling',
            #'schedule': crontab(hour=1),
            'schedule': timedelta(hours=12),
            'args': ['EchoMTG', 'GoogleAPIsSheet', 'x40 USD', 40, 'standard', -1000, 15]

        },

    'run-finance-mtg-selling-standard-lo':
        {
            'task': 'Workflows.finance.mtg_selling.generate_collection_selling',
            # 'schedule': crontab(hour=1),
            'schedule': timedelta(hours=12),
            'args': ['EchoMTG', 'GoogleAPIsSheet', 'x35 USD', 35, 'standard', 15]

        },

    'run-finance-mtg-selling-budget':
        {
            'task': 'Workflows.finance.mtg_selling.generate_collection_selling',
            #'schedule': crontab(hour=1),
            'schedule': timedelta(hours=12),
            'args': ['EchoMTG', 'GoogleAPIsSheet', 'x30 USD', 30, 'penny', -1]

        },

    'run-finance-mtg-selling-wants':
        {
            'task': 'Workflows.finance.mtg_selling.generate_collection_buylist',
            #'schedule': crontab(hour=1),
            'schedule': timedelta(hours=12),
            'args': ['EchoMTG', 'GoogleAPIsSheet', 'MY WISHLIST', 25878]

        },
    """
    #  endregion

    #  region Reminders
    #  https://ifttt.com/applets/tytTsJzW
    #  https://trello.cronofy.com/settings
    

    'run-trello-all-reminders-from-habit-cards-description':
        {
            'task': 'Workflows.habits.reminders.create_trello_reminders_from_habit_cards',
            'schedule': crontab(minute=5, hour=2),
            'args': ["Trello",
                     "Daily Dashboard",
                     "GRIND",
                     "EXECUTE"
                     ]
        },

    'run-trello-all-reminders-from-habit-cards-description-create_daily_tasks_metrics':
        {
            'task': 'Workflows.habits.reminders.create_daily_tasks_metrics',
            # 'schedule': crontab(minute=5, hour=1, day_of_week='mon,tue,wed,thu,fri,sat,sun'),
            'schedule': timedelta(hours=4),
            'args': ["ElasticSearch",
                     "Trello",
                     "Daily Dashboard",
                     "EXECUTE",
                     ]
        },

    'run-trello-all-reminders-from-habit-cards-description-archive':
        {
            'task': 'Workflows.habits.reminders.archive_trello_reminders_from_habit_cards',
            'schedule': crontab(minute=30, hour=1, day_of_week='mon,tue,wed,thu,fri,sat,sun'),
            'args': ["Trello",
                     "Daily Dashboard",
                     "EXECUTE",
                     "COMPLETED",
                     "RECURRING",
                     "DONE"
                     ]
        },

    'run-trello-reminders-agons':
        {
            'task': 'Workflows.habits.strenuous_life.create_trello_reminder_from_weekly_agons',
            'schedule': crontab(minute=10, hour=23, day_of_week='sun'),
            'args': ["StrenuousLife",
                     "Trello",
                     "Daily Dashboard",
                     "EXECUTE",
                     "https://media.giphy.com/media/pw7qE5fPNrNWo/giphy.gif"
                     ]

        },

    'run-trello-reminders-homework-for-life':
        {   #  https://www.authormagazine.org/articles/2018/6/2/homework-for-life
            'task': 'Workflows.habits.reminders.create_homework_for_life',
            'schedule': crontab(minute=5, hour=19, day_of_week='mon,tue,wed,thu,fri,sat,sun'),
            'args': ["Trello",
                     "Daily Dashboard",
                     "EXECUTE"
                     ]
        },

    'run-trello-reminders-homework-for-life-clean':
        {  # https://www.authormagazine.org/articles/2018/6/2/homework-for-life
            'task': 'Workflows.habits.reminders.move_cards_to_target_list',
            'schedule': crontab(minute=55, hour=23, day_of_week='mon,tue,wed,thu,fri,sat,sun'),
            'args': ["Trello",
                     "Daily Dashboard",
                     "EXECUTE",
                     "HOMEWORK FOR LIFE",
                     "*HFL"
                     ]
        },

    'run-trello-reminders-homework-for-life-clean-blank':
        {  # https://www.authormagazine.org/articles/2018/6/2/homework-for-life
            'task': 'Workflows.habits.reminders.clean_blank_homework_for_life',
            'schedule': crontab(minute=30, hour=1, day_of_week='mon,tue,wed,thu,fri,sat,sun'),
            'args': ["Trello",
                     "Daily Dashboard",
                     "HOMEWORK FOR LIFE"
                     ]
        },

    'run-trello-meal-plan':
        {
            'task': 'Workflows.habits.reminders.create_meal_planning',
            'schedule': crontab(minute=0, hour=1, day_of_week='sat'),
            'args': ["Trello", "WHAT'S MY ULAM TODAY?", "RECIPES LIST"]
        },

    #  endregion

    #  region MTG Selling

    'run-finance-mtg-selling-standard-jobs-google-hud':
        {
            'task': 'Workflows.finance.mtg_selling.generate_collection_selling_jobs',
            'schedule': timedelta(hours=8),
            'args': ["E:/GIT/HARQIS/Workflows/finance/tests", "google.py"]

        },

    #  endregion

    #  region Local Jobs

    'run-hud-test-update_portfolio_index_information':
        {
            'task': 'Workflows.trading.psei.pending.update_portfolio_index_information',
            'schedule': crontab(hour='*/4', minute=40, day_of_week='mon,tue,wed,thu,fri'),
            'args': ['ElasticSearch', 'AAAHeadless']
        },

    #  endregion

    #  region NIKE BOTS

    #  endregion


    #  region YNAB update jobs

    'run-hud-test-create_transactions_from_account_sms_update-gcash_payments':
        {
            'task': 'Workflows.finance.ynab_transactions.create_transactions_from_account_sms_update',
            'schedule': timedelta(hours=4),
            'args': ['YNAB', 'PushBullet', 'CASH - GCash', 'GCash', 'gcash_payments', 4]
        },

    'run-hud-test-create_transactions_from_account_sms_update-gcash_send':
        {
            'task': 'Workflows.finance.ynab_transactions.create_transactions_from_account_sms_update',
            'schedule': timedelta(hours=4),
            'args': ['YNAB', 'PushBullet', 'CASH - GCash', 'GCash', 'gcash_send', 4]
        },

    'run-hud-test-create_transactions_from_account_sms_update-gcash_receive':
        {
            'task': 'Workflows.finance.ynab_transactions.create_transactions_from_account_sms_update',
            'schedule': timedelta(hours=4),
            'args': ['YNAB', 'PushBullet', 'CASH - GCash', 'GCash', 'gcash_receive', 4]
        },

    'run-hud-test-create_transactions_from_account_sms_update-bpi_payments':
        {
            'task': 'Workflows.finance.ynab_transactions.create_transactions_from_account_sms_update',
            'schedule': timedelta(hours=4),
            'args': ['YNAB', 'PushBullet', 'PAYROLL - BPI', 'BPI-OTP', 'bpi_payments', 4]
        },

    'run-hud-test-create_transactions_from_account_sms_update-bpi_cc_payments':
        {
            'task': 'Workflows.finance.ynab_transactions.create_transactions_from_account_sms_update',
            'schedule': timedelta(hours=4),
            'args': ['YNAB', 'PushBullet', 'PAYROLL - BPI', 'BPI', 'bpi_withdraw', 4]
        },

    'run-hud-test-create_transactions_from_account_sms_update-union_transfers':
        {
            'task': 'Workflows.finance.ynab_transactions.create_transactions_from_account_sms_update',
            'schedule': timedelta(hours=4),
            'args': ['YNAB', 'PushBullet', 'PAYROLL - BPI', 'FUNDS - Investments', 'union_transfers', 4]
        },

    'run-hud-test-create_transactions_from_account_sms_update-update_account_oanda':
        {
            'task': 'Workflows.finance.ynab_transactions.update_account_oanda',
            'schedule': crontab(hour=1, minute=30, day_of_week='mon,tue,wed,thu,fri'),
            'args': ['YNAB', 'OANDA', 'ExchangeRates', 'FOREX - OANDA']
        },

    'run-hud-test-create_transactions_from_account_sms_update-update_daily_portfolio':
        {
            'task': 'Workflows.finance.ynab_transactions.update_daily_portfolio',
            'schedule': crontab(hour=16, minute=30, day_of_week='mon,tue,wed,thu,fri'),
            'args': ['YNAB', 'AAA', 'STOCKS - AAA']
        },

    #  endregion

    #  region GCash

    'run-hud-test-create_transactions_from_account_sms_update-gcash-gcash_receive':
        {
            'task': 'Workflows.finance.ynab_transactions.create_transactions_from_account_sms_update',
            'schedule': crontab(hour=0, minute=15, day_of_week='mon,tue,wed,thu,fri,sat,sun'),
            'args': ['YNAB', 'PushBullet', 'CASH - GCash', 'GCash', 'gcash_receive']
        },

    'run-hud-test-create_transactions_from_account_sms_update-gcash-gcash_payments_store':
        {
            'task': 'Workflows.finance.ynab_transactions.create_transactions_from_account_sms_update',
            'schedule': crontab(hour=0, minute=15, day_of_week='mon,tue,wed,thu,fri,sat,sun'),
            'args': ['YNAB', 'PushBullet', 'CASH - GCash', 'GCash', 'gcash_payments_store']
        },

    'run-hud-test-create_transactions_from_account_sms_update-gcash-gcash_payments':
        {
            'task': 'Workflows.finance.ynab_transactions.create_transactions_from_account_sms_update',
            'schedule': crontab(hour=0, minute=15, day_of_week='mon,tue,wed,thu,fri,sat,sun'),
            'args': ['YNAB', 'PushBullet', 'CASH - GCash', 'GCash', 'gcash_payments']
        },

    #  endregion

}