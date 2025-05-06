import json
from datetime   import time
from pathlib    import PureWindowsPath

default_settings = {
            "theme": "dark",
            "notifications": True,
            "reminders": True,
            "daily_report": True,
            "day_start": time (hour = 0, minute = 0, second = 0).isoformat ()
            }

path = PureWindowsPath (".")

def load_settings (file_path = path) -> dict:
    with open (file_path, 'r') as file:
        settings = json.load (file)
    return settings

def save_settings (settings, file_path = path) -> None:
    with open (file_path, 'w') as file:
        json.dump (settings, file, indent = 4)
            
def update_settings (key: str, value, file_path = path) -> None:
    settings = load_settings (file_path)
    settings[key] = value
    save_settings (file_path, settings)

def get_settings (key: str, file_path = path) -> any:
    settings = load_settings (file_path)
    return settings[key] if key in settings else None