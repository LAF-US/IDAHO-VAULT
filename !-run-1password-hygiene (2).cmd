@echo off
setlocal

set "ROOT=%~dp0"

powershell -ExecutionPolicy Bypass -File "%ROOT%1password-preflight.ps1"
if errorlevel 1 exit /b %errorlevel%

powershell -ExecutionPolicy Bypass -File "%ROOT%credential-sweep.ps1" -Mode api-surface
if errorlevel 1 exit /b %errorlevel%

powershell -ExecutionPolicy Bypass -File "%ROOT%duplicate-credential-triage.ps1" -Mode strict
if errorlevel 1 exit /b %errorlevel%

powershell -ExecutionPolicy Bypass -File "%ROOT%vault-placement-sweep.ps1"
if errorlevel 1 exit /b %errorlevel%

powershell -ExecutionPolicy Bypass -File "%ROOT%normalize-item-metadata.ps1"
