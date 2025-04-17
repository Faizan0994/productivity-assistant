import sqlite3

from win32api   import GetUserName
from pathlib    import PureWindowsPath
from os         import mkdir
from os.path    import expanduser, join, isdir
from .process   import program

# remove after completing ...
from shutil     import rmtree

def set_database (path, name):
    database = sqlite3.connect (join (path, name))
    dbcur = database.cursor ()
    dbcur.execute   ("""
                     CREATE TABLE programs 
                     (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                     name TEXT NOT NULL)
                     """)
    
    dbcur.execute   ("""
                     CREATE TABLE time 
                     (index INTEGER NOT NULL
                     program_id INTEGER NOT NULL,
                     start TEXT,
                     end TEXT,
                     FOREIGN KEY(group_id)
                        REFRENCE programs (id))
                     """)

# global variables
userName = GetUserName ()
databaseName = "data.db"
databasePath = join (expanduser ("~"), PureWindowsPath ("AppData", "Local", "Productivity Assistant"))
freshDownload = not isdir (databasePath)

if freshDownload:
        mkdir (databasePath)
        set_database (databasePath, databaseName)
        # run the introductory program ...

# remove it after making database ...
else:
      rmtree (databasePath)
      exit ("Removed file")

del (freshDownload)

database = sqlite3.connect (join (databasePath, databaseName))
cursordb = database.cursor ()

def add_program (programObj: program):
    cursordb.execute ("INSERT INTO programs VALUES (NULL, ?)", [programObj.name])   # inorder to auto increment use null
    database.commit ()

def in_program_list (program: str) -> bool:
    """
    Checks for the number of times the name appears 
    in  the programs and  return false if count  is
    zero
    """
    
    if [count[0] for count in cursordb.execute ("""
                                                SELECT COUNT (*) FROM 
                                                (SELECT name FROM programs WHERE name = ?)
                                                """, [program])] [0] == 0:
         return False
    else:
         return True