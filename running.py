from psutil         import Process
from win32gui       import GetForegroundWindow
from win32process   import GetWindowThreadProcessId
from time           import sleep
from datetime       import datetime

class program:
    __app = None

    def __init__ (self, application):
        self.__app = application
        
        with application.oneshot ():
            self.name = application.name ()
            self.startTime = application.create_time ()
            self.pid = application.pid

    def start_time (self):
        return datetime.fromtimestamp (self.startTime).strftime ("%d/%m/%y: %I:%M:%S %p")

    def running (self):
        return self.__app.is_running ()

def current_process ():
    return Process (GetWindowThreadProcessId (GetForegroundWindow ()) [1])

def is_current_process (proc):
    currentProcess = current_process ()

    with proc.oneshot ():
        pid = process.pid
    with currentProcess ():
        currentPid = currentProcess.pid

    if pid == currentPid:
        return True
    else
        return False
