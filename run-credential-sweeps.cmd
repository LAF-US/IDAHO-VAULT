@echo off
setlocal

set "PS_CMD=$ErrorActionPreference = 'Stop'; & '%~dp0credential-sweep.ps1' -Mode api-surface; & '%~dp0credential-sweep.ps1' -Mode account-surface; & '%~dp0security-sweep.ps1'"
powershell -ExecutionPolicy Bypass -Command "%PS_CMD%"
