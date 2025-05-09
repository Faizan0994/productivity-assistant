from backend_modules.process    import program, foreground_process
from backend_modules.database   import update_endtime, add_current

from time       import sleep

# important control flags
asstiantRunning = True

app = program (None)

def assistant (prevApp: program):
    while asstiantRunning:
        currApp = program (foreground_process ())

        # checking if the process exists
        if currApp.name != None:  
            if currApp != prevApp:
                if prevApp.name != None:
                    prevApp.set_time ("end")
                    update_endtime (index, prevApp.endTime)
                
                currApp.set_time ("start")
                index = add_current (currApp.process_id, currApp.startTime)
                prevApp = currApp
            else:
                prevApp.set_time ("end")
                update_endtime (index, prevApp.endTime)
        
        # database.total_time ("Code")
        sleep (1)


# main function execution 
assistant (app)