@echo off
setlocal

set "REPO_ROOT=%~dp0.."
set "ENV_FILE=%REPO_ROOT%\.op\openrouter.env"
set "PS_CMD=$ErrorActionPreference = 'Stop'; op run --env-file='%ENV_FILE%' -- codex %*"

powershell -ExecutionPolicy Bypass -Command "%PS_CMD%"
exit /b %ERRORLEVEL%
