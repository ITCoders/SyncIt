import os
import webbrowser
# from subprocess import call

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

HOME_DIRECTORY = 'G:'
ROOT_FOLDER_NAME = 'SyncIt'

browsed = []
done_paths = []


def login():
    """ function for login """
    g_auth = GoogleAuth()
    g_auth.LocalWebserverAuth()
    g_auth.Authorize()
    g_drive = GoogleDrive(g_auth)
    return g_drive


def id_of_title(title, parent_directory_id):
    """ function of getting id of a given filename """
    foldered_list = drive.ListFile({
        'q': "'{}' in parents and trashed=false".format(parent_directory_id)
    }).GetList()
    for file in foldered_list:
        if file['title'] == title:
            return file['id']
    return None


def create_folder(folder_id, subfolder):
    new_folder = drive.CreateFile({
        'title': subfolder,
        'parents': [{'kind': 'drive#fileLink', 'id': folder_id}],
        'mimeType': 'application/vnd.google-apps.folder'
    })
    new_folder.Upload()
    return new_folder


def download(folder_id, destination_location):
    """ function of downloading a specific folder from drive to local """
    if not os.path.exists(destination_location):
        os.makedirs(destination_location)
    foldered_list = drive.ListFile({
        'q': "'{}' in parents and trashed=false".format(folder_id)
    }).GetList()
    for item in foldered_list:
        item_path = os.path.join(destination_location, item['title'])
        if item['mimeType'] == 'application/vnd.google-apps.folder':
            download(item['id'], item_path)
        # print('title: {}, id: {}'.format(item['title'], item['size']))
        else:
            open(item_path, 'w+')  # <-- what does this line do?
            local_size = os.path.getsize(item_path)
            drive_size = item['fileSize']
            if local_size != drive_size:
                file = drive.CreateFile({'id': item['id']})
                file.GetContentFile(item_path)


def upload(source_location, folder_id):
    """ function for uploading source location to designated id """
    for folder_name, subfolders, filenames in os.walk(source_location):
        if folder_name not in done_paths:
            if filenames:
                for filename in filenames:
                    file_id = id_of_title(filename, folder_id)
                    file_path = os.path.join(folder_name, filename)
                    if file_id is not None:
                        file_drive = drive.CreateFile({'id': file_id})
                        drive_file_size = file_drive['fileSize']
                        local_file_size = os.path.getsize(file_path)
                        if drive_file_size != str(local_file_size):
                            file_drive.SetContentFile(file_path)
                            file_drive.Upload()
                            # else:
                            #     #blank
                    else:
                        new_file = drive.CreateFile({
                            'title': filename,
                            'parents': [{
                                'kind': 'drive#fileLink',
                                'id': folder_id
                            }]
                        })
                        new_file.SetContentFile(file_path)
                        new_file.Upload()
            if subfolders:
                for subfolder in subfolders:
                    subfolder_id = id_of_title(subfolder, folder_id)
                    if subfolder_id is None:
                        new_sub_folder = create_folder(folder_id, subfolder)
                        subfolder_id = new_sub_folder['id']
                    abs_path = os.path.join(folder_name, subfolder)
                    upload(abs_path, subfolder_id)
                    done_paths.append(abs_path)


def upload_folder(source_location, parent_id):
    """ function for creating a folder and upload into that """
    folder_name = os.path.split(source_location)[1]
    id_of_folder = id_of_title(folder_name, parent_id)
    if id_of_folder is None:
        new_folder = drive.CreateFile({
            'title': folder_name,
            'parents': [{'kind': 'drive#fileLink', 'id': parent_id}],
            'mimeType': 'application/vnd.google-apps.folder'
        })
        new_folder.Upload()
        id_of_folder = new_folder['id']
    upload(source_location, id_of_folder)


def list_folder(parent):
    """ function for returning file tree structure from parentid """
    filelist = []
    file_list = drive.ListFile(
        {'q': "'%s' in parents and trashed=false" % parent}).GetList()
    for f in file_list:
        if f['mimeType'] == 'application/vnd.google-apps.folder':  # if folder
            filelist.append({
                'id': f['id'],
                'title': f['title'],
                'list': list_folder(f['id'])
            })
        else:
            filelist.append(f['title'])
    return filelist


def get_username(drive_object):
    """ function to get the current user's name and email address """
    user_info = drive_object.GetAbout()['user']
    print('Logged in as: {displayName} ({emailAddress})\n'.format(**user_info))
    return user_info['displayName']


def folder_browser(folder_structure, folder_id):
    """ function for browsing into drive directory """
    if not folder_structure:
        print('└── >>> Empty Folder <<<')
    else:
        total_items = len(folder_structure)
        for dex, item in enumerate(folder_structure, 1):
            print('{} {}'.format(
                '└──' if dex == total_items else '├──',
                item['title'] if isinstance(item, dict) else item))

    folder_name = input("\nEnter Name of Folder You Want to Use\n"
                        "Enter '/' to use current folder\n"
                        "Enter ':' to create New Folder and use that\n")
    if folder_name == '/':
        return folder_id
    elif folder_name == ':':
        new_folder_name = input('Enter Name of Folder You Want to Create\n')
        new_folder = create_folder(folder_id, new_folder_name)
        folder_path = os.path.join(HOME_DIRECTORY, ROOT_FOLDER_NAME, USERNAME)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        return new_folder['id']
    else:
        folder_selected = folder_name
        for element in folder_structure:
            if isinstance(element, dict) \
                    and element['title'] == folder_selected:
                struc = element['list']
                browsed.append(folder_selected)
                print('\n{}'.format(folder_selected))
                return folder_browser(struc, element['id'])


if __name__ == '__main__':
    drive = login()
    print('Complete Authentication Flow First\n')

    USERNAME = get_username(drive)

    root_id = id_of_title(ROOT_FOLDER_NAME, 'root')
    if root_id is None:
        root_id = create_folder('root', ROOT_FOLDER_NAME)['id']

    structure = list_folder(root_id)
    print('Your Existing File Directory')
    id_of_working_drive_folder = folder_browser(structure, root_id)

    path = os.path.join(HOME_DIRECTORY, ROOT_FOLDER_NAME, USERNAME)
    for i in browsed:
        path = os.path.join(path, i)
    location_of_working_local_folder = path
    download(id_of_working_drive_folder, location_of_working_local_folder)
    # subprocess.check_call(['explorer', path])
    # call(['nautilus',path])

    sign_out = input('\nType Sign Out for sign out and sync\n')
    if sign_out == 'Sign Out':
        print('Uploading')
        upload(path, id_of_working_drive_folder)
        print('Upload Complete')
        webbrowser.open('accounts.google.com/logout')
