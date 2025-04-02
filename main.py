from time import sleep

import process

# important control flags
asstiantRunning = True

current = []

def assistant (currentAppList):
    while True:
	    # if not needed remove it
	  	currentAppList.sort (key = lambda application: application.name)
	  	
	  	app = process.program (process.foreground_process ())
	  	
	  	# checking if the function exists
	  	if app.name != None:
	  	    if process.in_current (app, current):
	  	        # do something...
	  	        print (app.start_time ())
	  	        pass
	  	    else:
	  	        currentAppList.append (app)
	  	        # do something... 
	  	    
	  	for application in currentAppList:
	  	    print (application.name, end = " ")
	  	print()
	  	
        sleep (1)
