@echo off
setlocal enabledelayedexpansion

echo ============================================
echo 1Password CLI Setup for OpenClaw
echo ============================================
echo.

REM Step 1: Check if 1Password CLI is installed
echo [Step 1/5] Checking for 1Password CLI...
where op >nul 2>&1
if errorlevel 1 (
    echo [INFO] 1Password CLI not found. Installing via Scoop...
    
    REM Check Scoop
    where scoop >nul 2>&1
    if errorlevel 1 (
        echo [ERROR] Scoop not found. Please install Scoop first:
        echo   https://scoop.sh/
        pause
        exit /b 1
    )
    
    echo Installing 1Password CLI...
    scoop install 1password
    if errorlevel 1 (
        echo [ERROR] Failed to install 1Password CLI
        pause
        exit /b 1
    )
    echo [OK] 1Password CLI installed
) else (
    echo [OK] 1Password CLI already installed
    op --version
)
echo.

REM Step 2: Check if signed in
echo [Step 2/5] Checking 1Password authentication...
op whoami >nul 2>&1
if errorlevel 1 (
    echo.
    echo [INFO] Not signed in to 1Password
    echo.
    echo Please sign in manually:
    echo   op account add --address my.1password.com --email your@email.com
    echo   op signin
    echo.
    echo Or set OP_SERVICE_ACCOUNT_TOKEN environment variable
    echo.
    set /p CONTINUE="Continue anyway? (y/n): "
    if /i "!CONTINUE!" neq "y" exit /b 1
) else (
    echo [OK] Already signed in:
    op whoami
echo.
)

REM Step 3: Set up environment variables
echo [Step 3/5] Setting up environment...
echo.
echo Add these to your environment (System Properties ^> Environment Variables):
echo.
echo   Variable: OP_CONFIG_DIR
echo   Value: %USERPROFILE%\.op
echo.
echo   Variable: OP_SERVICE_ACCOUNT_TOKEN (optional, for automation)
echo   Value: ops_...
echo.

REM Create .op directory if it doesn't exist
if not exist "%USERPROFILE%\.op" (
    mkdir "%USERPROFILE%\.op"
    echo [OK] Created %USERPROFILE%\.op directory
)

REM Step 4: Update OpenClaw config
echo [Step 4/5] Updating OpenClaw configuration...
echo.
echo Checking if 1Password is configured in openclaw.json...

REM Check if jq is available to parse JSON
where jq >nul 2>&1
if errorlevel 1 (
    echo [INFO] jq not installed. Please manually update openclaw.json:
    echo   Set secrets.providers.1password.enabled = true
) else (
    echo [OK] jq found. You can update config with:
    echo   openclaw config set secrets.providers.1password.enabled true
)
echo.

REM Step 5: Test 1Password integration
echo [Step 5/5] Testing 1Password integration...
echo.
echo Testing basic commands:
echo.

echo -- op --version --
op --version 2>nul || echo [WARN] op command not available
echo.

echo -- op vault list --
op vault list 2>nul || echo [INFO] Sign in required to list vaults
echo.

echo ============================================
echo 1Password CLI Setup Complete!
echo ============================================
echo.
echo Quick commands:
echo   op signin              - Sign in to 1Password
echo   op vault list          - List your vaults
echo   op item list           - List items in default vault
echo   op item get "Item Name" - Get item details
echo.
echo For OpenClaw integration:
echo   openclaw secrets configure  - Interactive secrets setup
echo   openclaw secrets audit    - Check secret references
echo.

pause
