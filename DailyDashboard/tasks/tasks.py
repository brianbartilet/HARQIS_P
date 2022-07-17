from Workflows import *
from DailyDashboard.tasks.apps import *
from environment_variables import *

"""
https://docs.celeryproject.org/en/stable/userguide/periodic-tasks.html


BUGS: https://github.com/eventlet/eventlet/issues/616

"""

CONFIG_DICTIONARY = {
    'DAILY_TASKS': DAILY_TASKS,
    'HUD_TASKS': HUD_TASKS,

}

app.conf.beat_schedule = CONFIG_DICTIONARY[ENV_TASK_APP]

app.conf.enable_utc = False
app.conf.timezone = 'Asia/Manila'