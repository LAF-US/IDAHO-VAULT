@echo off
setlocal enabledelayedexpansion

echo ============================================
echo signal-cli Installation for OpenClaw
echo ============================================
echo.

REM Check Java
echo [1/5] Checking Java installation...
java -version >java_check.txt 2>&1
findstr "version" java_check.txt >nul
if errorlevel 1 (
    echo [ERROR] Java not found or not in PATH
    echo Please install Java 11+ from: https://adoptium.net/
    echo.
    echo After installing Java, run this script again.
    del java_check.txt 2>nul
    exit /b 1
)
echo [OK] Java found
type java_check.txt
del java_check.txt 2>nul
echo.

REM Check Scoop
echo [2/5] Checking Scoop installation...
where scoop >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Scoop not found in PATH
    echo Please install Scoop first: https://scoop.sh/
    echo.
    echo Run this in PowerShell:
    echo   Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
    echo   irm get.scoop.sh ^| iex
    exit /b 1
)
echo [OK] Scoop found
echo.

REM Add extras bucket if not present
echo [3/5] Ensuring extras bucket is added...
scoop bucket list | findstr "extras" >nul
if errorlevel 1 (
    echo Adding extras bucket...
    scoop bucket add extras
) else (
    echo [OK] Extras bucket already present
)
echo.

REM Install signal-cli
echo [4/5] Installing signal-cli...
scoop install signal-cli
if errorlevel 1 (
    echo [ERROR] signal-cli installation failed
    exit /b 1
)
echo [OK] signal-cli installed
echo.

REM Verify
echo [5/5] Verifying installation...
signal-cli --version
echo.

echo ============================================
echo signal-cli Installation Complete!
echo ============================================
echo.
echo Next steps:
echo   1. Register your Signal phone number:
echo      signal-cli -u +1234567890 register
echo.
echo   2. Verify with the code you receive:
echo      signal-cli -u +1234567890 verify ^<CODE^>
echo.
echo   3. Update openclaw.json with your Signal number
echo.

pause