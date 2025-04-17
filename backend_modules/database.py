import sqlite3

from win32api   import GetUserName
from pathlib    import PureWindowsPath
from os         import mkdir
from os.path    import expanduser, join, isdir
from importlib  import import_module


# remove after completing ...
from shutil     import rmtree

def set_database (path, name):
    database = sqlite3.connect (join (path, name))
    dbcur = database.cursor ()
    dbcur.execute   ("""
                     CREATE TABLE programs 
                     (id INTEGER PRIMARY KEY AUTOINCREMENT,
                     name TEXT NOT NULL)
                     """)
    
    dbcur.execute   ("""
                     CREATE TABLE time_stamps 
                     (id INTEGER PRIMARY KEY AUTOINCREMENT,
                     program_id INTEGER NOT NULL,
                     start TEXT,
                     end TEXT,
                     FOREIGN KEY (program_id) REFERENCES programs (id))
                     """)
    
    dbcur.execute   ("""
                     CREATE INDEX program_name ON programs (name)
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

process = import_module ("backend_modules.process")

def add_program (name: str):
     # inorder to auto increment use null
    cursordb.execute    ("""
                         INSERT INTO programs VALUES (NULL, ?)
                         """, [name])
    database.commit ()

def pid (name: str):
     """
     returns the process id in *our* database
     """
     return [entery[0] for entery in cursordb.execute   ("""
                                                         SELECT id FROM programs WHERE name = ?
                                                         """, [name])] [0]

def in_program_list (name: str) -> bool:
    """
    Checks for the number of times the name appears 
    in  the programs and  return false if count  is
    zero
    """
    
    if [count[0] for count in cursordb.execute ("""
                                                SELECT COUNT (*) FROM 
                                                (SELECT name FROM programs WHERE name = ?)
                                                """, [name])] [0] == 0:
         return False
    else:
         return True