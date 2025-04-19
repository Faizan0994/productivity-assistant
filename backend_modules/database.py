import sqlite3

from win32api   import GetUserName
from pathlib    import PureWindowsPath
from os         import mkdir
from os.path    import expanduser, join, isdir
from datetime   import datetime, time, date

# remove after completing ...
from shutil     import rmtree

# sets indexes and creates tables in the database
def set_database (path, name):
    database = sqlite3.connect (join (path, name))
    dbcur = database.cursor ()
    dbcur.executescript     ("""
                            BEGIN;
                            CREATE TABLE programs 
                            (id INTEGER PRIMARY KEY AUTOINCREMENT,
                            name TEXT NOT NULL);
                             
                            CREATE TABLE time_stamps 
                            (id INTEGER PRIMARY KEY AUTOINCREMENT,
                            program_id INTEGER NOT NULL,
                            start TEXT,
                            end TEXT,
                            FOREIGN KEY (program_id) REFERENCES programs (id));
                             
                            CREATE UNIQUE INDEX program_name ON programs (name);
                            
                            COMMIT;
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

def add_program (name: str):
    # inorder to auto increment use null
    cursordb.execute    ("""
                         INSERT INTO programs VALUES (NULL, ?)
                         """, [name])
    database.commit ()

# returns the process id in *our* database
def pid (name: str) -> int:
     return [entery[0] for entery in cursordb.execute   ("""
                                                         SELECT id FROM programs WHERE name = ?
                                                         """, [name])] [0]

def add_current (pid: int, sartTime: str) -> int:
    cursordb.execute    ("""
                        INSERT INTO time_stamps (program_id, start)
                         VALUES (?, ?)
                        """, [pid, sartTime])
    database.commit ()
    entry_id = [entery[0] for entery in cursordb.execute    ("""
                                                            SELECT * FROM time_stamps 
                                                            ORDER BY id DESC
                                                            """)] [0]
    return entry_id

def update_endtime (index: int, endTime: str) -> int:
    cursordb.execute    ("""
                         UPDATE time_stamps SET end = ? WHERE id = ?
                         """, [endTime, index])
    database.commit ()

    # uncomment it to display results...
    # for i in cursordb.execute ("SELECT * FROM time_stamps WHERE id = ?", [index]):
    #       print (i)

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

def total_time (name: str, start = None, end = None):
    totalTimeSql = \
"\
SELECT name, DATETIME (start), DATETIME (end) FROM time_stamps \
LEFT JOIN programs on programs.id = time_stamps.program_id \
WHERE name = ? \
AND end IS NOT NULL \
"    
    parameters = [name]


    if isinstance(start, date) and isinstance (end, date):
        totalTimeSQL += \
"\
AND DATE (start) =< ? AND DATE (end) >= ? \
"
        start = start.strftime("%Y-%m-%d")
        end = end.strftime("%Y-%m-%d")
        
        parameters.extend (start, end)

    totalTime = cursordb.execute (totalTimeSql, parameters)
    
    for entry in totalTime:
        print (entry)
    # print (totalTimeSql)