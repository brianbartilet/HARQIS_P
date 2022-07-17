import shlex
import subprocess, psutil, os, uuid


def restart_celery_scheduler(app, task_file):
    pid_file = 'pid.{0}.{1}'\
        .format(restart_celery_scheduler.__name__, task_file).lower()

    if not os.path.isfile(pid_file):
        with open(pid_file, 'w'):
            pass

    with open(pid_file, 'r') as pid:
        target_process = pid.read()
        print("Target celery process id: {0}".format(target_process))

    try:
        for proc in psutil.process_iter():
            if proc.name() == 'celery.exe':
                cmd = 'taskkill /f /PID {0}'.format(target_process)
                subprocess.call(shlex.split(cmd))
                break
    except Exception:
        print("No celery beat process found")

    cmd = 'celery -A {0} beat -l info --pidfile='.format(app)
    process = subprocess.Popen(shlex.split(cmd)).pid

    with open(pid_file, 'w+') as pid:
        print("Saving celery process id: {0}".format(process))
        pid.write('{0}'.format(process))


def restart_celery_worker(app, task_file, use_eventlet=False, concurrency=10):

    pid_file = 'pid.{0}.{1}'.format(restart_celery_worker.__name__, task_file).lower()

    if not os.path.isfile(pid_file):
        with open(pid_file, 'w'):
            pass

    with open(pid_file, 'r') as pid:
        target_process = pid.read()
        print("Target celery process id: {0}".format(target_process))

    try:
        for proc in psutil.process_iter():
            if proc.name() == 'celery.exe':
                cmd = 'taskkill /f /PID {0}'.format(target_process)
                subprocess.call(shlex.split(cmd))
                break
    except Exception:
        print("No celery beat process found")

    cmd = 'celery -A {0} worker -l info --concurrency={2} -n {3}@%h -P {1}'\
        .format(app, 'eventlet' if use_eventlet else ' gevent', concurrency, task_file)

    process = subprocess.Popen(shlex.split(cmd)).pid

    with open(pid_file, 'w+') as pid:
        print("Saving celery process id: {0}".format(process))
        pid.write('{0}'.format(process))
