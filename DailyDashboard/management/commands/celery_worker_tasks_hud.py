from environment_variables import *

from django.core.management.base import BaseCommand
from django.utils import autoreload

from DailyDashboard.management.commands.helper import *


def restart_celery_worker_tasks_hud():
    restart_celery_worker('DailyDashboard', ENV_TASK_APP)


class Command(BaseCommand):

    def handle(self, *args, **options):
        print('Starting celery worker with autoreload...')

        # For Django>=2.2
        autoreload.run_with_reloader(restart_celery_worker_tasks_hud)

        # For django<2.1
        # autoreload.main(restart_celery)