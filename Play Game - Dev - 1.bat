@echo off

rem Read the contents of PPYTHON_PATH into %PPYTHON_PATH%:
set /P PPYTHON_PATH=<PPYTHON_PATH

echo ===============================
echo Starting Toontown World Online - DEV...

echo ===============================

%PPYTHON_PATH% -m start
pause
