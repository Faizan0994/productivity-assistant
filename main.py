from time import sleep
import process

current = []
while True:
    # worth soting? maybe remove in future...
    current.sort (key = lambda application: application.name)
    app = process.program (process.foreground_process ())
    
    # checking if the function exists...
    if app.name != None:
        if process.in_current (app, current):
            # do something...
            pass
        else:
            # do something... 
            current.append (app)
        
    for x in current:
        print (x.name, end = " ")
    print()
    sleep (1)
