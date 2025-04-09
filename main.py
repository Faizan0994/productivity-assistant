from time       import sleep

import backend_modules.process as process

# important control flags
asstiantRunning = True

current = []

def assistant (currentAppList):
    while True:
        # if not needed remove it
        currentAppList.sort (key = lambda application: application.name)
        
        app = process.program (process.foreground_process ())

        # checking if the process exists
        if app.name != None:
            if not process.in_current (app, current):
                currentAppList.append (app)
                # do something... 
	  	    
        for application in currentAppList:
            # print (application.name, end = " ")
            return application.startTime 
        print()
	  	
        sleep (1)


# main function execution 
from backend_modules.calc_time import to_utc
time = to_utc (assistant (current))
print (time)
