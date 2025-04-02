from time import sleep

import process

# main loop flag
asstiantRunning = True

current = []

while True:
    # if not needed remove it
    current.sort (key = lambda application: application.name)
    
    app = process.program (process.foreground_process ())
    
    # checking if the function exists...
    if app.name != None:
        if process.in_current (app, current):
            # do something...
            pass
        else:
            current.append (app)
            # do something... 
        
    for x in current:
        print (x.name, end = " ")
    print()
    sleep (1)
