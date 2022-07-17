from Applications.ELK.references import *
import jsonmerge
import uuid


APP_NAME = "ElasticSearch"
LOGGING_INDEX = 'harqis_metrics'
ELASTIC_TIME_FORMAT = '%Y-%m-%dT%H:%M'


def elastic_logging(source_id=APP_NAME, override=False):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if ENV_TESTENV == SettingsEnvironment.DEV.value and override is False:
                return func(*args, **kwargs)
            path = "{0}.{1}".format(func.__module__, func.__qualname__)
            try:
                logs = QList(get_index_data_from_elastic(LOGGING_INDEX, source_id, DtoFunctionLogger))

                target = logs.where(lambda x: x.name == path).first() if len(logs) > 0 else None
            except Exception:
                target = None
            args_str = ''.join(['"{0}" '.format(str(arg)) for arg in args])
            index_dto = DtoFunctionLogger(name=path,
                                          passed=0,
                                          failed=0,
                                          last_failed='2000-01-01T00:00',
                                          pass_fail_percent=0,
                                          exception_message='None',
                                          args=args_str) \
                if not target else target

            f = error = None
            now = datetime.now().strftime(ELASTIC_TIME_FORMAT)
            try:
                f = func(*args, **kwargs)
                index_dto.passed += 1
            except Exception as e:
                error = e
                index_dto.failed += 1
                index_dto.last_failed = now
                index_dto.exception_message = error.__class__.__name__
                index_dto.args = args_str
            finally:
                index_dto.date = now
                index_dto.compute_stat()

                send_json_data_to_elastic_server(app_config_name=APP_NAME,
                                                 json_dump=index_dto.get_dict(),
                                                 index_name=LOGGING_INDEX,
                                                 use_interval_map=False,
                                                 location_key=path)
                if error:
                    raise error

            return f

        return wrapper

    return decorator


def send_json_data_to_elastic_server(json_dump, index_name: str, location_key: str,
                                     app_config_name=APP_NAME, use_interval_map=True, identifier=''):

    update_interval_config = str(apps_config[app_config_name]['update_interval']).upper()
    if use_interval_map:
        id_ = '_' + update_interval_map[update_interval_config]
    else:
        id_ = '' if len(identifier) == 0 else '_' + identifier

    loc = location_key + id_

    print("Using {0} interval with generated location key {1}".format(update_interval_config, loc))

    tmp_json = '{0}.json'.format(uuid.uuid4())
    result = jsonmerge.merge({"date": datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%f')}, json_dump)

    with open(tmp_json, 'w') as f:
        json.dump(result, f)

    headers = {'Content-Type': 'application/json'}
    if apps_config[app_config_name]['use_basic_auth']:
        headers['Authorization'] = "Basic {0}".format(apps_config[app_config_name]['basic_auth'])

    proxies = apps_config[app_config_name]['proxies'] if str(ENV_ENABLE_PROXY).lower() == "true" else {}

    with open(tmp_json, 'rb') as f:
        response = requests.post(
            url="{0}/{1}/_doc/{2}".format(apps_config[app_config_name]['url'], index_name, loc),
            proxies=proxies,
            headers=headers,
            data=f.read()
        )
    print('Sending data from item {0} got response: {1}'.format(location_key, response.status_code))
    os.remove(tmp_json)
    assert_that(response.status_code, any_of(equal_to(HTTPStatus.CREATED), equal_to(HTTPStatus.OK)))
    # TODO: handle this
    # https://stackoverflow.com/questions/50609417/elasticsearch-error-cluster-block-exception-forbidden-12-index-read-only-all


def get_index_data_from_elastic(index_name: str, app_config_name=APP_NAME, type_hook=None, fetch_docs=10000):

    headers = {'Content-Type': 'application/json'}
    if apps_config[app_config_name]['use_basic_auth']:
        headers['Authorization'] = "Basic {0}".format(apps_config[app_config_name]['basic_auth'])

    proxies = apps_config[app_config_name]['proxies'] if str(ENV_ENABLE_PROXY).lower() == "true" else {}

    response = requests.get(
        url="{0}/{1}/_search?size={2}&pretty=true&q=*:*".format(apps_config[app_config_name]['url'],
                                                                index_name,
                                                                fetch_docs),
        proxies=proxies,
        headers=headers)
    assert_that(response.status_code, any_of(equal_to(HTTPStatus.CREATED), equal_to(HTTPStatus.OK)))

    docs_list = ApiResponse(type_hook=dict, data=response.content).deserialized_data['hits']['hits']

    out = []
    if type_hook is None:
        out = docs_list
    else:
        for doc in docs_list:
            out.append(type_hook(**doc['_source']))

    return out