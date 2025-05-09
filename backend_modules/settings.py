import json
from datetime   import time
from .link      import settingsPath

default_settings = {
            "theme": "dark",
            "notifications": True,
            "reminders": True,
            "daily_report": True,
            "day_start": time (hour = 0, minute = 0, second = 0).isoformat ()
            }

def load_settings (file_path = settingsPath) -> dict:
    with open (file_path, 'r') as file:
        settings = json.load (file)
    return settings

def save_settings (settings, file_path = settingsPath) -> None:
    with open (file_path, 'w') as file:
        json.dump (settings, file, indent = 4)
            
def update_settings (key: str, value, file_path = settingsPath) -> None:
    settings = load_settings (file_path)
    settings[key] = value
    save_settings (file_path, settings)

def get_settings (key: str, file_path = settingsPath) -> any:
    settings = load_settings (file_path)
    return settings[key] if key in settings else None