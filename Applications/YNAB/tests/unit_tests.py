import uuid
from datetime import datetime

from Applications.YNAB.references import *


class TestsYouNeedABudget(TestCase):

    def test_user_info_data(self):
        service = ApiServiceYNABUser(source_id='Tests_YNAB')
        data = service.get_user_info()
        assert_that(data, is_not(None))

    def test_get_budgets(self):
        service = ApiServiceYNABBudgets(source_id='Tests_YNAB')
        data = service.get_budgets()
        assert_that(len(data['budgets']), greater_than_or_equal_to(0))

    def test_get_budget_info(self):
        service = ApiServiceYNABBudgets(source_id='Tests_YNAB')
        data = service.get_budgets()

        target_budget = QList(data['budgets']).first()

        budget = service.get_budget_info(target_budget['id'])
        assert_that(len(budget['budget']), greater_than_or_equal_to(0))

    def test_get_accounts_in_budget(self):
        service = ApiServiceYNABBudgets(source_id='Tests_YNAB')
        current_budgets = service.get_budgets()

        target_budget = QList(current_budgets['budgets']).first()
        service = ApiServiceYNABAccounts(source_id='Tests_YNAB')
        current_accounts = service.get_accounts(target_budget['id'])

        assert_that(len(current_accounts), greater_than_or_equal_to(0))

    @pytest.mark.skip(reason=SKIP_TEST_TRANSACTION)
    def test_create_new_account_in_budget(self):
        service = ApiServiceYNABBudgets(source_id='Tests_YNAB')
        current_budgets = service.get_budgets()

        target_budget = QList(current_budgets['budgets'])\
            .where(lambda z: (z['name'] == service.parameters['budget_name']))\
            .first()
        service = ApiServiceYNABAccounts(source_id='Tests_YNAB')
        create_name = 'Test Account {0}'.format(uuid.uuid4())
        dto_account = DtoSaveAccountWrapper(
            account=DtoSaveAccount(name=create_name, type='savings', balance=0))

        current_accounts = service.create_new_account(target_budget['id'], dto_account)

        assert_that(create_name, equal_to(current_accounts['account']['name']))

    def test_get_categories_in_budget(self):
        service = ApiServiceYNABBudgets(source_id='Tests_YNAB')
        current_budgets = service.get_budgets()

        target_budget = QList(current_budgets['budgets']).first()
        service = ApiServiceYNABCategories(source_id='Tests_YNAB')
        current_categories = service.get_categories(target_budget['id'])

        assert_that(len(current_categories['category_groups']), greater_than_or_equal_to(0))

    def test_get_transactions(self):
        service = ApiServiceYNABBudgets(source_id='Tests_YNAB')
        current_budgets = service.get_budgets()

        target_budget = QList(current_budgets['budgets'])\
            .where(lambda z: (z['name'] == service.parameters['budget_name']))\
            .first()

        service = ApiServiceYNABTransactions(source_id='Tests_YNAB')
        current_transactions = service.get_transactions(target_budget['id'])

        assert_that(len(current_transactions['transactions']), greater_than_or_equal_to(0))

    def test_get_transactions_in_account(self):
        service = ApiServiceYNABBudgets(source_id='Tests_YNAB')
        current_budgets = service.get_budgets()

        target_budget = QList(current_budgets['budgets'])\
            .where(lambda z: (z['name'] == service.parameters['budget_name']))\
            .first()

        service = ApiServiceYNABAccounts(source_id='Tests_YNAB')
        current_account = QList(service.get_accounts(target_budget['id'])['accounts']).first()

        service = ApiServiceYNABTransactions(source_id='Tests_YNAB')
        current_transactions = service.get_transactions_per_account(target_budget['id'], current_account['id'])

        assert_that(len(current_transactions['transactions']), greater_than_or_equal_to(0))

    @pytest.mark.skip(reason=SKIP_TEST_TRANSACTION)
    def test_create_transaction(self):
        service = ApiServiceYNABBudgets(source_id='Tests_YNAB')
        current_budgets = service.get_budgets()
        target_budget = QList(current_budgets['budgets'])\
            .where(lambda z: (z['name'] == service.parameters['budget_name']))\
            .first()

        service = ApiServiceYNABCategories(source_id='Tests_YNAB')
        current_categories = service.get_categories(target_budget['id'])
        target_category_group = QList(current_categories['category_groups'])\
            .where(lambda z: (z['name'] == service.parameters['category_group_name']))\
            .first()
        target_category = QList(target_category_group['categories']).first()

        service = ApiServiceYNABAccounts(source_id='Tests_YNAB')
        current_account = QList(service.get_accounts(target_budget['id'])['accounts'])\
            .where(lambda z: (z['name'] == 'Loans'))\
            .first()
        account_id = current_account['id']

        service = ApiServiceYNABTransactions(source_id='Tests_YNAB')
        dto_transact = DtoSaveTransactionsWrapper(
            transaction=DtoSaveTransaction(
                account_id=account_id,
                date=datetime.today().strftime('%Y-%m-%d'),
                amount=100000930, # 100,000.930
                category_id=target_category['id'],
                memo='Test Memo',
                cleared='cleared',
                approved=True,


            )
        )

        data = service.create_new_transaction(target_budget['id'], dto_transact)

        assert_that(len(data['transaction_ids']), equal_to(1))

    @pytest.mark.skip(reason=SKIP_TEST_TRANSACTION)
    def test_create_multiple_transaction(self):
        service = ApiServiceYNABBudgets(source_id='Tests_YNAB')
        current_budgets = service.get_budgets()
        target_budget = QList(current_budgets['budgets'])\
            .where(lambda z: (z['name'] == service.parameters['budget_name']))\
            .first()

        service = ApiServiceYNABCategories(source_id='Tests_YNAB')
        current_categories = service.get_categories(target_budget['id'])
        target_category_group = QList(current_categories['category_groups'])\
            .where(lambda z: (z['name'] == service.parameters['category_group_name']))\
            .first()
        target_category = QList(target_category_group['categories']).first()

        service = ApiServiceYNABAccounts(source_id='Tests_YNAB')
        current_account = QList(service.get_accounts(target_budget['id'])['accounts'])\
            .where(lambda z: (z['name'] == service.parameters['account_name']))\
            .first()
        account_id = current_account['id']

        service = ApiServiceYNABTransactions(source_id='Tests_YNAB')
        dto_transact = DtoSaveTransactionsWrapper(
            transactions=[
                DtoSaveTransaction(
                    account_id=account_id,
                    date=datetime.today().strftime('%Y-%m-%d'),
                    amount=100000930, # 100,000.930
                    category_id=target_category['id'],
                    memo='Test Memo Multi 1',
                    cleared='cleared',
                    approved=True,


                ),
                DtoSaveTransaction(
                    account_id=account_id,
                    date=datetime.today().strftime('%Y-%m-%d'),
                    amount=0,  # 100,000.930
                    category_id=target_category['id'],
                    memo='Test Memo Multi 2',
                    cleared='cleared',
                    approved=True,

                ),
            ]
        )

        data = service.create_new_transaction(target_budget['id'], dto_transact)

        assert_that(len(data['transaction_ids']), len(dto_transact.transactions))