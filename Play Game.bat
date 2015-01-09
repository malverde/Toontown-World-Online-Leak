@echo off

set /P TTWUsername="Username (DEFAULT: username): " || ^
set TTWUsername=username
set TTWPassword=password
set TTW_PLAYCOOKIE=%TTWUsername%
set TTW_GAMESERVER=108.161.134.133

rem Read the contents of PPYTHON_PATH into %PPYTHON_PATH%:
set /P PPYTHON_PATH=<PPYTHON_PATH

CALL "toontown\toonbase\gameservices.exe"

echo ===============================
echo Starting Toontown World Online...
echo ppython: %PPYTHON_PATH%
echo Username: %TTWUsername%
echo Client Agent IP: %TTW_GAMESERVER%
echo ===============================

%PPYTHON_PATH% -m toontown.toonbase.ToontownStart
pause
