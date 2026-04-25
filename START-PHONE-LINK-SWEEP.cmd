@echo off
set "SWEEP_SCRIPT=%~dp0phone-link-auto-sweep.ps1"

powershell -NoLogo -NoProfile -ExecutionPolicy Bypass -WindowStyle Hidden -Command ^
	"Start-Process -FilePath 'powershell.exe' -WindowStyle Hidden -ArgumentList @('-NoLogo','-NoProfile','-ExecutionPolicy','Bypass','-File','\"%SWEEP_SCRIPT%\"')"

exit /b 0