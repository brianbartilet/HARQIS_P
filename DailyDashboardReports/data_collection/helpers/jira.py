from DailyDashboardReports.data_collection.helpers.elasticsearch import *
from DailyDashboardReports.data_collection.models.jira import *
from Core.utilities.multiprocess import *

import jsonmerge

INDEX_NAME_JIRA = 'jira_issue_collection'


@multiprocess_worker()
def worker_jira_issues(queue, index_name):
    while True:
        item = queue.get(block=False, timeout=None)
        ticket = load_jira_data_to_model(item)
        send_json_data_to_elastic_server(ticket.get_dict(), index_name, ticket.id)


def keys_exists(element: dict, *keys):
    """
    Check if *keys (nested) exists in `element` (dict).
    """
    if len(keys) == 0:
        raise AttributeError('No keys detected!')

    _element = element
    for key in keys:
        try:
            _element = _element[key]
        except Exception:
            return None

    return _element


def load_jira_data_to_model(data: dict):

    kwargs_mapping = {
        'id': keys_exists(data, 'id'),
        'key': keys_exists(data, 'key'),
        'url': keys_exists(data, 'self'),
        'issue_type': keys_exists(data, 'fields', 'issuetype', 'name'),
        'reporter': keys_exists(data, 'fields', 'reporter', 'displayName'),
        'assignee': keys_exists(data, 'fields', 'assignee', 'displayName'),
        'priority': keys_exists(data, 'fields', 'priority', 'name'),
        'created_date': keys_exists(data, 'fields', 'created'),
        'components': keys_exists(data, 'fields', 'customfield_17120', 'value'),
        'due_date': keys_exists(data, 'fields', 'duedate'),
        'status': keys_exists(data, 'fields', 'status', 'name'),
        'project': keys_exists(data, 'fields', 'project', 'name'),
        'project_key': keys_exists(data, 'fields', 'project', 'key'),
        'summary': keys_exists(data, 'fields', 'summary'),
        'environment': keys_exists(data, 'fields', 'customfield_10104', 'value')
    }

    return DtoJiraIssue(**kwargs_mapping)


def send_tickets_to_elastic_index_from_query(query: str, index_name=INDEX_NAME_JIRA):
    data = jira_server.get_project_issues(jquery_expression=query)

    log.info("Running JIRA query :: {0}".format(query))
    log.info("Got issue count: {0}".format(len(data['issues'])))

    mp_client = MultiProcessingClient(data['issues'], default_wait_secs=30)
    mp_client.execute_tasks(worker_jira_issues, (mp_client.queue, index_name))


