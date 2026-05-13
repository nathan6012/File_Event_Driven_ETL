from pathlib import Path
from datetime import datetime, timedelta
import os

# Folder to clean
pwd = Path(__file__).resolve().parent
root_dir = pwd.parent
STORAGE_FOLDER = root_dir/"storage"

# Delete files older than 5 days
DAYS_OLD = 5


def delete_old_files():
    now = datetime.now()
    cutoff_time = now - timedelta(days=DAYS_OLD)

    if not STORAGE_FOLDER.exists():
        print("Storage folder does not exist.")
        return

    deleted_count = 0

    for file in STORAGE_FOLDER.iterdir():

        # Skip folders
        if not file.is_file():
            continue

        # File last modified time
        file_modified_time = datetime.fromtimestamp(
            os.path.getmtime(file)
        )

        # Delete if older than cutoff
        if file_modified_time < cutoff_time:
            try:
                file.unlink()
                deleted_count += 1
                print(f"Deleted: {file.name}")

            except Exception as e:
                print(f"Error deleting {file.name}: {e}")

    print(f"\nCleanup finished. Deleted {deleted_count} files.")


