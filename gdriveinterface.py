from __future__ import print_function
import httplib2
import os
import io

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
from googleapiclient.http import MediaIoBaseDownload

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/drive-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/drive.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Drive API Python Quickstart'


def get_credentials():
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'drive-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def main():
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('drive', 'v3', http=http)

    results = service.files().list(
        fields='nextPageToken, files(id, name, parents)',
        q="'0B8-YwIvbRgEFYV9LTzJ1UDhXalk' in parents"
        ).execute()
    items = results['files']
    if not items:
        print('No files found.')
    else:
        print('Files:')
        for item in items:
            try:
                print('{0} ({1}) {2}'.format(item['name'], item['id'], item['parents']))
            except:
                print('{0} ({1})'.format(item['name'], item['id']))

def grab_soc_files():
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('drive', 'v3', http=http)

    soc_folder_id = service.files().list(
        fields='files(id)',
        q="name='SOC'").execute()['files'][0]['id']

    soc_files_json = service.files().list(
        fields='files(name, id, mimeType)',
        q="'{0}' in parents".format(soc_folder_id)).execute()['files']
    return soc_files_json

def download_plaintext(f_id):
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('drive', 'v3', http=http)

    request = service.files().export_media(fileId=f_id, mimeType='text/plain')
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
    text = fh.getvalue()[1:]
    fh.close()
    return text

if __name__ == '__main__':
    files = grab_soc_files()
    ids = [f['id'] for f in files]
    print(download_plaintext(ids[0]))
