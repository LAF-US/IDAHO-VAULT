@echo off
REM Phone Link Intake — run from vault root
REM Moves files from Phone Link downloads into INBOX/phone-link/
REM
REM Usage:
REM   phone-link-intake.bat              (normal run)
REM   phone-link-intake.bat --dry-run    (preview only)
REM   phone-link-intake.bat --copy       (copy instead of move)

cd /d "%~dp0"
python .github/scripts/phone_link_intake.py %*
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo Intake failed. Check output above.
    pause
    exit /b 1
)
echo.
echo Done. Review INBOX/phone-link/ for ingested files.
pause
