@echo off
setlocal

call "%~dp0STOP-PHONE-LINK-SWEEP.cmd"
call "%~dp0START-PHONE-LINK-SWEEP.cmd"

echo Phone Link autosweep restarted in hidden mode.

endlocal
exit /b 0
