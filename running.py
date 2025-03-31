from psutil         import Process
from win32gui       import GetForegroundWindow
from win32process   import GetWindowThreadProcessId
from time           import sleep
from datetime       import datetime

class program:
    __app = None

    def __init__ (self, application):
        processDict = application.as_dict()
        
        self.__app = application
        self.name = processDict["name"]
        self.startTime = processDict["create_time"]
        self.pid = processDict["pid"]

    def started (self):
        return datetime.fromtimestamp (self.startTime).strftime("%d/%m/%y: %I:%M:%S %p")

    def isRunning (self):
        return __app.is_running ()

def foregroundProcess ():
    return Process (GetWindowThreadProcessId (GetForegroundWindow ()) [1])

app = program (foregroundProcess ())

print (app.isRunning())
