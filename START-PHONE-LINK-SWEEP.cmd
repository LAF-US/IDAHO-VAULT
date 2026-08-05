@echo off
setlocal

set "SWEEP_SCRIPT=%~dp0.github\scripts\phone_link_auto_sweep.py"

if not exist "%SWEEP_SCRIPT%" (
	echo Missing Phone Link sweeper: "%SWEEP_SCRIPT%"
	exit /b 1
)

where pythonw.exe >nul 2>nul
if %ERRORLEVEL% EQU 0 (
	start "Phone Link Auto Sweep" /B pythonw.exe "%SWEEP_SCRIPT%"
	exit /b 0
)

where pyw.exe >nul 2>nul
if %ERRORLEVEL% EQU 0 (
	start "Phone Link Auto Sweep" /B pyw.exe -3 "%SWEEP_SCRIPT%"
	exit /b 0
)

where python.exe >nul 2>nul
if %ERRORLEVEL% EQU 0 (
	start "Phone Link Auto Sweep" /MIN python.exe "%SWEEP_SCRIPT%"
	exit /b 0
)

echo Python was not found on PATH. Install Python or add python.exe/pythonw.exe to PATH.
exit /b 1
