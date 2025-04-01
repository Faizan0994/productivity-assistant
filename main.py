from time import sleep
import process

current = []
while True:
    current.sort (key = lambda application: application.name)
    app = process.program (process.foreground_process ())
    
    # checking if the function exists...
    if app.name != None:
        isCurrent = process.in_current (app, current)
        if isCurrent:
            # do something...
            pass
        else:
            # do something... 
            current.append (app)
        
    for x in current:
        print (x.name, end = " ")
    print()
    sleep (1)
