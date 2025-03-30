from win32gui import GetForegroundWindow
import psutil
import time
import win32process

process_time={}
timestamp = {}
while True:
    currentApp = psutil.Process(win32process.GetWindowThreadProcessId(GetForegroundWindow())[1]).name().replace(".exe", "")
    """ The above line is equivalent to the following code:
    hwnd = GetForegroundWindow()  # Get the handle of currently active window. Google the term "handle" in windows
    pid = win32process.GetWindowThreadProcessId(hwnd)[1]  # Get the process id of the concerned process
    currentApp = psutil.Process(pid).name().replace(".exe", "")
    """
    timestamp[currentApp] = int(time.time()) # Current Epoch time
    time.sleep(1) # A one-second delay between iterations to prevent load on system resources
    if currentApp not in process_time.keys():
        process_time[currentApp] = 0
    process_time[currentApp] = process_time[currentApp]+(int(time.time())-timestamp[currentApp]) # Increase usage time by current time + last timestamp
    print(process_time)