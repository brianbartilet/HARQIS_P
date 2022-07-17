import json, os
from environment_variables import *


if __name__ == "__main__":

    if ENV_DEBUG == "1":
        config = "C:\\\\GIT\\wtw.bcuk.automation\\Core\\reporting\\allure_reports\\portal\\config\\default.json"
        uploads_path = "/Core/reporting/dashboard\\portal\\uploads"
    else:
        config  = os.path.join(os.getcwd(), "Core\\reporting\\allure_reports\\portal\\config") + "\\default.json"
        uploads_path = os.path.join(os.getcwd(), "Core\\reporting\\allure_reports\\portal\\uploads")

    with open(config) as h:
        data = json.load(h)
        for app in data['routes']:
            folder_app = os.path.join(uploads_path, app)
            if not os.path.exists(folder_app):
                os.makedirs(folder_app)

            for env in data['environments']:
                folder_env = os.path.join(folder_app, env)
                if not os.path.exists(folder_env):
                    os.makedirs(folder_env)

                for bgroup in data['bgroups']:
                    folder_bgroup = os.path.join(folder_env, bgroup)
                    if not os.path.exists(folder_bgroup):
                        os.makedirs(folder_bgroup)