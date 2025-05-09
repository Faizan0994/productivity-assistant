# this file stores global paths used by
# database.py and settings.py

from pathlib    import PureWindowsPath
from os.path    import join, expanduser

path = join (expanduser ("~"), PureWindowsPath ("AppData", "Local", "Productivity Assistant"))
databasePath = PureWindowsPath (path, "data.db")
settingsPath = PureWindowsPath (path, "settings.json")