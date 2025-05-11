from threading  import Thread
from psutil     import process_iter
from main       import assistant
from gui        import main             as gui

background = Thread (target = assistant)

for process in process_iter (['name']):
    if not process == __name__:
        background.start ()
        gui ()
        background.join ()
    else:
        gui ()