import backend_modules.process as process
from time       import sleep

# important control flags
asstiantRunning = True

current = []

def assistant (currentAppList) -> process.program:
    while True:
        # if not needed remove it
        currentAppList.sort (key = lambda application: application.name)
        app = process.program (process.foreground_process ())

        # checking if the process exists
        if app.name != None:
            if not process.in_current (app, current):
                currentAppList.append (app)
                # do something...
	  	    
            # if app is not in the database

        for application in currentAppList:
            # print (application.name, end = " ")
            return application
        print()
	  	
        sleep (1)


# main function execution 
from backend_modules import addProgram, database
import sqlite3

x = assistant (current)
print (x.name)
addProgram (x)