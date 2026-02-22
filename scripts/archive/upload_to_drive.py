import os
import argparse
import pickle
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.http import MediaFileUpload

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/drive.file']

def get_service():
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists('credentials.json'):
                print("Error: credentials.json not found. Please download OAuth 2.0 Client IDs json from Google Cloud Console.")
                return None
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('drive', 'v3', credentials=creds)
    return service

def create_folder(service, name, parent_id=None):
    file_metadata = {
        'name': name,
        'mimeType': 'application/vnd.google-apps.folder'
    }
    if parent_id:
        file_metadata['parents'] = [parent_id]
        
    # Check if folder exists first
    query = f"mimeType='application/vnd.google-apps.folder' and name='{name}' and trashed=false"
    if parent_id:
        query += f" and '{parent_id}' in parents"
        
    results = service.files().list(q=query, spaces='drive', fields='files(id, name)').execute()
    items = results.get('files', [])
    
    if items:
        # Return existing folder ID
        return items[0]['id']
    else:
        file = service.files().create(body=file_metadata, fields='id').execute()
        return file.get('id')

def upload_file(service, filename, filepath, parent_id=None):
    file_metadata = {'name': filename}
    if parent_id:
        file_metadata['parents'] = [parent_id]
        
    media = MediaFileUpload(filepath, resumable=True)
    
    # Check if file exists (basic check by name)
    query = f"name='{filename}' and trashed=false"
    if parent_id:
        query += f" and '{parent_id}' in parents"
    
    results = service.files().list(q=query, spaces='drive', fields='files(id, name)').execute()
    items = results.get('files', [])
    
    if items:
        print(f"  Skipping {filename} (already exists)")
        return items[0]['id']
    
    file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    print(f"  Uploaded {filename}")
    return file.get('id')

def recursive_upload(service, local_path, parent_drive_id):
    if os.path.isfile(local_path):
        filename = os.path.basename(local_path)
        upload_file(service, filename, local_path, parent_drive_id)
        return

    # If directory, iterate
    if os.path.isdir(local_path):
        # Create corresponding folder in Drive (except if it's the root we pass)
        # Actually logic:
        # We start at member_results, target is 1FHh...
        # We want everything INSIDE member_results to go INTO 1FHh...
        # So we iterate contents of local_path.
        
        for item in os.listdir(local_path):
            if item.startswith('.') or item == "__pycache__": continue
            
            item_path = os.path.join(local_path, item)
            
            if os.path.isdir(item_path):
                # Create subfolder
                print(f"Enter folder: {item}")
                sub_folder_id = create_folder(service, item, parent_drive_id)
                recursive_upload(service, item_path, sub_folder_id)
            else:
                # Upload file
                upload_file(service, item, item_path, parent_drive_id)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Upload folder to Google Drive.")
    parser.add_argument("--source", default="member_results", help="Local folder to upload")
    # Default target ID provided by user
    parser.add_argument("--target-id", default="1FHh4VKxjO2zJF6Bx42UZgxv80cmpsEdG", help="Target Google Drive Folder ID")
    
    args = parser.parse_args()
    
    if not os.path.exists(args.source):
        print(f"Error: Source '{args.source}' does not exist.")
        exit(1)
        
    service = get_service()
    if service:
        print(f"Starting upload from '{args.source}' to Drive Folder ID '{args.target_id}'...")
        recursive_upload(service, args.source, args.target_id)
        print("Upload complete.")
