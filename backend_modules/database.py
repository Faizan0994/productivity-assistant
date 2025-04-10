from win32api   import GetUserName
from pathlib    import PureWindowsPath
from os         import access, listdir, mkdir
from os.path    import expanduser, join, isdir
import os

# global variables
userName = GetUserName()

databasePath = join (expanduser ("~"), PureWindowsPath ("AppData", "Local", "Productivity Assistant"))
freshDownload = not isdir (databasePath)
if freshDownload:
        mkdir (databasePath)
        # run the introductory program...
del (freshDownload)