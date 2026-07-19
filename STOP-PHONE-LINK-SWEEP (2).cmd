@echo off
setlocal

powershell -NoLogo -NoProfile -ExecutionPolicy Bypass -Command ^
	"$procs = Get-CimInstance Win32_Process | Where-Object { $_.Name -match '^powershell(\.exe)?$' -and $_.CommandLine -match '-File' -and $_.CommandLine -match 'phone-link-auto-sweep\.ps1' }; $stopped = 0; foreach ($p in $procs) { try { Stop-Process -Id $p.ProcessId -Force -ErrorAction Stop; $stopped++; Write-Host ('Stopped PID ' + $p.ProcessId) } catch { Write-Host ('Could not stop PID ' + $p.ProcessId) } }; Write-Host ('Stopped ' + $stopped + ' autosweep process(es).')"

endlocal
exit /b 0
