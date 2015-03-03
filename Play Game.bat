@echo off

set /P ttrUsername="Username: " || ^
set /P ttrPassword="Password: " || ^
set TTR_PLAYCOOKIE=%ttrUsername%:%ttrPassword%
set TTR_GAMESERVER=54.174.138.210

rem Read the contents of PPYTHON_PATH into %PPYTHON_PATH%:
set /P PPYTHON_PATH=<PPYTHON_PATH

echo ===============================
echo Starting Toontown World Online...
echo ppython: %PPYTHON_PATH%
echo Username: %ttrUsername%
echo Client Agent IP: %TTR_GAMESERVER%
echo ===============================

%PPYTHON_PATH% -m toontown.toonbase.ToontownStart
pause
