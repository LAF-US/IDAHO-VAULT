@echo off
setlocal

set "SWEEP_SCRIPT=%~dp0phone-link-auto-sweep.ps1"
set "STARTUP_DIR=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup"
set "STARTUP_LAUNCHER=%STARTUP_DIR%\IDAHO-VAULT-Phone-Link-Sweep.cmd"

if /I "%~1"=="--register-startup" goto register_startup
if /I "%~1"=="--unregister-startup" goto unregister_startup

set "SWEEP_SCRIPT=%~dp0.github\scripts\phone_link_auto_sweep.py"

:finish
endlocal
exit /b 0

:register_startup
if not exist "%STARTUP_DIR%" mkdir "%STARTUP_DIR%"
(
echo @echo off
echo call "%~f0"
) > "%STARTUP_LAUNCHER%"
echo Startup registration ensured at "%STARTUP_LAUNCHER%".
goto finish

:unregister_startup
if exist "%STARTUP_LAUNCHER%" del "%STARTUP_LAUNCHER%"
echo Startup registration removed from "%STARTUP_LAUNCHER%".
goto finish
