#!/usr/bin/env python3
"""
Upload local project files to Google Drive.

Uploads docs/, results/, member_results/, resources/, GEMINI.md, README.md
to the shared Google Drive folder, mirroring the local directory structure.

Usage:
    python3 scripts/upload_to_drive.py [--dry-run]
    
Environment:
    GOOGLE_DRIVE_FOLDER_ID  — Target Drive folder ID (default: 1FHh4VKxjO2zJF6Bx42UZgxv80cmpsEdG)
    
Requirements:
    pip install google-api-python-client google-auth-oauthlib
"""

import os
import sys
import argparse
import mimetypes
from pathlib import Path

try:
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from google.auth.transport.requests import Request
    from googleapiclient.discovery import build
    from googleapiclient.http import MediaFileUpload
except ImportError:
    print("Error: Required packages not installed.")
    print("Run: pip install google-api-python-client google-auth-oauthlib")
    sys.exit(1)

# --- Configuration ---
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_FOLDER_ID = "1FHh4VKxjO2zJF6Bx42UZgxv80cmpsEdG"
SCOPES = ["https://www.googleapis.com/auth/drive"]
TOKEN_PATH = PROJECT_ROOT / ".gdrive-token.json"
CREDENTIALS_PATH = PROJECT_ROOT / "credentials.json"

# What to upload
UPLOAD_DIRS = ["docs", "results", "member_results", "resources"]
UPLOAD_FILES = ["GEMINI.md", "README.md"]

# Skip patterns
SKIP_PATTERNS = {
    "__pycache__", ".git", ".env", ".DS_Store", ".gdrive-token.json",
    "credentials.json", "node_modules", ".agents", ".gemini",
}
SKIP_EXTENSIONS = {".pyc", ".pyo"}


def authenticate():
    """Authenticate with Google Drive API."""
    creds = None
    
    if TOKEN_PATH.exists():
        creds = Credentials.from_authorized_user_file(str(TOKEN_PATH), SCOPES)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not CREDENTIALS_PATH.exists():
                print(f"Error: {CREDENTIALS_PATH} not found.")
                print("Download OAuth credentials from Google Cloud Console.")
                print("See: https://console.cloud.google.com/apis/credentials")
                sys.exit(1)
            flow = InstalledAppFlow.from_client_secrets_file(str(CREDENTIALS_PATH), SCOPES)
            creds = flow.run_local_server(port=0)
        
        TOKEN_PATH.write_text(creds.to_json())
    
    return build("drive", "v3", credentials=creds)


def find_or_create_folder(service, name, parent_id):
    """Find existing folder by name in parent, or create it."""
    query = (
        f"name='{name}' and '{parent_id}' in parents "
        f"and mimeType='application/vnd.google-apps.folder' and trashed=false"
    )
    results = service.files().list(q=query, fields="files(id, name)").execute()
    files = results.get("files", [])
    
    if files:
        return files[0]["id"]
    
    # Create folder
    metadata = {
        "name": name,
        "mimeType": "application/vnd.google-apps.folder",
        "parents": [parent_id],
    }
    folder = service.files().create(body=metadata, fields="id").execute()
    return folder["id"]


def find_existing_file(service, name, parent_id):
    """Find existing file by name in parent folder."""
    query = (
        f"name='{name}' and '{parent_id}' in parents "
        f"and mimeType!='application/vnd.google-apps.folder' and trashed=false"
    )
    results = service.files().list(q=query, fields="files(id, name)").execute()
    files = results.get("files", [])
    return files[0]["id"] if files else None


def should_skip(path):
    """Check if path should be skipped."""
    name = path.name
    if name.startswith("."):
        return True
    if name in SKIP_PATTERNS:
        return True
    if path.suffix in SKIP_EXTENSIONS:
        return True
    return False


def upload_file(service, local_path, parent_id, dry_run=False):
    """Upload or update a single file."""
    name = local_path.name
    mime_type = mimetypes.guess_type(str(local_path))[0] or "application/octet-stream"
    
    existing_id = find_existing_file(service, name, parent_id)
    
    if dry_run:
        action = "UPDATE" if existing_id else "CREATE"
        print(f"  [{action}] {local_path.relative_to(PROJECT_ROOT)} ({mime_type})")
        return action
    
    media = MediaFileUpload(str(local_path), mimetype=mime_type, resumable=True)
    
    if existing_id:
        # Update existing file
        service.files().update(
            fileId=existing_id,
            media_body=media,
        ).execute()
        print(f"  [UPDATED] {local_path.relative_to(PROJECT_ROOT)}")
        return "UPDATE"
    else:
        # Create new file
        metadata = {"name": name, "parents": [parent_id]}
        service.files().create(
            body=metadata,
            media_body=media,
            fields="id",
        ).execute()
        print(f"  [CREATED] {local_path.relative_to(PROJECT_ROOT)}")
        return "CREATE"


def upload_directory(service, local_dir, parent_id, dry_run=False, stats=None):
    """Recursively upload a directory."""
    if stats is None:
        stats = {"created": 0, "updated": 0, "skipped": 0, "folders": 0}
    
    local_path = Path(local_dir)
    
    for item in sorted(local_path.iterdir()):
        if should_skip(item):
            stats["skipped"] += 1
            continue
        
        if item.is_dir():
            folder_id = find_or_create_folder(service, item.name, parent_id)
            stats["folders"] += 1
            if not dry_run:
                print(f"  [FOLDER] {item.relative_to(PROJECT_ROOT)}/")
            else:
                print(f"  [FOLDER] {item.relative_to(PROJECT_ROOT)}/")
            upload_directory(service, item, folder_id, dry_run, stats)
        elif item.is_file():
            try:
                action = upload_file(service, item, parent_id, dry_run)
                if action == "CREATE":
                    stats["created"] += 1
                else:
                    stats["updated"] += 1
            except Exception as e:
                print(f"  [ERROR] {item.relative_to(PROJECT_ROOT)}: {e}")
                stats["skipped"] += 1
    
    return stats


def main():
    parser = argparse.ArgumentParser(description="Upload project files to Google Drive")
    parser.add_argument("--dry-run", action="store_true", help="Preview without uploading")
    parser.add_argument("--folder-id", default=None, help="Target Drive folder ID")
    args = parser.parse_args()
    
    folder_id = args.folder_id or os.environ.get("GOOGLE_DRIVE_FOLDER_ID", DEFAULT_FOLDER_ID)
    
    print("=" * 50)
    print("☁️  Google Drive Upload")
    print("=" * 50)
    print(f"Target folder: {folder_id}")
    print(f"Project root:  {PROJECT_ROOT}")
    if args.dry_run:
        print(">> DRY RUN MODE <<")
    print()
    
    service = authenticate()
    
    total_stats = {"created": 0, "updated": 0, "skipped": 0, "folders": 0}
    
    # Upload directories
    for dir_name in UPLOAD_DIRS:
        dir_path = PROJECT_ROOT / dir_name
        if not dir_path.exists():
            print(f"⚠️  {dir_name}/ not found, skipping")
            continue
        
        print(f"\n📂 {dir_name}/")
        drive_folder_id = find_or_create_folder(service, dir_name, folder_id)
        total_stats["folders"] += 1
        stats = upload_directory(service, dir_path, drive_folder_id, args.dry_run)
        for k in total_stats:
            total_stats[k] += stats.get(k, 0)
    
    # Upload root files
    print(f"\n📄 Root files")
    for file_name in UPLOAD_FILES:
        file_path = PROJECT_ROOT / file_name
        if not file_path.exists():
            print(f"  ⚠️  {file_name} not found, skipping")
            continue
        try:
            action = upload_file(service, file_path, folder_id, args.dry_run)
            if action == "CREATE":
                total_stats["created"] += 1
            else:
                total_stats["updated"] += 1
        except Exception as e:
            print(f"  [ERROR] {file_name}: {e}")
    
    # Summary
    print(f"\n{'=' * 50}")
    print(f"✅ Upload Complete!")
    print(f"   📁 Folders: {total_stats['folders']}")
    print(f"   🆕 Created: {total_stats['created']}")
    print(f"   🔄 Updated: {total_stats['updated']}")
    print(f"   ⏭️  Skipped: {total_stats['skipped']}")
    print(f"{'=' * 50}")
    print(f"\n🔗 https://drive.google.com/drive/folders/{folder_id}")


if __name__ == "__main__":
    main()
