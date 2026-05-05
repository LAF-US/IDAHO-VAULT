@echo off
setlocal

set "SCRIPT=%~dp0normalize-item-metadata.ps1"

if /I "%~1"=="apply-titles" (
  if /I not "%~2"=="EDIT_ITEMS" (
    echo Usage: %~nx0 apply-titles EDIT_ITEMS
    exit /b 1
  )
  powershell -ExecutionPolicy Bypass -File "%SCRIPT%" -ApplyTitles -ConfirmToken EDIT_ITEMS
  goto :eof
)

if /I "%~1"=="apply-all" (
  if /I not "%~2"=="EDIT_ITEMS" (
    echo Usage: %~nx0 apply-all EDIT_ITEMS
    exit /b 1
  )
  powershell -ExecutionPolicy Bypass -File "%SCRIPT%" -ApplyTitles -ApplyTags -ConfirmToken EDIT_ITEMS
  goto :eof
)

powershell -ExecutionPolicy Bypass -File "%SCRIPT%"
