echo off
IF [%1] == [] (python main.py) ELSE (python backend_modules/%1.py)