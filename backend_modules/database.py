from win32api   import GetUserName
from pathlib    import PureWindowsPath

userName = GetUserName()
databasePath = PureWindowsPath ("c:/", "User", userName, "AppData")