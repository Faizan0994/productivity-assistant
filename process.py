from psutil         import Process, NoSuchProcess, AccessDenied
from win32gui       import GetForegroundWindow
from win32process   import GetWindowThreadProcessId
from datetime       import datetime

# Program class represents the required information of the Process object
# for  example, its name, date of creation and process ID. The strat time
# is  stored in datetime object   and hence is of float type. This  *may* 
# prove  uselful in storing and  processing data. Hence another  function 
# was  made to display time in more readable fasion. The running  fnction
# is part of Process object, hence, it  became important to save it. As I 
# thought  of  avoiding it, hence, I made a private variable for  it  and 
# therefore,  it  can  now be only called wihin the class  and  for  this 
# instance  to  see  if process is running. It is important  to  NOT  USE 
# pid_exists  method for pids are  recycled. There is also a function  to 
# see if two programs are same by seeing if their names are same.

# During  intialization,  it is possible that None is passed due  to  some 
# error. Hence, the type is compared to determine if its an Process object 
# or NoneType. For encountering an error the name is set to none.

class program:
    __app = None

    def __init__ (self, application):
        if isinstance (application, Process):
            self.__app = application
        
            with application.oneshot ():
                self.name = application.name ()
                self.startTime = application.create_time ()
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

    def start_time (self):
        return datetime.fromtimestamp (self.startTime).strftime ("%d/%m/%y: %I:%M:%S %p")

    def running (self):
        return self.__app.is_running ()

# foreground  process  returns  the  pid of the  window  present  in  the
# foreground.  The GetForegroundWindow returns the hwndle (handle to  the 
# window).  As  we need the PID, we pass it  to  GetWindowThreadProcessID 
# which gives both the process and  thread id. GetProcessID can't be used
# as  it accepts pyHWND which I tried and have asked but failed. The  pid 
# is  passed  to Process to make a Process object. For  NoSuchErrors  and 
# AccessDenied return is None. See program commment.

def foreground_process ():
    try:
        return Process (GetWindowThreadProcessId (GetForegroundWindow ()) [1])
    except NoSuchProcess:
        return None
    except AccessDenied:
        return None
    except ValueError:
        return None

# Was thinking of implementing binary search... 

def in_current (app, orderedAppList):
    if app in ordderedAppList:
        return True
    else:
        return False
