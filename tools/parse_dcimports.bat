set /P PPYTHON_PATH=<..\PPYTHON_PATH

%PPYTHON_PATH% parse_dcimports.py -o ..\otp\distributed\DCClassImports.py ..\astron\toontown.dc 
pause
