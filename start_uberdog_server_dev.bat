@echo off

set MAX_CHANNELS=999999
set STATE_SERVER=4002
set ASTRON_IP=127.0.0.1:7199
set EVENT_LOGGER_IP=127.0.0.1:7197
set BASE_CHANNEL=1000000
set CONFIG=config/dev-server.prc

rem Read the contents of PPYTHON_PATH into %PPYTHON_PATH%:
set /P PPYTHON_PATH=<PPYTHON_PATH

echo ===============================
echo Starting Toontown World UberDOG server...
echo ppython: %PPYTHON_PATH%
echo Base Channel: %BASE_CHANNEL%
echo Max Channels: %MAX_CHANNELS%
echo State Server ID: %STATE_SERVER%
echo Message Director IP: %ASTRON_IP%
echo Event Logger IP: %EVENT_LOGGER_IP%
echo SERVER configuration: %CONFIG%
echo ===============================

:main
%PPYTHON_PATH% -m toontown.uberdog.ServiceStart --base-channel %BASE_CHANNEL% ^
               --max-channels %MAX_CHANNELS% --stateserver %STATE_SERVER% ^
               config %CONFIG% ^
               --astron-ip %ASTRON_IP% --eventlogger-ip %EVENT_LOGGER_IP%

goto main