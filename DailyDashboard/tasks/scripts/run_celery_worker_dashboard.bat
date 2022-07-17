set ENV=DEV
set ENV_TASK_APP=HUD_TASKS
start /high python.exe manage.py celery_worker_tasks_hud