from Workflows.finance import *


class UnitTests(TestCase):

    def test_create_budget_transactions_from_collection(self):
        create_budget_transactions_from_collection(echo_id='EchoMTG', ynab_id='YNAB')

    def test_create_budget_transactions_from_collection_budget(self):
        create_budget_transactions_from_collection(echo_id='EchoMTG', ynab_id='YNAB', budget_type='penny')

    def test_update_budget_transactions_from_collection(self):
        update_budget_transactions_from_collection(echo_id='EchoMTG', ynab_id='YNAB')

    def test_update_budget_transactions_from_removed_collection(self):
        update_budget_transactions_from_removed_items_collection(echo_id='EchoMTG', ynab_id='YNAB')

    def test_update_collection_notes_for_trading_from_uncleared_budget_transactions(self):
        update_collection_notes_for_trading_from_uncleared_budget_transactions(echo_id='EchoMTG', ynab_id='YNAB')

    def test_update_collection_notes_for_trading_from_cleared_budget_transactions(self):
        update_collection_notes_for_trading_from_cleared_budget_transactions(echo_id='EchoMTG', ynab_id='YNAB')

    def test_update_budget_transactions_from_changed_price_budget_range(self):
        update_budget_transactions_from_changed_price_budget_range(echo_id='EchoMTG', ynab_id='YNAB')

    def test_generate_collection_spreadsheet(self):
        generate_collection_spreadsheet(echo_id='EchoMTG', spreadsheet_name='collection.csv', rate_conversion=35)

    def test_add_new_cards_from_csv_job(self):
        add_new_cards_from_csv_job(echo_id='EchoMTG',
                                   trello_id='Trello',
                                   jobs_board_name='Daily Dashboard',
                                   jobs_list_name='JOBS'
                                   )

    def test_generate_collection_selling(self):
        generate_collection_selling(echo_id='EchoMTG',
                                    google_sheet_app_id='GoogleAPIsSheet',
                                    spreadsheet_name='TEMPLATE')

    def test_generate_collection_selling_standard_lo(self):
        generate_collection_selling('EchoMTG',
                                    'GoogleAPIsSheet',
                                    'x35 USD',
                                    35,
                                    'standard',
                                    15)

    def test_generate_collection_selling_standard_hi(self):
        generate_collection_selling('EchoMTG',
                                    'GoogleAPIsSheet',
                                    'x40 USD',
                                    40,
                                    'standard',
                                    -1000,
                                    15)

    def test_generate_collection_selling_penny(self):
        generate_collection_selling('EchoMTG',
                                    'GoogleAPIsSheet',
                                    'x30 USD',
                                    30,
                                    'penny',
                                    None)

    def test_generate_collection_buylist(self):
        generate_collection_buylist('EchoMTG',
                                    'GoogleAPIsSheet',
                                    'MY WISHLIST',
                                    25878)

    def test_generate_collection_selling_jobs(self):
        generate_collection_selling_jobs(
            path="E:/GIT/HARQIS/Workflows/finance/tests",
            script_file="google.py"
        )

    def test_create_transactions_from_account_sms_update_gcash(self):
        create_transactions_from_account_sms_update(
            ynab_id='YNAB',
            pushbullet_id='PushBullet',
            account_name='CASH - GCash',
            chat_name='GCash',
            mapping_key='gcash_send'

        )

    def test_create_transactions_from_account_sms_update_gcash_receive(self):
        create_transactions_from_account_sms_update(
            ynab_id='YNAB',
            pushbullet_id='PushBullet',
            account_name='CASH - GCash',
            chat_name='GCash',
            mapping_key='gcash_receive',
            hours_interval=60

        )

    def test_create_transactions_from_account_sms_update_gcash_store(self):
        create_transactions_from_account_sms_update(
            ynab_id='YNAB',
            pushbullet_id='PushBullet',
            account_name='CASH - GCash',
            chat_name='GCash',
            mapping_key='gcash_payments_store',
            hours_interval=10000

        )

    def test_create_transactions_from_account_sms_update_gcash_payments(self):
        create_transactions_from_account_sms_update(
            ynab_id='YNAB',
            pushbullet_id='PushBullet',
            account_name='CASH - GCash',
            chat_name='GCash',
            mapping_key='gcash_payments',
            hours_interval=10000

        )

    def test_create_transactions_from_account_sms_update_gcash_payments_gcash_receive_bank(self):
        create_transactions_from_account_sms_update(
            ynab_id='YNAB',
            pushbullet_id='PushBullet',
            account_name='CASH - GCash',
            chat_name='GCash',
            mapping_key='gcash_receive_bank',
            hours_interval=50000

        )


    def test_update_account_oanda(self):
        update_account_oanda('YNAB', 'OANDA', 'CurrencyFreaks', 'FOREX - OANDA')

    def test_update_daily_portfolio(self):
        update_daily_portfolio('YNAB', 'AAA', 'STOCKS - AAA')

    def test_push_statement_to_account(self):
        push_statement_to_account('YNAB', 'CREDIT - BPI', 'C:/Users/brian/Downloads')