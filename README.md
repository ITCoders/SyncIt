# Sync It

SyncIt is a cross-platform client to synchronise work with your Google Drive folder.

This client is for public PCs like Computer Labs in colleges where multiple users would use same PCs and have problem in synchronising their works. This would provide a much better way to synchronise their work with Google Drive. User would login into their google account and then select their Google Drive folder they want to work. Then all files and subfolders of that folder would be downloaded locally. User would work in that local folder and after his work is finished, he would sign out and local work would be synchronised with Google Drive.

## Dependencies:
* Python 3.x
* PyDrive (Get it [here](https://github.com/googledrive/PyDrive))
* PyQt4

## Instructions
* This application requires an Google-Drive API key.
* To get an API key go to [API Console](https://code.google.com/apis/console) and make your own project.
* On ‘Services’ menu, turn Drive API on.
* On ‘API Access’ menu, create OAuth2.0 client ID, select application type to be web application and click on 'Download JSON'
* put `client_secrets.json` with `Drive_sync.py` to automate authentication flow. 
