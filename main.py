import backend_modules.process  as process
import backend_modules.database as database

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
                if not database.in_program_list (app.name):
                    database.add_program(app)
                    
                # if not app.name in database.programList ():
                #     database.addProgram (app)	  	    

        return None
        
        print()
        sleep (1)


# main function execution 
assistant (current)