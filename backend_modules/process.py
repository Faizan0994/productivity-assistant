from psutil         import ( NoSuchProcess, 
                            AccessDenied,
                            Process)

from .calc_time     import (convert_to_time,
                            current_time, 
                            datetime, 
                            timedelta,
                            to_utc)

from .database      import ( get_limit,
                            in_program_list, 
                            NoRecordFound,
                            add_program, 
                            time_spent, 
                            pid) 

from .settings      import get_settings
from win32process   import GetWindowThreadProcessId
from win32gui       import GetForegroundWindow
from signal         import SIGTERM
from os             import kill

# During  intialization,  it is possible that None is passed due  to  some 
# error. Hence, the type is compared to determine if its an Process object 
# or NoneType. For encountering an error the name is set to none.

class program:
    def __init__ (self, application):
        if isinstance (application, Process):
            # oneshot is for optimization
            with application.oneshot ():    
                self.name = application.name ()[0:-4]

            self.pid = application.pid
            # adds program into database if its not entered previously
            if not in_program_list (self.name):
                add_program (self.name)
            
            self.process_id = pid (self.name)
            
            # var for timeSpeantToday
            currentTime = current_time ()
            now = currentTime.date ()
            timezone = currentTime.tzinfo
            day_start = convert_to_time (get_settings ("day_start"))
            day_start = datetime (year = now.year, 
                                  month = now.month, 
                                  day = now.month,
                                  hour = day_start.hour,
                                  minute = day_start.minute,
                                  second = day_start.second,
                                  tzinfo = timezone).isoformat ()
            now = currentTime.isoformat ()

            self.timeSpentToday = time_spent (day_start, now, self.name)

            # deleting variables
            del (currentTime, now, timezone, day_start)

            # gets limit of the program
            try:
                self.limit = get_limit (self.process_id)
            except NoRecordFound:
                self.limit = None
            
            if not isinstance (self.limit, type (None)):
                self.limit = timedelta (minutes = self.limit [1])
                self.__check_limit ()
        
        elif isinstance (application, type (None)):
            self.name = None

    def __eq__ (self, other) -> bool:
        if self.name == other.name:
            return True
        else:
            return False
    
    def set_time (self, variable:str):
        if variable == "start":
            self.startTime = to_utc (current_time ()).isoformat ()
        elif variable == "end":
            self.endTime = to_utc (current_time ()).isoformat ()
        else:
            raise Exception (f"program.set_time:\t{variable} is not accepted as an argument")
    
    def __kill_process (self) -> None:
        # kills process
        kill (self.pid, SIGTERM)

    def __check_limit (self) -> None:
        # checks the daily limit and kills the process
        if self.limit >= self.timeSpentToday:
            self.__kill_process ()

def foreground_process ():
    """
    Returns  the  pid of the  window  present  in  the foreground.
    The  GetForegroundWindow  returns  the hwndle (handle  to  the  
    window).   As   we    need   the    PID,   we   pass   it   to  
    GetWindowThreadProcessID   which   gives   both   the  process 
    and thread id as a tuple.
    """
    # remove except and merge them togather later 
    try:
        return Process (GetWindowThreadProcessId (GetForegroundWindow ()) [1])
    except NoSuchProcess:
        return None
    except AccessDenied:
        return None
    except ValueError:
        return None