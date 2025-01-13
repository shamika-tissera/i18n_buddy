import os
import shutil

def create_backup(source_dir: str, dest_dir: str):
    # Create a backup of the source directory
    if os.path.exists(dest_dir):
        shutil.rmtree(dest_dir)
    shutil.copytree(source_dir, dest_dir)

def delete_backup(dest_dir: str):
    # Delete the backup directory
    if os.path.exists(dest_dir):
        shutil.rmtree(dest_dir)
    
