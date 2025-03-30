import psutil

for process in psutil.process_iter(["name", "username"]):
    print (process.info)