from psutil         import Process

from win32gui       import GetForegroundWindow
from win32process   import GetWindowThreadProcessId
from time           import sleep


class program:
    def __init__ (self, application):
        processDict = application.as_dict()
        self.name = processDict["name"]
        self.startTime = processDict["create_time"]
        self.pid = processDict["pid"]

def foregroundProcess ():
    return Process (GetWindowThreadProcessId (GetForegroundWindow ()) [1])

app = program (foregroundProcess ())

print (app.pid)
