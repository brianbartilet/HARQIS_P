import zipfile, os
from ftplib import FTP, error_perm


def move_files(ftp, path):
    for name in os.listdir(path):
        local_path = os.path.join(path, name)
        if os.path.isfile(local_path):
            print("STOR", name, local_path)
            ftp.storbinary('STOR ' + name, open(local_path, 'rb'))
        elif os.path.isdir(local_path):
            print("MKD", name)

            try:
                ftp.mkd(name)

            except error_perm as e:
                if not e.args[0].startswith('550'):
                    raise

            print("CWD", name)
            ftp.cwd(name)
            move_files(ftp, local_path)
            print("CWD", "..")
            ftp.cwd("..")


if __name__ == "__main__":
    path = os.environ["PATH_TO_DEPLOY"]
    app = os.environ["UPLOAD_FOLDER_APPLICATION_NAME"]

    ftp_host = os.environ["FTP_HOST"]
    ftp_user = os.environ["FTP_USER"]
    ftp_password = os.environ["FTP_PASSWORD"]

    allure_folder = os.environ["ALLURE_FOLDER"]
    print("PATH", allure_folder)

    #with zipfile.ZipFile(allure_folder + ".zip", "r") as zip_ref:
    #    zip_ref.extractall("tmp")

    with FTP(ftp_host) as ftp:
        ftp.login(user=ftp_user, passwd=ftp_password)
        ftp.getwelcome()
        ftp.cwd(path + "\\" + app)
        #local = "tmp\\" + allure_folder
        local = allure_folder
        move_files(ftp, local)










