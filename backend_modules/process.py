from psutil         import Process, NoSuchProcess, AccessDenied
from win32gui       import GetForegroundWindow
from win32process   import GetWindowThreadProcessId
from .calc_time     import current_time, to_utc
from .database      import in_program_list, add_program, pid

# During  intialization,  it is possible that None is passed due  to  some 
# error. Hence, the type is compared to determine if its an Process object 
# or NoneType. For encountering an error the name is set to none.

class program:
    def __init__ (self, application):
        if isinstance (application, Process):
            # oneshot is for optimization
            with application.oneshot ():    
                self.name = application.name ()[0:-4]

            # adds program into database if its not entered previously
            if not in_program_list (self.name):
                add_program (self.name)
            
            self.pid = pid (self.name)           

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