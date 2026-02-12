# JSON save/load utilities

import json
import os

# Saves analysis results to a JSON file.
def save_results(results, file_path):
    folder = os.path.dirname(file_path)
    if folder:
        os.makedirs(folder, exist_ok=True)

    try:
        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(results, file, indent=4)
        return True
    except Exception as e:
        print(f"Error saving file: {e}")
        return False

# Loads data from a JSON file.
def load_json(file_path, default=None):
    if not os.path.exists(file_path):
        return default if default is not None else {}

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)
    except json.JSONDecodeError:
        print(f"Error: {file_path} contains invalid JSON.")
        return default if default is not None else {}