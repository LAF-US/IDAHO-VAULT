@echo off
setlocal

set "PID_FILE=%~dp0!\INBOX\_phone-link-watcher.pid"

powershell -NoLogo -NoProfile -ExecutionPolicy Bypass -Command ^
	"$pidFile = '%PID_FILE%'; if (-not (Test-Path -LiteralPath $pidFile)) { Write-Host 'No watcher PID file found.'; exit 0 }; $raw = Get-Content -LiteralPath $pidFile -ErrorAction SilentlyContinue | Select-Object -First 1; if (-not $raw) { Write-Host 'Watcher PID file is empty.'; Remove-Item -LiteralPath $pidFile -Force -ErrorAction SilentlyContinue; exit 0 }; $targetPid = 0; if (-not [int]::TryParse($raw, [ref]$targetPid)) { Write-Host ('Watcher PID file is invalid: ' + $raw); Remove-Item -LiteralPath $pidFile -Force -ErrorAction SilentlyContinue; exit 0 }; $proc = Get-Process -Id $targetPid -ErrorAction SilentlyContinue; if ($null -eq $proc) { Write-Host ('Watcher process ' + $targetPid + ' is not running.'); Remove-Item -LiteralPath $pidFile -Force -ErrorAction SilentlyContinue; exit 0 }; try { Stop-Process -Id $targetPid -Force -ErrorAction Stop; Write-Host ('Stopped PID ' + $targetPid) } catch { Write-Host ('Could not stop PID ' + $targetPid) }; Remove-Item -LiteralPath $pidFile -Force -ErrorAction SilentlyContinue"

endlocal
exit /b 0
