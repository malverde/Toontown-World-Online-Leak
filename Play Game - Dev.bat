@echo off

set /P ttrUsername="Username: " || ^
set ttrUsername=username
set ttrPassword=password
set TTR_PLAYCOOKIE=%ttrUsername%
set TTR_GAMESERVER=54.173.27.28

rem Read the contents of PPYTHON_PATH into %PPYTHON_PATH%:
set /P PPYTHON_PATH=<PPYTHON_PATH

echo ===============================
echo Starting Toontown World Online - DEV...
echo ppython: %PPYTHON_PATH%
echo Username: %ttrUsername%
echo Client Agent IP: %TTR_GAMESERVER%
echo ===============================

%PPYTHON_PATH% -m toontown.toonbase.ToontownStart
pause
