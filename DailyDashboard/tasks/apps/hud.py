from Workflows import *
from datetime import timedelta
from celery.schedules import crontab

"""
https://docs.celeryproject.org/en/stable/userguide/periodic-tasks.html
https://stackoverflow.com/questions/31468354/unpicklingerror-on-celerybeat-startup

"""
HUD_TASKS = {

    #  region HUD
    'run-hud-test-update_quick_links':
        {
            'task': 'Workflows.hud.hud.update_quick_links',
            'schedule': timedelta(hours=8),
            'args': []
        },

    'run-hud-test-update_dashboard_trello_current_cards_info':
        {
            'task': 'Workflows.hud.hud.update_dashboard_trello_current_cards_info',
            'schedule': timedelta(hours=1),
            'args': ['Trello', 'Daily Dashboard']
        },

    'run-hud-test-update_dashboard_trello_current_cards_info_reminders':
        {
            'task': 'Workflows.hud.hud.update_dashboard_trello_current_cards_info_reminders',
            'schedule': timedelta(hours=4),
            'args': ['Trello', 'Daily Dashboard']
        },

    'run-hud-test-update_dashboard_trello_daily_trading':
        {
            'task': 'Workflows.hud.hud.update_dashboard_trello_current_cards_info_trading',
            'schedule': timedelta(minutes=10),
            'args': ['OANDA']
        },

    'run-hud-test-get_current_budget_info':
        {
            'task': 'Workflows.hud.hud.get_current_budget_info',
            'schedule': timedelta(hours=4),
            'args': ['YNAB']
        },

    'run-hud-test-update_dashboard_messages':
        {
            'task': 'Workflows.hud.hud.update_dashboard_messages',
            'schedule': timedelta(minutes=30),
            'args': ['PushNotifications']
        },

    'run-hud-test-update_dashboard_messages_failed':
        {
            'task': 'Workflows.hud.hud.update_dashboard_messages_failed',
            'schedule': timedelta(minutes=5),
            'args': ['PushNotifications']
        },


    'run-hud-test-get_psei_automated_trades':
        {
            'task': 'Workflows.hud.hud.get_psei_automated_trades',
            'schedule': timedelta(hours=1),
            'args': ['ElasticSearch']
        },

    'run-hud-test-get_psei_automated_signals':
        {
            'task': 'Workflows.hud.hud.get_psei_automated_signals',
            'schedule': crontab(minute=10, hour='16,17,18,19,20', day_of_week='mon,tue,wed,thu,fri'),
            'args': ['ElasticSearch', ['Swing Sniper B', 'Swing Sniper W'], 1]
        },

    'run-hud-test-get_psei_portfolio':
        {
            'task': 'Workflows.hud.hud.get_psei_portfolio',
            'schedule': crontab(minute=5, hour='9,12,16', day_of_week='mon,tue,wed,thu,fri'),
            'args': ['AAAHeadless']
        },

    'run-hud-test-get_psei_orders':
        {
            'task': 'Workflows.hud.hud.get_psei_orders',
            'schedule': crontab(minute=20, hour='9,12,16', day_of_week='mon,tue,wed,thu,fri'),
            'args': ['AAAHeadless']
        },

    'run-hud-test-get_psei_portfolio_ticker':
        {
            'task': 'Workflows.hud.hud.get_psei_portfolio_ticker',
            'schedule': crontab(minute='10,40', hour='9,12,16', day_of_week='mon,tue,wed,thu,fri'),
            'args': ['AAAHeadless', 'Investagrams']
        },

    'run-hud-test-get_mtg_collection_trends':
        {
            'task': 'Workflows.hud.hud.get_mtg_collection_trends',
            'schedule': timedelta(hours=4),
            'args': ['EchoMTG']
        },


    #  endregion


}
