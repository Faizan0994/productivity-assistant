import sqlite3

from win32api   import GetUserName
from pathlib    import PureWindowsPath
from os         import access, listdir, mkdir
from os.path    import expanduser, join, isdir

def setDatabase ():
    database = sqlite3.connect (join (databasePath, databaseName))
    dbcur = database.cursor ()
    dbcur.execute ("CREATE TABLE programs (ID int, name VARCHAR (255), PRIMARY KEY (ID))")
    tables = dbcur.execute ("SELECT name FROM sqlite_master")
    print (dbcur.fetchall ())

# global variables
userName = GetUserName()
# use this later ...
# databasePath = join (expanduser ("~"), PureWindowsPath ("AppData", "Local", "Productivity Assistant"))

databaseName = "datalake.db"
databasePath = join (expanduser ("~"), PureWindowsPath ("Documents", "productivity-assistant", "database"))
freshDownload = not isdir (databasePath)

if freshDownload:
        mkdir (databasePath)
        setDatabase ()
        # run the introductory program ...
del (freshDownload)

database = sqlite3.connect (join (databasePath, databaseName))