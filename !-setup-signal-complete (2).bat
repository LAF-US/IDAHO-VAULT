@echo off
setlocal enabledelayedexpansion

echo ============================================
echo Signal-CLI Setup for OpenClaw
echo Phone: +12086279028
echo ============================================
echo.

set SIGNAL_NUMBER=+12086279028

REM Step 1: Check Java
echo [Step 1/6] Checking Java installation...
java -version >java_check.txt 2>&1
findstr "version" java_check.txt >nul
if errorlevel 1 (
    echo [ERROR] Java not found!
    echo Please install Java 11+ from: https://adoptium.net/
    del java_check.txt 2>nul
    pause
    exit /b 1
)
echo [OK] Java found
type java_check.txt
del java_check.txt 2>nul
echo.

REM Step 2: Check Scoop
echo [Step 2/6] Checking Scoop installation...
where scoop >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Scoop not found in PATH
    echo Please install Scoop from: https://scoop.sh/
    pause
    exit /b 1
)
echo [OK] Scoop found
echo.

REM Step 3: Install signal-cli
echo [Step 3/6] Installing signal-cli...
scoop bucket list | findstr "extras" >nul
if errorlevel 1 (
    echo Adding extras bucket...
    scoop bucket add extras
)
scoop install signal-cli
if errorlevel 1 (
    echo [ERROR] signal-cli installation failed
    pause
    exit /b 1
)
echo [OK] signal-cli installed
echo.

REM Step 4: Verify installation
echo [Step 4/6] Verifying signal-cli...
signal-cli --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] signal-cli not working properly
    pause
    exit /b 1
)
echo [OK] signal-cli working
echo.

REM Step 5: Create credentials directory
echo [Step 5/6] Creating credentials directory...
if not exist "C:\Users\loganf\Documents\IDAHO-VAULT\.openclaw\credentials\signal\default" (
    mkdir "C:\Users\loganf\Documents\IDAHO-VAULT\.openclaw\credentials\signal\default"
    echo [OK] Directory created
) else (
    echo [OK] Directory already exists
)
echo.

REM Step 6: Signal Registration (Manual)
echo [Step 6/6] Signal Registration
echo ============================================
echo IMPORTANT: You need to register your Signal number
echo.
echo Run these commands in a terminal:
echo.
echo   signal-cli -u %SIGNAL_NUMBER% register
echo.
echo You will receive a verification code via SMS.
echo Then run:
echo.
echo   signal-cli -u %SIGNAL_NUMBER% verify ^^^^CODE^^^^
echo.
echo Replace ^^^^CODE^^^^ with the actual verification code
echo.
echo After registration, Signal is configured to use:
echo   Number: %SIGNAL_NUMBER%
echo   Data Path: C:\Users\loganf\.openclaw\credentials\signal
echo.
echo ============================================
echo Setup Complete!
echo ============================================
echo.
echo Signal channel is ENABLED in openclaw.json
echo Restart OpenClaw gateway to activate Signal
echo.

pause
