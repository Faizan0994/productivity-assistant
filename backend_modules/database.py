import sqlite3

from os         import mkdir
from os.path    import isdir
from .calc_time import to_utc, datetime, timedelta
from .settings  import default_settings
from .settings  import save_settings as set_default_settings
from .link      import path, databasePath, settingsPath

# remove after completing ...
from shutil     import rmtree

# errors
class NoRecordFound (Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(message)
    def __str__(self):
        return self.message

# sets indexes and creates tables in the database
def set_database (databasePath, settingsPath):
    database = sqlite3.connect (databasePath)
    dbcur = database.cursor ()
    dbcur.executescript ("""
                         BEGIN;
                         
                         CREATE TABLE programs 
                         (id INTEGER PRIMARY KEY,
                         name TEXT NOT NULL); 
                         
                         CREATE TABLE time_stamps 
                         (id INTEGER PRIMARY KEY,   
                         program_id INTEGER NOT NULL,
                         start TEXT,
                         end TEXT,
                         FOREIGN KEY (program_id) REFERENCES programs (id)); 
                         
                         CREATE TABLE daily_limits
                         (limits_id INTIGER NOT NULL,
                         limits INTIGER NOT NULL,
                         FOREIGN KEY (limits_id) REFERENCES programs (id)); 
                         
                         CREATE UNIQUE INDEX program_name 
                         ON programs (name); 
                         
                         COMMIT;""")
    
    set_default_settings (file_path = settingsPath, settings = default_settings)
    settingPath = settingsPath

freshDownload = not isdir (path)

if freshDownload:
        mkdir (path)
        set_database (databasePath, settingsPath)
        # run the introductory program ...

# remove it after making database ...
# else:
#       rmtree (path)
#       exit ("Removed file")

del (freshDownload)

database = sqlite3.connect (databasePath)
cursordb = database.cursor ()

def add_program (name: str):
    # inorder to auto increment use null
    cursordb.execute ("""
                      INSERT INTO programs (name)
                      VALUES (?)
                      """, [name])
    database.commit ()

def pid (name: str) -> int:
    # returns the process id in *our* database
    try:
        return [entery[0] for entery in cursordb.execute ("""
                                                          SELECT id FROM programs 
                                                          WHERE name = ?
                                                          """, [name])] [0]
    except IndexError:
        class ProgramNotFound (Exception):
            def __init__(self, message):
                self.message = message
                super().__init__(message)
            def __str__ (self):
                return self.message
        raise ProgramNotFound (f"Application not in database: {name}")

def add_current (pid: int, sartTime: str) -> int:
    # Adds program and time tracked. It returns its id
    cursordb.execute ("""
                      INSERT INTO time_stamps 
                      (program_id, start) VALUES (?, ?)
                      """, [pid, sartTime])
    database.commit ()
    return [entery[0] for entery in cursordb.execute ("""
                                                      SELECT * FROM time_stamps 
                                                      ORDER BY id DESC
                                                      """)] [0]

def update_endtime (index: int, endTime: str) -> int:
    # Updates the end time of program
    cursordb.execute ("""
                      UPDATE time_stamps 
                      SET end = ? WHERE id = ?
                      """, [endTime, index])
    database.commit ()

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

def cordinates (timerange: list, name: str = "") -> list:
    """
    Returns a list of touples of time stamp displayed on x-axis 
    and the time spent in each duration
    """

    points = []
    
    if len(timerange) >= 3:
        for startTime, endTime in zip (timerange[0:-1], timerange[1::]):
            intervals = time_spent (start = startTime.isoformat (), end = endTime.isoformat (), name = name)
            points.append ((startTime, intervals))
    else:
        class ArrayLength (Exception):
            def __init__ (self, message):
                self.message = message
                super().__init__ (message)
            def __str__ (self):
                return self.message
        raise ArrayLength ("The length of list is too small")

    return points

def time_spent (start: str = "", end: str = "", name: str = "") -> timedelta:
    """
    Returns the time intervals between start and end
    if  empty  strings  are passed, it  returns  the 
    total  time  spent  the  name  will  filter  the 
    intervals by application.  Returns timedelta (0)
    when none is given.
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
    timeSpent = timedelta (0)
    
    # which would be more optimal?
    if not (start == "" and end == ""):
        start = to_utc (datetime.fromisoformat (start))
        end = to_utc (datetime.fromisoformat (end))

        for interval in intervals:
            startOfInterval = datetime.fromisoformat (interval[0])
            endOfInterval = datetime.fromisoformat (interval[1])

            if startOfInterval < start and endOfInterval > end:
                timeSpent += end - start
            elif startOfInterval <= start and endOfInterval > start:
                timeSpent += endOfInterval - start
            elif endOfInterval >= end and startOfInterval < end:
                timeSpent += end - startOfInterval
            else:
                timeSpent += endOfInterval - startOfInterval
    else:
        for interval in intervals:
            startOfInterval = datetime.fromisoformat (interval[0])
            endOfInterval = datetime.fromisoformat (interval[1])
            
            timeSpent += endOfInterval - startOfInterval
    
    return timeSpent

def programs_in_duration (start: str = "", end: str = "") -> list:
    """
    Returns list of programs that have been runed
    from start time to end time. Returns an empty
    list if there is no program.
    """

    executionTuple = execution (start, end)
    sql = executionTuple[0]
    paramaters = executionTuple[1]
    del (executionTuple)

    sql = f"SELECT DISTINCT (name) FROM ({sql})"
    programs = [app[0] for app in cursordb.execute (sql, paramaters)]
    return programs

def execution (start:str = "", end: str = "") -> tuple:
    """
    This is a common function that is used by programs 
    in   duration   and  time_spent.   This   function 
    converts  start and end  to utc format, hence  YOU 
    DONT NEED TO CONVERT WHERE IT IS CALLED.
    """

    sql =   "SELECT name, start, end FROM time_stamps\
            LEFT JOIN programs ON programs.id = time_stamps.program_id\
            WHERE end IS NOT NULL"
    parameters = []
    
    if not (start == "" and end == ""):
        start = to_utc (datetime.fromisoformat (start)).isoformat ()
        end = to_utc (datetime.fromisoformat (end)).isoformat ()
        
        sql =   f"SELECT * FROM ({sql})\
                WHERE DATETIME (start) > DATETIME (?)\
                OR (DATETIME (start) < ? AND DATETIME (end) > ?)"
        sql =   f"SELECT * FROM ({sql})\
                WHERE DATETIME (end) <= ?\
                OR (DATETIME (end) > ? AND DATETIME (start) < ?)"
        
        # if start only start is specified or end is specified ...
        # add it later ...
        
        parameters.extend ([start, start, start, end, end, end])
    
    return (sql, parameters)


def app_usage (start: str = "", end: str = "") -> list:
    # returns the list of app, time spent tuple
    
    apps = programs_in_duration (start, end)
    appUsage = []

    for app in apps:
        appUsage.append ((app, time_spent (start, end, app)))
    
    return sorted (appUsage, key = lambda appTuple: appTuple [1], reverse = True)

def most_used_app (start: str = "", end: str = "") -> tuple:
    # returns  the  most  used app  within  the  given
    # duration
    
    appUsage = app_usage (start, end)

    if not appUsage == []:
        return appUsage [0]
    else:
        raise NoRecordFound ("No available data")
    
def add_daily_limit (process_id: int, t: int):
    # adds program to daily limited database
    cursordb.execute ("""
                      INSERT INTO daily_limits
                      (limits_id, limits)
                      VALUES (?, ?)
                      """, [process_id, t])
    database.commit ()

def get_limit (process_id: int) -> sqlite3.Cursor:
    """
    Returns daily limited program and its time, if not
    found it raises the exception of NoLimitFound
    """
    
    limit = [process for process in cursordb.execute ("""
                                                      SELECT * FROM daily_limits 
                                                      WHERE limits_id = ?
                                                      """, [process_id])]
    
    if not limit == []:
        return limit
    else:        
        process = [program for program in cursordb.execute ("""
                                                            SELECT name FROM programs 
                                                            WHERE id = ?
                                                            """, [process_id])] [0]        
        
        raise NoRecordFound (f"No limit found for {process}")

def all_daily_limits () -> list[tuple]:
    # displays all the daily limits
    # return format: [(id, name, limit), ...]
    return [programs for programs in cursordb.execute ("""
                                                       SELECT programs.id, programs.name, daily_limits.limits 
                                                       FROM programs 
                                                       LEFT JOIN daily_limits 
                                                       ON programs.id = daily_limits.limits_id 
                                                       WHERE daily_limits.limits IS NOT NULL;
                                                       """)]
