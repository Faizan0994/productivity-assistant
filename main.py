from backend_modules.process    import program, foreground_process
from backend_modules.database   import update_endtime, add_current
import backend_modules.database as database

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
                index = add_current (currApp.pid, currApp.startTime)
                prevApp = currApp
            else:
                prevApp.set_time ("end")
                update_endtime (index, prevApp.endTime)
        
        # database.total_time ("Code")
        sleep (1)


# main function execution 
# assistant (app)

from backend_modules.database import cordinates, programs_in_duration
from backend_modules.calc_time import x_points
from datetime import datetime

print ("Intervals:")
points = x_points (datetime (2025, 4, 19, 10, 0, 0), datetime (2025, 4, 22, 12, 0, 0))
for i in points:
    print (i)
print ()

programs_in_duration (start = datetime (2025, 4, 19, 10, 0, 0).isoformat (), end = datetime (2025, 4, 22, 12, 0, 0).isoformat ())