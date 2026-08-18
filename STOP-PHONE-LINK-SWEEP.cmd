@echo off
setlocal
set "PYTHON_SWEEP=%~dp0.github\scripts\phone_link_auto_sweep.py"
set "POWERSHELL_SWEEP=%~dp0phone-link-auto-sweep.ps1"

powershell -NoLogo -NoProfile -ExecutionPolicy Bypass -Command ^
	"$pythonSweep = [regex]::Escape([IO.Path]::GetFullPath($env:PYTHON_SWEEP)); $powershellSweep = [regex]::Escape([IO.Path]::GetFullPath($env:POWERSHELL_SWEEP)); $procs = Get-CimInstance Win32_Process | Where-Object { ($_.Name -match '^(pythonw?|pyw)(\.exe)?$' -and $_.CommandLine -match $pythonSweep) -or ($_.Name -match '^powershell(\.exe)?$' -and $_.CommandLine -match '-File' -and $_.CommandLine -match $powershellSweep) }; $stopped = 0; foreach ($p in $procs) { try { Stop-Process -Id $p.ProcessId -Force -ErrorAction Stop; $stopped++; Write-Host ('Stopped PID ' + $p.ProcessId) } catch { Write-Host ('Could not stop PID ' + $p.ProcessId) } }; Write-Host ('Stopped ' + $stopped + ' autosweep process(es).')"

endlocal
exit /b 0
