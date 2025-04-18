import backend_modules.process  as process
import backend_modules.database as database

from time       import sleep

# important control flags
asstiantRunning = True

app = process.program (None)

def assistant (prevApp: process.program):
    while True:
        currApp = process.program (process.foreground_process ())

        # checking if the process exists
        if currApp.name != None:  
            if currApp != prevApp:
                if prevApp.name != None:
                    prevApp.set_time ("end")
                    database.update_endtime (index, prevApp.endTime)
                
                currApp.set_time ("start")
                index = database.add_current (currApp.pid, currApp.startTime)
                prevApp = currApp
            else:
                prevApp.set_time ("end")
                database.update_endtime (index, prevApp.endTime)
        
        print()
        sleep (5)


# main function execution 
assistant (app)