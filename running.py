from psutil         import Process
from win32gui       import GetForegroundWindow
from win32process   import GetWindowThreadProcessId

def process ():
    return Process(GetWindowThreadProcessId(GetForegroundWindow())[1])

print (process ())
