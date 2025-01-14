import os
from constants.log_levels import LogLevel
from interactor import log_in_console
import ujson # ujson is said to be more performant than the builtin library, hence using it
import sys

def fetch_source_files(file_path: str) -> list[dict]:
    """Fetch the source file content.
    """
    files_in_json = []
    for file in os.listdir(file_path):
        if file.endswith('.json'):
            with open(os.path.join(file_path, file), 'r', encoding='utf-8') as f:
                file_content = ujson.load(f)
                files_in_json.append({
                    'file_name': file,
                    'content': file_content
                })
                
    return files_in_json

def fetch_target_files(file_path: str) -> list[dict]:
    """Fetch the target file content.
    """
    files_in_json = []
    for file in os.listdir(file_path):
        if file.endswith('.json'):
            with open(os.path.join(file_path, file), 'r', encoding='utf-8') as f:
                content = f.read().strip()
                if content:
                    try:
                        file_content = ujson.loads(content)
                    except ujson.JSONDecodeError:
                        log_in_console(f"File {file} in {file_path} is not a valid JSON file. Exiting the program.", LogLevel.CRITICAL)
                        sys.exit()
                    files_in_json.append({
                        'file_name': file,
                        'content': file_content
                    })
                else:
                    files_in_json.append({
                        'file_name': file,
                        'content': {}
                    })
                
    return files_in_json

def fetch_file_content(file_path: str) -> dict:
    """Fetch the content of the file.
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read().strip()
        if content:
            file_content = ujson.loads(content)
        else:
            file_content = {}
    return file_content

def write_to_file(file_path: str, content: dict, ensure_ascii: bool = True):
    """Write the content to the file.
    """
    with open(file_path, 'w', encoding='utf-8') as f:
        ujson.dump(content, f, indent=4, ensure_ascii=ensure_ascii)
