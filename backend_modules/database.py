import sqlite3

from win32api   import GetUserName
from pathlib    import PureWindowsPath
from os         import access, listdir, mkdir
from os.path    import expanduser, join, isdir
from .process   import program

# remove after completing ...
from shutil     import rmtree

def setDatabase (path, name):
    database = sqlite3.connect (join (path, name))
    dbcur = database.cursor ()
    dbcur.execute ("CREATE TABLE programs (id INTEGER PRIMARY KEY AUTOINCREMENT, name VARCHAR (255))")

# global variables
userName = GetUserName()
databaseName = "data.db"
databasePath = join (expanduser ("~"), PureWindowsPath ("AppData", "Local", "Productivity Assistant"))
freshDownload = not isdir (databasePath)

if freshDownload:
        mkdir (databasePath)
        setDatabase (databasePath, databaseName)
        # run the introductory program ...

# remove it after making database ...
else:
      rmtree (databasePath)
      exit ("Removed file")

del (freshDownload)

database = sqlite3.connect (join (databasePath, databaseName))
# tablesdb = cursordb.execute ("SELECT name FROM sqlite_master")
# programsdb = cursordb.execute ("SELECT name FROM sqlite_master WHERE name = 'progams'")

def addProgram (database: sqlite3.Connection, programObj: program):
    cursordb = database.cursor ()
    cursordb.execute ("INSERT INTO programs VALUES (NULL, ?)", [programObj.name])   # inorder to auto increment use null
    database.commit ()
    # to check ...
    # print (cursordb.execute ("SELECT * FROM programs").fetchall ())

# for emergency situations ...
# databasePath = join (expanduser ("~"), PureWindowsPath ("Documents", "productivity-assistant", "database"))