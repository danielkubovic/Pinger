@echo off
set interval=60
set ip=192.168.0.1

:loop
time /T
ping %ip% -t >> output.txt
sleep -m 6000
goto loop
