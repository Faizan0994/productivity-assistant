from psutil         import Process
from win32gui       import GetForegroundWindow
from win32process   import GetWindowThreadProcessId
from datetime       import datetime

class program:
    __app = None

    def __init__ (self, application):
        self.__app = application
        
        with application.oneshot ():
            self.name = application.name ()
            self.startTime = application.create_time ()
            self.pid = application.pid
    
    def __eq__ (self, other):
        if self.name == other.name:
            return True
        else:
            return False

    def start_time (self):
        return datetime.fromtimestamp (self.startTime).strftime ("%d/%m/%y: %I:%M:%S %p")

    def running (self):
        return self.__app.is_running ()

def current_process ():
    try:
        return Process (GetWindowThreadProcessId (GetForegroundWindow ()) [1])
    except NoSuchProcess:
        return None
    except AccessDenied:
        return None

def is_current_process (app, appList):
    for currentApp in appList:
        if currentApp == app:
            return True
    return False
