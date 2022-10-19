from ast import Try
from pydrive.drive import GoogleDrive
from pydrive.auth import GoogleAuth
from datetime import datetime


def drive_upload():
    try:
        GoogleAuth.DEFAULT_SETTINGS['client_config_file'] = 'CloudBackup\client_secrets.json'
        # Below code does the authentication
        # part of the code
        gauth = GoogleAuth()

        # Creates local webserver and auto
        # handles authentication.
        gauth.LocalWebserverAuth()	
        drive = GoogleDrive(gauth)
        
        now = datetime.now()
        fname = f'{now.strftime("%Y_%m_%d__%H_%M_%S")}.db'
        f = drive.CreateFile({'title': fname,'parents':[{'id':'1eT6PDeSS8VNd2SmdAgWfGUBQLiO30XFk'}]})
        f.SetContentFile("data\Seva_manager.db")
        f.Upload()

        # Due to a known bug in pydrive if we
        # don't empty the variable used to
        # upload the files to Google Drive the
        # file stays open in memory and causes a
        # memory leak, therefore preventing its
        # deletion
        f = None
    except Exception as e:
        print(e.with_traceback())
    

#Python main function
if __name__ == '__main__':
    drive_upload()

# End of code