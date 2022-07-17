from Applications import *
from Core.utilities.multiprocess import *
from Core.utilities.csv_reader import *
import re
import csv
import uuid


budget_types = {
    'penny': lambda x: 0 <= x < 5,
    'standard': lambda x: x >= 5
}


@app.task()
@notify_work()
@elastic_logging()
def create_budget_transactions_from_collection(echo_id, ynab_id, budget_type='standard'):

    collection_service = ApiServiceEchoMTGInventory(echo_id)
    collection = QList(collection_service.get_collection()['items'])\
        .where(lambda x: budget_types[budget_type](float(x['current_price'])))

    collection_notes_service = ApiServiceEchoMTGNotes(echo_id)

    ynab_service = ApiServiceYNABBudgets(ynab_id)
    current_budgets = ynab_service.get_budgets()

    target_budget = QList(current_budgets['budgets']) \
        .where(lambda z: (z['name'] == ynab_service.parameters['budget_name'])) \
        .first()

    ynab_service = ApiServiceYNABAccounts(ynab_id)
    current_account = QList(ynab_service.get_accounts(target_budget['id'])['accounts']) \
        .where(lambda z: (z['name'] == ynab_service.parameters['account_name_' + budget_type])) \
        .first()

    ynab_service = ApiServiceYNABTransactions(ynab_id)
    current_transactions = ynab_service\
        .get_transactions_per_account(target_budget['id'], current_account['id'])['transactions']

    new_items = []
    skipped_items = []
    for item in collection:
        item_id = item['inventory_id']

        match = QList(current_transactions) \
            .where(lambda x: x['deleted'] is False) \
            .where(lambda x: x['memo'] is not None)\
            .where(lambda x: x['memo'] != '') \
            .first_or_default(lambda x: re.match(r"^.*\[(.*)\].*$", str(x['memo']))[1] == item_id)
        if match:
            skipped_items.append(item)
        else:
            new_items.append(item)

    for skipped in skipped_items:
        log.warning("Skipped Card: {0} - {1}".format(skipped['inventory_id'], skipped['name']))

    new_items_transactions = []
    for new_item in new_items:
        if new_item['note_id'] == '0':
            cleared = 'uncleared'
        else:
            note = collection_notes_service.get_note(new_item['note_id'])
            cleared = 'cleared' if 'HOLD' in note['note']['note'] else 'uncleared'

        new_items_transactions.append(
            DtoSaveTransaction(
                account_id=current_account['id'],
                date=new_item['date_acquired_html'],
                amount=int(round(float(collection_service.parameters['conversion_rate'])
                                 * float(new_item['current_price']), 2) * 1000),
                memo="[{0}]  {3} - {4}  -  {5}  ${1}  {2}%"
                    .format(new_item['inventory_id'],
                            new_item['current_price'],
                            round(float(new_item['personal_gain']) * 100, 0),
                            new_item['name'],
                            new_item['expansion'],
                            "FOIL" if new_item['foil'] == '1' else ""
                            ),
                cleared=cleared,
                approved=True
            )
        )

    if len(new_items_transactions) > 0:
        dto_transact = DtoSaveTransactionsWrapper(transactions=new_items_transactions)
        ynab_service.create_new_transaction(target_budget['id'], dto_transact)
    else:
        log.warning("No new items found.")


@app.task()
@notify_work()
@elastic_logging()
def update_budget_transactions_from_collection(echo_id, ynab_id, budget_type='standard'):
    collection_service = ApiServiceEchoMTGInventory(echo_id)
    collection = QList(collection_service.get_collection()['items'])\
        .where(lambda x: budget_types[budget_type](float(x['current_price'])))

    collection_notes_service = ApiServiceEchoMTGNotes(echo_id)

    ynab_service = ApiServiceYNABBudgets(ynab_id)
    current_budgets = ynab_service.get_budgets()

    target_budget = QList(current_budgets['budgets']) \
        .where(lambda z: (z['name'] == ynab_service.parameters['budget_name'])) \
        .first()

    ynab_service = ApiServiceYNABAccounts(ynab_id)
    current_account = QList(ynab_service.get_accounts(target_budget['id'])['accounts']) \
        .where(lambda z: (z['name'] == ynab_service.parameters['account_name_' + budget_type])) \
        .first()

    ynab_service = ApiServiceYNABTransactions(ynab_id)
    current_transactions = ynab_service \
        .get_transactions_per_account(target_budget['id'], current_account['id'])['transactions']

    updated_items = []
    for item in collection:
        item_id = item['inventory_id']
        match = QList(current_transactions) \
            .where(lambda x: x['deleted'] is False) \
            .where(lambda x: x['memo'] is not None) \
            .where(lambda x: x['memo'] != '') \
            .first_or_default(lambda x: re.match(r"^.*\[(.*)\].*$", str(x['memo']))[1] == item_id)
        if match:
            search_string = " ${0} ".format(item['current_price'])
            if search_string not in match['memo']:
                updated_items.append((item, match))
            elif item['date_acquired_html'] != match['date']:
                updated_items.append((item, match))
            else:
                continue

    updated_items_transactions = []
    for updated_item, match in updated_items:

        if updated_item['note_id'] == '0':
            cleared = 'uncleared'
        else:
            note = collection_notes_service.get_note(updated_item['note_id'])
            cleared = 'cleared' if 'HOLD' in note['note']['note'] else 'uncleared'

        updated_items_transactions.append(
            DtoUpdateTransaction(
                id=match['id'],
                account_id=current_account['id'],
                date=updated_item['date_acquired_html'],
                amount=int(round(float(collection_service.parameters['conversion_rate'])
                                 * float(updated_item['current_price']), 2)
                           * 1000),
                memo="[{0}]  {3} - {4}  -  {5}  ${1}  {2}%"
                    .format(updated_item['inventory_id'],
                            updated_item['current_price'],
                            round(float(updated_item['personal_gain']) * 100, 0),
                            updated_item['name'],
                            updated_item['expansion'],
                            "FOIL" if updated_item['foil'] == '1' else ""
                            ),
                cleared=cleared,
                approved=True
            )
        )
        log.warning("Updating Transaction with Card: {0} - {1}"
                    .format(updated_item['name'], updated_item['set_code'].upper()))

    if len(updated_items_transactions) > 0:
        dto_transact = DtoSaveTransactionsWrapper(transactions=updated_items_transactions)
        ynab_service.update_transaction(target_budget['id'], dto_transact)
    else:
        log.warning("No items to update.")


@app.task()
@notify_work()
@elastic_logging()
def update_budget_transactions_from_removed_items_collection(echo_id, ynab_id, budget_type='standard'):
    collection_service = ApiServiceEchoMTGInventory(echo_id)
    removed_collection = QList(collection_service.get_collection_dump()['inventoryData'])\
        .where(lambda x: x['d'] is not None)

    ynab_service = ApiServiceYNABBudgets(ynab_id)
    current_budgets = ynab_service.get_budgets()

    target_budget = QList(current_budgets['budgets']) \
        .where(lambda z: (z['name'] == ynab_service.parameters['budget_name'])) \
        .first()

    ynab_service = ApiServiceYNABAccounts(ynab_id)
    current_account = QList(ynab_service.get_accounts(target_budget['id'])['accounts']) \
        .where(lambda z: (z['name'] == ynab_service.parameters['account_name_' + budget_type])) \
        .first()

    ynab_service = ApiServiceYNABTransactions(ynab_id)
    current_transactions = ynab_service \
        .get_transactions_per_account(target_budget['id'], current_account['id'])['transactions']

    remove_items = []
    for item in removed_collection:
        item_id = item['i']
        match = QList(current_transactions) \
            .where(lambda x: x['deleted'] is False) \
            .where(lambda x: x['memo'] is not None) \
            .where(lambda x: x['memo'] != '') \
            .first_or_default(lambda x: re.match(r"^.*\[(.*)\].*$", str(x['memo']))[1] == item_id)
        if match:
            if "SOLD/TRADED" in match['memo']:
                continue
            remove_items.append((item, match))

    updated_items_transactions = []
    for updated_item, match in remove_items:
        updated_items_transactions.append(
            DtoUpdateTransaction(
                id=match['id'],
                account_id=current_account['id'],
                date=str(updated_item['d']).split(' ')[0],
                amount=0,
                memo="{0} SOLD/TRADED".format(match['memo']),
                cleared='cleared',
                approved=True
            )
        )
        log.warning("Updating/Removing Transaction with Card: {0}".format(match['memo']))

    if len(updated_items_transactions) > 0:
        dto_transact = DtoSaveTransactionsWrapper(transactions=updated_items_transactions)
        ynab_service.update_transaction(target_budget['id'], dto_transact)
    else:
        log.warning("No items to remove.")


@app.task()
@notify_work()
@elastic_logging()
def update_budget_transactions_from_changed_price_budget_range(echo_id, ynab_id):
    for budget_type in budget_types:

        collection_service = ApiServiceEchoMTGInventory(echo_id)
        collection_price_change = QList(collection_service.get_collection()['items']) \
            .where(lambda x: not budget_types[budget_type](float(x['current_price'])))

        ynab_service = ApiServiceYNABBudgets(ynab_id)
        current_budgets = ynab_service.get_budgets()

        target_budget = QList(current_budgets['budgets']) \
            .where(lambda z: (z['name'] == ynab_service.parameters['budget_name'])) \
            .first()

        ynab_service = ApiServiceYNABAccounts(ynab_id)
        current_account = QList(ynab_service.get_accounts(target_budget['id'])['accounts']) \
            .where(lambda z: (z['name'] == ynab_service.parameters['account_name_' + budget_type])) \
            .first()

        ynab_service = ApiServiceYNABTransactions(ynab_id)
        current_transactions = ynab_service \
            .get_transactions_per_account(target_budget['id'], current_account['id'])['transactions']

        remove_items = []
        for check_price_change in collection_price_change:
            try:
                match = QList(current_transactions)\
                    .first_or_default(lambda x: re.match(r"^.*\[(.*)\].*$", str(x['memo']))[1] ==
                                                check_price_change['inventory_id'])
            except Exception as e:
                continue
            if match:
                remove_items.append((check_price_change, match))


        updated_items_transactions = []
        for updated_item, match in remove_items:
            updated_items_transactions.append(
                DtoUpdateTransaction(
                    id=match['id'],
                    account_id=current_account['id'],
                    date=match['date'],
                    amount=0,
                    memo="{0} PRICE CHANGED".format(str(match['memo']).replace('PRICE CHANGED', '')),
                    cleared='cleared',
                    approved=True
                )
            )
            log.warning("Updating/Removing Transaction with Card: {0}".format(match['memo']))

        if len(updated_items_transactions) > 0:
            dto_transact = DtoSaveTransactionsWrapper(transactions=updated_items_transactions)
            ynab_service.update_transaction(target_budget['id'], dto_transact)
        else:
            log.warning("No items to remove.")


@app.task()
@notify_work()
@elastic_logging()
def update_collection_notes_for_trading_from_uncleared_budget_transactions(echo_id, ynab_id, budget_type='standard'):
    collection_service = ApiServiceEchoMTGInventory(echo_id)
    collection = QList(collection_service.get_collection_dump()['inventoryData'])
    collection_view = QList(collection_service.get_collection()['items'])\
        .where(lambda x: budget_types[budget_type](float(x['current_price'])))

    ynab_service = ApiServiceYNABBudgets(ynab_id)
    current_budgets = ynab_service.get_budgets()

    target_budget = QList(current_budgets['budgets']) \
        .where(lambda z: (z['name'] == ynab_service.parameters['budget_name'])) \
        .first()

    ynab_service = ApiServiceYNABAccounts(ynab_id)
    current_account = QList(ynab_service.get_accounts(target_budget['id'])['accounts']) \
        .where(lambda z: (z['name'] == ynab_service.parameters['account_name_' + budget_type])) \
        .first()

    ynab_service = ApiServiceYNABTransactions(ynab_id)
    current_transactions = ynab_service \
        .get_transactions_per_account(target_budget['id'], current_account['id'])['transactions']

    uncleared_items = []
    for item in collection:
        item_id = item['i']
        match = QList(current_transactions) \
            .where(lambda x: str(x['cleared']).strip() == 'uncleared')\
            .where(lambda x: x['deleted'] is False) \
            .where(lambda x: x['memo'] is not None) \
            .where(lambda x: x['memo'] != '') \
            .first_or_default(lambda x: re.match(r"^.*\[(.*)\].*$", str(x['memo']))[1] == item_id)
        if match:
            uncleared_items.append((item, match))

    collection_service = ApiServiceEchoMTGNotes(echo_id)

    if len(uncleared_items) > 0:
        for updated_item, match in uncleared_items:
            try:
                inventory_item_view = QList(collection_view).first(lambda x: str(x['inventory_id']) == str(updated_item['i']))
            except:
                log.warning('Error on {0}'.format(updated_item))

            if inventory_item_view['note_id'] == '0':
                collection_service.create_note(inventory_item_view['inventory_id'], "{0}".format("[SELL/TRADE]"))
            else:
                collection_service.update_note(inventory_item_view['note_id'], "{0}".format("[SELL/TRADE]"))

            log.warning("Updating Transaction with Trading/Selling Card: {0}".format(match['memo']))
    else:
        log.warning("No items to update for trading/selling.")


@app.task()
@notify_work()
@elastic_logging()
def update_collection_notes_for_trading_from_cleared_budget_transactions(echo_id, ynab_id, budget_type='standard'):
    collection_service = ApiServiceEchoMTGInventory(echo_id)
    collection = QList(collection_service.get_collection_dump()['inventoryData'])
    collection_view = QList(collection_service.get_collection()['items'])\
        .where(lambda x: budget_types[budget_type](float(x['current_price'])))

    ynab_service = ApiServiceYNABBudgets(ynab_id)
    current_budgets = ynab_service.get_budgets()

    target_budget = QList(current_budgets['budgets']) \
        .where(lambda z: (z['name'] == ynab_service.parameters['budget_name'])) \
        .first()

    ynab_service = ApiServiceYNABAccounts(ynab_id)
    current_account = QList(ynab_service.get_accounts(target_budget['id'])['accounts']) \
        .where(lambda z: (z['name'] == ynab_service.parameters['account_name_' + budget_type])) \
        .first()

    ynab_service = ApiServiceYNABTransactions(ynab_id)
    current_transactions = ynab_service \
        .get_transactions_per_account(target_budget['id'], current_account['id'])['transactions']

    cleared_items = []
    for item in collection:
        item_id = item['i']
        match = QList(current_transactions) \
            .where(lambda x: str(x['cleared']).strip() == 'cleared')\
            .where(lambda x: x['deleted'] is False) \
            .where(lambda x: x['memo'] is not None) \
            .where(lambda x: x['memo'] != '') \
            .first_or_default(lambda x: re.match(r"^.*\[(.*)\].*$", str(x['memo']))[1] == item_id)
        if match:
            cleared_items.append((item, match))

    collection_service = ApiServiceEchoMTGNotes(echo_id)

    if len(cleared_items) > 0:
        for updated_item, match in cleared_items:

            try:
                inventory_item_view = QList(collection_view).first(lambda x: x['inventory_id'] == updated_item['i'])
                if inventory_item_view['note_id'] == '0':
                    collection_service.create_note(inventory_item_view['inventory_id'], "{0}".format("[HOLD]"))
                else:
                    collection_service.update_note(inventory_item_view['note_id'], "{0}".format("[HOLD]"))

                log.warning("Updating Transaction with For Holding Card: {0}".format(match['memo']))
            except Exception:
                log.warning("Skipping card already sold. {0}".format(match['memo']))
    else:
        log.warning("No items to update for trading/selling.")


@multiprocess_worker()
def worker_get_notes(queue, output_dict, echo_id):
    notes_service = ApiServiceEchoMTGNotes(echo_id)
    while True:
        item = queue.get(block=False, timeout=None)
        output_dict['result_{0}_{1}'.format(item['note_id'], uuid.uuid4())] \
            = {'task': item, 'output': notes_service.get_note(item['note_id'])}


@multiprocess_worker()
def worker_add_card(queue, output_dict, echo_id, foil_index):
    collection_service = ApiServiceEchoMTGInventory(echo_id)
    while True:
        item_mtg_card = queue.get(block=False, timeout=None)
        dto_card = DtoEchoMTGCard(
            mid=item_mtg_card.multiverseid,
            foil=foil_index
        )
        output_dict['result_{0}'.format(uuid.uuid4())] \
            = {'task': dto_card.mid, 'output': collection_service.add_card_to_collection(dto_card)}


@app.task()
def generate_collection_spreadsheet(echo_id, spreadsheet_name, rate_conversion):
    collection_service = ApiServiceEchoMTGInventory(echo_id)
    collection = collection_service.get_collection()['items']

    mp_client = MultiProcessingClient(tasks=collection, default_wait_secs=20)
    mp_client.execute_tasks(worker_get_notes, (mp_client.queue, mp_client.output_dict, echo_id))
    collection_with_notes = QList(mp_client.get_tasks_output())\
        .where(lambda x: 'TRADE' in x['output']['note']['note'])

    output_file = os.path.join(os.getcwd(), spreadsheet_name)

    with open(output_file, mode='w', newline='') as csv_file:
        fieldnames = ['Name',
                      'Rarity',
                      'Foil',
                      'Edition',
                      'Type',
                      'Colors',
                      'Condition',
                      'USD TCG Mid',
                      'PHP x{0}'.format(rate_conversion),
                      ]

        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()

        for item in collection_with_notes:
            item = item['task']
            target_price = float(float(item['current_price']) * rate_conversion)

            writer.writerow(
                {
                    'Name': '=HYPERLINK("{0}", "{1}")'.format(item['image'], item['name']),
                    'Rarity': str(item['rarity'])[0].upper(),
                    'Foil': 'Y' if item['foil'] == '1' else '',
                    'Edition': item['expansion'],
                    'Type': item['t'],
                    'Colors': item['colors'],
                    'Condition': item['condition'],
                    'USD TCG Mid': item['current_price'],
                    'PHP x{0}'.format(rate_conversion): str(round(target_price, 2)),


                }
            )


@app.task()
def add_new_cards_from_csv_job(echo_id,
                               trello_id,
                               jobs_board_name,
                               jobs_list_name,
                               ):
    file_ext = '.csv'
    current_cards, id_list, target_board = get_board_data(trello_id, jobs_board_name, jobs_list_name)

    service_trello_cards = ApiServiceCards(trello_id)
    service_trello_boards = ApiServiceBoards(trello_id)

    parsed_labels = [l.id for l in QList(service_trello_boards.get_board_labels(target_board))
        .where(lambda x: x.name in ['DONE'])]

    jobs = QList(current_cards)\
        .where(lambda x: echo_id in x.name)\
        .where(lambda x: not [i for i in x.id_labels if i in parsed_labels])

    for card_ in jobs:
        use_attachment = QList(service_trello_cards.get_attachments(card_id=card_.id))\
            .where(lambda x: file_ext in x.file_name)\
            .first()

        dl_attachment = service_trello_cards.get_attachment(card_.id, use_attachment.id)
        file_name = service_trello_cards.download_attachment(
            attachment_url=dl_attachment.url,
            attachment_id=dl_attachment.id,
            file_type=file_ext,

        )

        objects = generate_objects_from_csv_data(file_name, DtoDelverLensMTGCard)
        foil_index = 1 if '[F]' in card_.name else 0
        mp_client = MultiProcessingClient(tasks=objects, default_wait_secs=40, worker_count=4)
        mp_client.execute_tasks(worker_add_card, (mp_client.queue, mp_client.output_dict, echo_id, foil_index))

        dump = ''
        for output_task in mp_client.get_tasks_output():
            dump = dump + "\nmid: {0} status: {1} {2} - {3}".format(
                                                        keys_exists(output_task, 'task'),
                                                        keys_exists(output_task, 'output', 'status'),
                                                        keys_exists(output_task, 'output', 'card', 'card_name'),
                                                        keys_exists(output_task, 'output', 'card', 'expansion')
            )

        if 'error' in dump:
            parsed_labels = [l.id for l in QList(service_trello_boards.get_board_labels(target_board))
                .where(lambda x: x.name in ['DONE', 'ERROR'])]

        service_trello_cards.update_card(DtoCard(id=card_.id, idLabels=parsed_labels, desc=dump))





