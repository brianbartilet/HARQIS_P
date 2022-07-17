taskkill /f /im python.exe /t
taskkill /f /im flower.exe /t
taskkill /f /im node.exe /t


call environment.bat

call DailyDashboard/tasks/scripts/run_celery_scheduler.bat
call DailyDashboard/tasks/scripts/run_celery_scheduler_dashboard.bat
call DailyDashboard/tasks/scripts/run_celery_worker.bat

call DailyDashboard/tasks/scripts/run_flower.bat

call DailyDashboard/tasks/scripts/run_dashboard.bat