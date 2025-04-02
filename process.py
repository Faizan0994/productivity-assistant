from psutil         import Process, NoSuchProcess, AccessDenied
from win32gui       import GetForegroundWindow
from win32process   import GetWindowThreadProcessId
from datetime       import datetime

# During  intialization,  it is possible that None is passed due  to  some 
# error. Hence, the type is compared to determine if its an Process object 
# or NoneType. For encountering an error the name is set to none.

class program:
    __app = None

    def __init__ (self, application):
        if isinstance (application, Process):
            self.__app = application
        
            with application.oneshot ():    
                # oneshot is for optimization
                self.name = application.name ()
                self.startTime = datetime.fromtimestamp (application.create_time ())
                self.pid = application.pid
         
        elif isinstance (application, type (None)):
            self.name = None

    def __eq__ (self, other):
        if self.name == other.name:
            return True
        else:
            return False
    
    def __gt__ (self, other):
        if self.name > other.name:
            return True
        else:
            return False

    def __lt__ (self, other):
        if self.name < other.name:
            return True
        else:
            return False

    def print_time (self):  
        # returns dattime object as readable string
        print (self.startTime.strftime ("%d/%m/%y: %I:%M:%S %p %z"))

    def running (self):     
        # do nott use pid_exists
        return self.__app.is_running ()


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

def in_current (app, orderedAppList): 
    # To check if the app is currently running
    if app in orderedAppList:
        return True
    else:
        return False
