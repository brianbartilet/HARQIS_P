from Applications import *
from Core.utilities.multiprocess import *
from Core.utilities.csv_reader import *
import re
import csv
import uuid

from .mtg_collection import worker_get_notes, budget_types


@app.task()
@notify_work()
@elastic_logging()
def generate_collection_selling_jobs(path, script_file):
    #  temporary workaround for making google apis thread safe.. very shitty
    os.chdir(path)
    subprocess.run(["pytest", script_file])


@app.task()
@notify_work()
@elastic_logging()
def generate_collection_selling(echo_id,
                                google_sheet_app_id,
                                spreadsheet_name,
                                rate_conversion=40,
                                budget_type='standard',
                                gain_min_target=12,
                                gain_max_target=1000):

    collection_service = ApiServiceEchoMTGInventory(echo_id)
    collection = QList(collection_service.get_collection()['items'])\
        .where(lambda x: budget_types[budget_type](float(x['current_price'])))

    mp_client = MultiProcessingClient(tasks=collection, default_wait_secs=20)
    mp_client.execute_tasks(worker_get_notes, (mp_client.queue, mp_client.output_dict, echo_id))

    collection_with_notes = QList(mp_client.get_tasks_output())\
        .where(lambda x: 'TRADE' in x['output']['note']['note'])

    if gain_min_target is None:
        target_selling_collection = [x['task'] for x in collection_with_notes if float(x['task']['gain'])]
    else:
        target_selling_collection = [x['task'] for x in collection_with_notes if
                                     gain_max_target > float(x['task']['gain']) >= gain_min_target
                                     ]

    # parse data
    target_keys = ['tcg_mid',
                   'colors',
                   'name',
                   't',
                   'set',
                   'rarity',
                   'lang',
                   'condition',
                   'current_price',
                   'image',
                   'gain',
                   'foil'
                   ]
    cleaned_collection = []
    for dict_ in target_selling_collection:
        cleaned_collection.append({target_key: dict_[target_key] for target_key in target_keys })
    headers = ('CARD NAME',
               'SET EDITION',
               'FOIL',
               'RARITY',
               'LANGUAGE',
               'CONDITION',
               'COLORS',
               'TCG MID',
               'PRICE PHP',
               'IMAGE LINK')

    dump_rows = []
    for dict_ in cleaned_collection:
        dump_rows.append((
            str(dict_['name']),
            str(dict_['set']),
            'Y' if dict_['foil'] == '1' else '',
            str(dict_['rarity'])[0].upper(),
            str(dict_['lang']).upper(),
            str(dict_['condition']).upper(),
            str(dict_['colors']).title(),
            str(dict_['current_price']).title(),
            float(dict_['current_price'] if dict_['current_price'] is not None else 0) * rate_conversion,
            '=HYPERLINK("{0}", "Image")'.format(dict_['image'])
        ))

    #  Google Sheet Dump

    scopes = apps_config[google_sheet_app_id]['parameters']['scopes']
    service = ApiServiceGoogleSheets(source_id=google_sheet_app_id, scopes_list=scopes)

    row_length = len(service.get_sheet_data(spreadsheet_name))
    if not row_length == 0 and row_length > 3:
        service.clear_sheet_data(range_expression='{0}!3:{1}'.format(spreadsheet_name, row_length))

    service.set_headers(headers)
    service.set_row_data(dump_rows, sort_index=0)

    service.update_sheet_data('{0}!{1}'.format(spreadsheet_name, 'A2'))


@app.task()
@notify_work()
@elastic_logging()
def generate_collection_buylist(echo_id,
                                google_sheet_app_id,
                                spreadsheet_name,
                                echo_list_id):

    lists_service = ApiServiceEchoMTGLists(source_id=echo_id)
    lists_data = lists_service.get_list_data(echo_list_id)['list']['card_list']

    # parse data
    target_keys = ['foil_price',
                   'tcg_mid',
                   'name',
                   't',
                   'set',
                   'rarity',
                   'colors',
                   'image',
                   'foil'
                   ]
    cleaned_collection = []
    for key_id in lists_data:
        cleaned_collection.append({target_key: lists_data[key_id][target_key] for target_key in target_keys })

    headers = ('CARD NAME',
               'SET EDITION',
               'FOIL',
               'RARITY',
               'COLORS',
               'TCG MID',
               'IMAGE LINK')

    dump_rows = []
    for dict_ in cleaned_collection:
        dump_rows.append((
            str(dict_['name']),
            str(dict_['set']),
            'Y' if dict_['foil'] == '1' else '',
            str(dict_['rarity'])[0].upper(),
            str(dict_['colors']).title(),
            str(dict_['foil_price']).title() if dict_['foil'] == '1' else str(dict_['tcg_mid']).title(),
            '=HYPERLINK("{0}", "Image")'.format(dict_['image'])
        ))

    #  Google Sheet Dump

    scopes = apps_config[google_sheet_app_id]['parameters']['scopes']
    service = ApiServiceGoogleSheets(source_id=google_sheet_app_id, scopes_list=scopes)

    row_length = len(service.get_sheet_data(spreadsheet_name))
    if not row_length == 0 and row_length > 3:
        service.clear_sheet_data(range_expression='{0}!3:{1}'.format(spreadsheet_name, row_length))

    service.set_headers(headers)
    service.set_row_data(dump_rows, sort_index=0)

    service.update_sheet_data('{0}!{1}'.format(spreadsheet_name, 'A2'))


@app.task()
@notify_work()
@elastic_logging()
def run_elastic_logging():
    raise Exception
