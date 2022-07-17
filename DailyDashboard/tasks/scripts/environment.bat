set ENV_ENV_APP_PATH=C:\GIT\HARQIS

cd %ENV_ENV_APP_PATH%

git pull

call venv\Scripts\activate.bat


rem SAMPLE FLOWER COMMAND:
rem set ENV=DEV
rem python ..\send_flower_task.py --task Workflows.workday.daily_punch.create_daily_health --args "DailyHealthForm" "Trello" "Daily Dashboard" "COMPLETED"