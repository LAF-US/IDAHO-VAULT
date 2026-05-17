@echo off
setlocal

set "REPO_ROOT=%~dp0.."
set "ENV_FILE=%REPO_ROOT%\.op\openrouter.env"
set "RESOLVER=%~dp0resolve-openrouter-secret.ps1"
set "PS_CMD=$ErrorActionPreference = 'Stop'; op signin | Out-Null; if (-not (Test-Path '%ENV_FILE%')) { & '%RESOLVER%' | Out-Null }; op run --env-file='%ENV_FILE%' -- codex --profile openrouter"

powershell -ExecutionPolicy Bypass -Command "%PS_CMD%"
