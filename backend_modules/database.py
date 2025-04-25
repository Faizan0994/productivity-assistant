import sqlite3

from win32api   import GetUserName
from pathlib    import PureWindowsPath
from os         import mkdir
from os.path    import expanduser, join, isdir
from .calc_time import to_utc
from datetime   import datetime, timedelta

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
# else:
#       rmtree (databasePath)
#       exit ("Removed file")

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

def cordinates (timerange: list, name: str = ""):
    """
    Returns a list of touples of time stamp displayed on x-axis 
    and the time spent in each duration
    """

    points = []
    
    if len(timerange) >= 3:
        timerange = [t.isoformat () for t in timerange]
        for startTime, endTime in zip (timerange[0:-1], timerange[1::]):
            intervals = interval_time (start = startTime, end = endTime, name = name)
            points.append ((endTime, intervals))
    else:
        class ArrayLength (Exception):
            def __init__(self, message):
                self.message = message
                super().__init__(message)
            def __str__(self):
                return self.message
        raise ArrayLength ("The length of list is too small")

    for entry in points:
        print (entry[0], entry[1].total_seconds ())


def interval_time (start: str = "", end: str = "", name: str = "") -> list:
    """
    Returns the time intervals between start and end
    if  empty  strings  are passed, it  returns  the 
    total  time  spent  the  name  will  filter  the 
    intervals by application.
    """

    executionTuple = execution (start, end)
    sql = executionTuple[0]
    parameters = executionTuple[1]
    del (executionTuple)
    
    if not name == "":
        sql =   f"SELECT * FROM ({sql})\
                WHERE name = ?"
        parameters.append (name)
    
    sql =   f"SELECT start, end FROM ({sql})"

    intervals = cursordb.execute (sql, parameters)
    start = datetime.fromisoformat (start)
    end = datetime.fromisoformat (end)
    timeSpent = timedelta (0)

    for interval in intervals:
        startOfInterval = datetime.fromisoformat (interval[0])
        endOfInterval = datetime.fromisoformat (interval[1])
        
        if startOfInterval < start and endOfInterval > end:
            timeSpent += end - start
        elif startOfInterval < start and endOfInterval > start:
            timeSpent += endOfInterval - start
        elif endOfInterval > end and startOfInterval < end:
            timeSpent += end - startOfInterval
        else:
            timeSpent += endOfInterval - startOfInterval
    
    return timeSpent

def programs_in_duration (start: str, end: str) -> list:
    """
    Returns list of programs that have been runed
    from start time to end time
    """

    executionTuple = execution (start, end)
    sql = executionTuple[0]
    paramaters = executionTuple[1]
    del (executionTuple)
    sql = f"SELECT DISTINCT (name) FROM ({sql})"
    programs = [app[0] for app in cursordb.execute (sql, paramaters)]
    return programs

def execution (start:str, end: str) -> tuple:
    """
    This is a common function that is used by programs 
    in  duration  and  interval  time.  This  function 
    converts  start and end  to utc format, hence  YOU 
    DONT NEED TO CONVERT WHERE IT IS CALLED.
    """

    start = to_utc (datetime.fromisoformat (start)).isoformat ()
    end = to_utc (datetime.fromisoformat (end)).isoformat ()

    sql =   "SELECT name, start, end FROM time_stamps\
            LEFT JOIN programs ON programs.id = time_stamps.program_id\
            WHERE end IS NOT NULL"
    parameters = []
    
    if not (start == "" and end == ""):
        sql =   f"SELECT * FROM ({sql})\
                WHERE DATETIME (start) > DATETIME (?)\
                OR (DATETIME (start) < ? AND DATETIME (end) > ?)"
        sql =   f"SELECT * FROM ({sql})\
                WHERE DATETIME (end) <= ?\
                OR (DATETIME (end) > ? AND DATETIME (start) < ?)"
        
        parameters.extend ([start, start, start, end, end, end])
    
    return (sql, parameters)

# temporary database, use it for debugging ...
# database = sqlite3.connect (PureWindowsPath ("test_data", "data.db"))
# cursordb = database.cursor ()