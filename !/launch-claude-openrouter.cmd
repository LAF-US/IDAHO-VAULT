@echo off
setlocal

set "REPO_ROOT=%~dp0.."
set "ENV_FILE=%REPO_ROOT%\.op\openrouter.env"

if not exist "%ENV_FILE%" (
    echo Error: %ENV_FILE% not found
    exit /b 1
)

for /f "usebackq tokens=1,* delims==" %%a in ("%ENV_FILE%") do (
    set "%%a=%%b"
)

claude %*
exit /b %ERRORLEVEL%