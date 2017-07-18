from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import logging
import time


def auto_drive(google_secret):
    """
    Automatically authorize use to log in Google drive. The first time requires web login.
    :return: Google drive object.
    """
    gauth = GoogleAuth()
    # Try to load saved client credentials
    gauth.LoadCredentialsFile(google_secret)
    if gauth.credentials is None:
        # Authenticate if they're not there
        gauth.LocalWebserverAuth()
    elif gauth.access_token_expired:
        # Refresh them if expired
        gauth.Refresh()
    else:
        # Initialize the saved creds
        gauth.Authorize()
    # Save the current credentials to a file
    gauth.SaveCredentialsFile(google_secret)
    drive = GoogleDrive(gauth)
    return drive


def upload_to_cloud(drive, file):

    submit = drive.CreateFile()
    submit.SetContentFile(file)
    submit.Upload()
    print("Upload a file to G-Drive.")
    logging.info("Upload a file to Google Drive at: {}".format(time.strftime("%Y-%m-%d %H:%M:%S")))