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
                
                currApp.set_time ("start")
                prevApp = currApp
                
            if not database.in_program_list (currApp.name):
                database.add_program(currApp)
                    
                # if not app.name in database.programList ():
                #     database.addProgram (app)	  	    

        return None
        
        print()
        sleep (1)


# main function execution 
assistant (app)