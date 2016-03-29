import os
import webbrowser
#from subprocess import call

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

HOME_DIRECTORY="G:\\"
ROOT_FOLDER_NAME="SyncIt"
#----------------------------------
#function for login
def Login():
    gauth=GoogleAuth()
    gauth.LocalWebserverAuth()
    gauth.Authorize()
    drive=GoogleDrive(gauth)
    return drive
#----------------------------------

#funtion of getting id of a given filename
def id_of_title(title,parent_directory_id):
    foldered_list=drive.ListFile({'q':  "'"+parent_directory_id+"' in parents and trashed=false"}).GetList()
    for file in foldered_list:
        if(file['title']==title):
            return file['id']
    return None
#---------------------------------------
def create_folder(id, subfolder):
    newFolder = drive.CreateFile({'title': subfolder, "parents": [{"kind": "drive#fileLink", "id": id}],
                                     "mimeType": "application/vnd.google-apps.folder"})
    newFolder.Upload()
    return newFolder
#---------------------------------------
#function of downloading folder of given folder id from drive to local
def download(folder_id,destination_location):
    if not os.path.exists(destination_location):
        os.makedirs(destination_location)
    foldered_list=drive.ListFile({'q':  "'"+folder_id+"' in parents and trashed=false"}).GetList()
    for file2 in foldered_list:
        if file2['mimeType']=='application/vnd.google-apps.folder':
            download(file2['id'],destination_location+os.path.sep+file2['title'])
        # print ('title: %s, id: %d' % (file2['title'], file2['size']))
        else:
            open(destination_location+os.path.sep+file2['title'],'w+')
            local_size=os.path.getsize(destination_location+os.path.sep+file2['title'])
            drive_size=file2['fileSize']
            if local_size!=drive_size:
                file=drive.CreateFile({'id': file2['id']})
                file.GetContentFile(destination_location+os.path.sep+file2['title'])
#-------------------------------------------------------

donePaths=[]
#function for uploading source location to designated id
def upload(source_location, id):
    for folderName, subfolders, filenames in os.walk(source_location):
        if folderName not in donePaths:
            if filenames:
                for filename in filenames:
                    file_id=id_of_title(filename,id)
                    if file_id!=None:
                        file_drive=drive.CreateFile({'id':file_id})
                        drive_file_size=file_drive['fileSize']
                        local_file_size=os.path.getsize(folderName+os.path.sep+filename)
                        if drive_file_size!=str(local_file_size):
                            file_drive.SetContentFile(folderName+os.path.sep+filename)
                            file_drive.Upload()
                        # else:
                        #     #blank
                    else:
                        newfile = drive.CreateFile({'title': filename,"parents": [{"kind":"drive#fileLink","id":id}]})
                        newfile.SetContentFile(folderName+os.path.sep+filename)
                        newfile.Upload()
            if subfolders:
                for subfolder in subfolders:
                    subfolder_id=id_of_title(subfolder,id)
                    if subfolder_id!=None:
                        absPath = os.path.join(folderName,subfolder)
                        upload(absPath,subfolder_id)
                        donePaths.append(absPath)
                    else:
                        newSubFolder = create_folder(id, subfolder)
                        subfolder_id=newSubFolder['id']
                        absPath = os.path.join(folderName,subfolder)
                        upload(absPath,subfolder_id)
                        donePaths.append(absPath)
#----------------------------------------------
#function for creating a folder and upload into that
def uploadFolder(source_location,parent_id):
    folder_name=os.path.split(source_location)[1]
    id_of_folder=id_of_title(folder_name,parent_id)
    if(id_of_folder==None):
        newFolder=drive.CreateFile({'title': folder_name,"parents": [{"kind":"drive#fileLink","id":parent_id}],"mimeType": "application/vnd.google-apps.folder"})
        newFolder.Upload()
        id_of_folder=newFolder['id']
    upload(source_location,id_of_folder)
#---------------------------------------------------
#function for returning file tree structure from parentid
def ListFolder(parent):
  filelist=[]
  file_list = drive.ListFile({'q': "'%s' in parents and trashed=false" % parent}).GetList()
  for f in file_list:
    if f['mimeType']=='application/vnd.google-apps.folder': # if folder
        filelist.append({"id":f['id'],"title":f['title'],"list":ListFolder(f['id'])})
    else:
        filelist.append(f['title'])
  return filelist
#-------------------------------------------------------
def get_username(drive_object):
    file_list = drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
    for file1 in file_list:
        emailId = list(file1["owners"])[0]["emailAddress"]
    return str(emailId)[:9]
#----------------------------------------------------
#function for browsing into drive directory
browsed=[]
def folder_browser(structure,id):
    for element in structure:
        if type(element) is dict:
            print (element['title'])
        else:
            print (element)
    print("Enter Name of Folder You Want to Use\nEnter '/' to use current folder\nEnter ':' to create New Folder and use that" )
    inp=input()
    if inp=='/':
        return id
    elif inp==':':
        print("Enter Name of Folder You Want to Create")
        inp=input()
        newfolder=create_folder(id,inp)
        if not os.path.exists(HOME_DIRECTORY+ROOT_FOLDER_NAME+os.path.sep+USERNAME):
            os.makedirs(HOME_DIRECTORY+ROOT_FOLDER_NAME+os.path.sep+USERNAME)
        return newfolder['id']

    else:
        folder_selected=inp
        for element in structure:
            if type(element) is dict:
                if element["title"]==folder_selected:
                    struc=element["list"]
                    browsed.append(folder_selected)
                    print("Inside "+folder_selected)
                    return folder_browser(struc,element['id'])
#-----------------------------------------------------
drive=Login()
print("Complete Authentication Flow First")
USERNAME=get_username(drive)
print("Logged in as "+USERNAME)
root_id=id_of_title(ROOT_FOLDER_NAME,'root')
if root_id==None:
    root_id=create_folder('root',ROOT_FOLDER_NAME)['id']
structure=ListFolder(root_id)
print("Your Existing File Directory")
id_of_working_drive_folder=folder_browser(structure,root_id)
path=HOME_DIRECTORY+ROOT_FOLDER_NAME+os.path.sep+USERNAME
for i in browsed:
    path=path+os.path.sep+i
location_of_working_local_folder=path
download(id_of_working_drive_folder,location_of_working_local_folder)
# subprocess.check_call(['explorer', path])
#call(["nautilus",path])
print("Type Sign Out for sign out and sync")
inp=input()
if inp=="Sign Out":
    print("Uploading")
    upload(path,id_of_working_drive_folder)
    print("Upload Complete")
    webbrowser.open('accounts.google.com/logout')