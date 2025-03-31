import process
from time import sleep

current = []
while True:
    app = process.program (process.current_process ())
    isCurrent = process.is_current_process (app, current)
    if isCurrent:
        print ("I am here!")
    else:
        current.append (app)
        for x in current:
            print (x.name)
        print ()

    sleep (1)
