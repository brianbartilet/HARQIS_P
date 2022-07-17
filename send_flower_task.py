import requests, json, argparse, sys
from Applications.load_config import apps_config
from environment_variables import *


def main():
    parser = argparse.ArgumentParser(description='Input task url')
    parser.add_argument('--task',
                        help='application task full path e.g. Workflows.workday.daily_punch.punch_out',
                        dest='task', default='Workflow')
    parser.add_argument('--args', nargs='*', help='arguments quotes seperated')

    parsed_args = parser.parse_args()

    config = apps_config['Flower']
    task_api = '{}/task'.format(config['url'])
    args = {'args': parsed_args.args}
    url = '{0}/async-apply/{1}'.format(task_api, parsed_args.task)
    requests.post(url, data=json.dumps(args))


if __name__ == '__main__':
    main()
    #  sample command: python send_flower_task.py --task Workflows.workday.daily_punch.punch_out --args PeonAllSec