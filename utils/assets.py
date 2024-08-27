import json
import time
import os

def save_json_file(filename, data):
    """
    Save data to a JSON file.
    :param filename: The name of the file.
    :param data: The data to save.
    """
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def sleep(seconds=1):
    """
    Pause execution for a specified number of seconds.
    :param seconds: Number of seconds to sleep.
    """
    time.sleep(seconds)

def fix_name_for_folder(name):
    # Sanitize folder names
    return name.replace('/', '_').replace('\\', '_')

def create_folder(folder_name):
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
