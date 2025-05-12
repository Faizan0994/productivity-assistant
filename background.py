import winreg
import os

from threading  import Thread
import sys
from psutil     import process_iter
from main       import assistant
from gui        import main             as gui

background = Thread (target = assistant)

# Using registery editing
def add_to_startup (app_name, exe_path = None):
    if exe_path is None:
        # executable's path
        exe_path = sys.executable

    key = winreg.OpenKey (
        winreg.HKEY_CURRENT_USER,
        r"Software\Microsoft\Windows\CurrentVersion\Run",
        0, winreg.KEY_SET_VALUE
    )

    # launch in silent mode at startup
    winreg.SetValueEx (key, app_name, 0, winreg.REG_SZ, f'"{exe_path}" --silent')
    winreg.CloseKey (key)

def is_first_run (flag_file = "first_run.flag"):
    return not os.path.exists (flag_file)

def mark_first_run_done (flag_file = "first_run.flag"):
    try:
        with open(flag_file, "w") as f:
            f.write ("done")
    except:
        pass

if is_first_run():
    add_to_startup ("productivity_assistant")
    mark_first_run_done ()

def is_silent_mode():
    return "--silent" in sys.argv

for process in process_iter (['name']):
    if not process == __name__:
        background.start ()
        if not is_silent_mode ():
            gui ()
        background.join()
    else:
        gui ()