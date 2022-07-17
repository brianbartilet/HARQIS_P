import os.path

from Applications import *
from Workflows.finance.settings import *
from datetime import datetime, timedelta


@app.task()
@notify_work()
@elastic_logging()
def update_account_oanda(ynab_id, oanda_id, exchange_id, ynab_account_name, target_currency='PHP'):
    ynab_service_budgets = ApiServiceYNABBudgets(ynab_id)
    current_budgets = ynab_service_budgets.get_budgets()

    target_budget = QList(current_budgets['budgets']) \
        .where(lambda z: (z['name'] == ynab_service_budgets.parameters['budget_name'])) \
        .first()

    ynab_service_accounts = ApiServiceYNABAccounts(ynab_id)
    current_account = QList(ynab_service_accounts.get_accounts(target_budget['id'])['accounts']) \
        .where(lambda z: (z['name'] == ynab_account_name)) \
        .first()

    ynab_service_transact = ApiServiceYNABTransactions(ynab_id)

    service_oanda_account = ApiServiceAccount(source_id=oanda_id)

    account_data = service_oanda_account.get_account_info()
    account_trade = QList(account_data.accounts) \
        .first(lambda x: x.mt4AccountID == service_oanda_account.parameters['mt4AccountID'])
    account_details = service_oanda_account.get_account_details(account_trade.id)

    current_balance = float(account_details.balance)

    exchange_rate_service = ApiServiceCurrencyFreaksRates(exchange_id)
    current_rates = exchange_rate_service.get_latest_rates()
    current_rate = float(current_rates['rates'][target_currency])
    converted_balance = current_balance * current_rate

    computed = converted_balance - (current_account['balance'] / 1000)

    dto_oanda = DtoSaveTransaction(
            account_id=current_account['id'],
            date=datetime.today().strftime('%Y-%m-%d'),
            amount=int(round(float(computed), 2) * 1000),
            payee_name=oanda_id,
            memo='Current Balance @ {0} {1}{2}'.format(current_rate, 'USD', target_currency),
            cleared='cleared',
            approved=True
            )

    dto_transact = DtoSaveTransactionsWrapper(transactions=[dto_oanda, ])
    ynab_service_transact.create_new_transaction(target_budget['id'], dto_transact)


@app.task()
@notify_work()
@elastic_logging()
def create_transactions_from_account_sms_update(ynab_id,
                                                pushbullet_id,
                                                account_name,
                                                chat_name,
                                                mapping_key,
                                                hours_interval=24,
                                                default_category_group='Immediate',
                                                default_category='Spending Money'
                                                ):
    """
    Possible machine learning application for categories, use ElasticSearch

    """
    ynab_service_budgets = ApiServiceYNABBudgets(ynab_id)
    current_budgets = ynab_service_budgets.get_budgets()

    target_budget = QList(current_budgets['budgets']) \
        .where(lambda z: (z['name'] == ynab_service_budgets.parameters['budget_name'])) \
        .first()

    ynab_service_accounts = ApiServiceYNABAccounts(ynab_id)
    current_account = QList(ynab_service_accounts.get_accounts(target_budget['id'])['accounts']) \
        .where(lambda z: (z['name'] == account_name)) \
        .first()

    ynab_service_categories = ApiServiceYNABCategories(ynab_id)
    categories_ = ynab_service_categories.get_categories(target_budget['id'])
    category_group = QList(categories_['category_groups']).first(lambda x: x['name'] == default_category_group)
    category = QList(category_group['categories']).first(lambda x: x['name'] == default_category)

    ynab_service_transact = ApiServiceYNABTransactions(ynab_id)

    pb_service = ApiServicePushBulletChat(pushbullet_id)
    threads = pb_service.get_threads()['threads']

    try:
        target_thread = QList(threads).where(lambda x: x['recipients'][0]['name'] == chat_name).first()
    except StopIteration:
        return

    thread_info = pb_service.get_thread_items(target_thread['id'])
    now = datetime.now()
    last_day_threads = QList(thread_info['thread']).where(lambda x: now - timedelta(hours=hours_interval) <= datetime.fromtimestamp(x['timestamp']) <= now)

    new_items_transactions = []
    for item in last_day_threads:
        match = re.match(messages_mapping[mapping_key][0], item['body'])
        if match is not None:
            #  starts custom here
            amount = str(match.group(messages_mapping[mapping_key][1][0])).replace(',', '')
            recipient = match.group(messages_mapping[mapping_key][1][1])
            reference_id = match.group(messages_mapping[mapping_key][1][2])

            debit = -1 if messages_mapping[mapping_key][2] == 'debit' else 1
            new_items_transactions.append(
                DtoSaveTransaction(
                    account_id=current_account['id'],
                    date=datetime.fromtimestamp(item['timestamp']),
                    amount=int(round(float(amount), 2) * 1000 * debit),
                    payee_name=recipient,
                    memo='Reference: {0} '.format(reference_id),
                    cleared='cleared',
                    approved=False,
                    category_id=category['id']
                )
            )

    if len(new_items_transactions) > 0:
        dto_transact = DtoSaveTransactionsWrapper(transactions=new_items_transactions)
        ynab_service_transact.create_new_transaction(target_budget['id'], dto_transact)


@app.task()
@notify_work()
@elastic_logging()
@holidays_aware()
def update_daily_portfolio(ynab_id, trading_account_id_aaa, ynab_account_name):
    ynab_service_budgets = ApiServiceYNABBudgets(ynab_id)
    current_budgets = ynab_service_budgets.get_budgets()

    target_budget = QList(current_budgets['budgets']) \
        .where(lambda z: (z['name'] == ynab_service_budgets.parameters['budget_name'])) \
        .first()

    ynab_service_accounts = ApiServiceYNABAccounts(ynab_id)
    current_account = QList(ynab_service_accounts.get_accounts(target_budget['id'])['accounts']) \
        .where(lambda z: (z['name'] == ynab_account_name)) \
        .first()

    ynab_service_transact = ApiServiceYNABTransactions(ynab_id)

    webdriver_config = apps_config[trading_account_id_aaa]['webdriver']
    wdf = WebDriverFactory

    with wdf.create_webdriver(**webdriver_config) as driver:
        pl = PageAAALogin(driver, source_id=trading_account_id_aaa)
        pl.login()

        ptd = PageAAATradingDeskAccount(driver, source_id=trading_account_id_aaa)
        ptd.wait_page_to_load()
        portfolio_ = ptd.get_account_information()
        current_portfolio_balance = portfolio_.total_portfolio_value

    current_balance = current_account['balance'] / 1000

    computed = current_portfolio_balance - current_balance

    dto = DtoSaveTransaction(
            account_id=current_account['id'],
            date=datetime.today().strftime('%Y-%m-%d'),
            amount=int(round(float(computed), 2) * 1000),
            payee_name='AAA',
            memo='Daily Portfolio Update',
            cleared='uncleared',
            approved=True
            )

    dto_transact = DtoSaveTransactionsWrapper(transactions=[dto, ])
    ynab_service_transact.create_new_transaction(target_budget['id'], dto_transact)


@app.task()
@notify_work()
@elastic_logging()
def push_statement_to_account(ynab_id, ynab_account_name, csv_path_root, pattern_file='BPI_STATEMENT_{0}.csv'):
    today = datetime.today().strftime('%Y%m%d')
    csv_file = os.path.join(csv_path_root, pattern_file.format(today))

    ynab_service_budgets = ApiServiceYNABBudgets(ynab_id)
    current_budgets = ynab_service_budgets.get_budgets()

    target_budget = QList(current_budgets['budgets']) \
        .where(lambda z: (z['name'] == ynab_service_budgets.parameters['budget_name'])) \
        .first()

    ynab_service_accounts = ApiServiceYNABAccounts(ynab_id)
    current_account = QList(ynab_service_accounts.get_accounts(target_budget['id'])['accounts']) \
        .where(lambda z: (z['name'] == ynab_account_name)) \
        .first()

    ynab_service_transact = ApiServiceYNABTransactions(ynab_id)

    
    if os.path.exists(csv_file):
        transactions = generate_objects_from_csv_data(csv_file, DtoStatementTransaction,
                                                          convert_kwargs=True,
                                                          clean_chars=[' ', ','])

        total_amount = sum([float(x.amount) for x in transactions])


        dto_transact = DtoSaveTransactionsWrapper(transactions=[dto, ])
        ynab_service_transact.create_new_transaction(target_budget['id'], dto_transact)



        """
        {
   "transaction":{
      "account_id":"00d17281-a898-4bac-a3e4-0cbcb947c6e7",
      "date":"2020-02-18",
      "amount":-200000,
      "memo":"This is a split",
      "subtransactions":[
         {
            "amount":-100000,
            "payee_name":"Split payee",
            "category_id":"99e33804-e58f-4121-9930-ba013c8bb4c3",
            "memo":"Split 1"
         },
         {
            "amount":-100000,
            "payee_id":"f7d7779a-0084-4023-91fd-7de2a80f9105",
            "category_id":"3b9dcabc-ca09-4c7f-a26e-cb823209194d",
            "memo":"Split 2"
         }
      ]
   }
}
        
        """
