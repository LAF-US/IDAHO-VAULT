@echo off
setlocal

set "SCRIPT=%~dp0vault-placement-sweep.ps1"

if /I "%~1"=="apply" (
  if /I not "%~2"=="MOVE_ITEMS" (
    echo Usage: %~nx0 apply MOVE_ITEMS
    exit /b 1
  )
  powershell -ExecutionPolicy Bypass -File "%SCRIPT%" -Apply -ApplyThreshold high -ConfirmToken MOVE_ITEMS
  goto :eof
)

if /I "%~1"=="apply-medium" (
  if /I not "%~2"=="MOVE_ITEMS" (
    echo Usage: %~nx0 apply-medium MOVE_ITEMS
    exit /b 1
  )
  powershell -ExecutionPolicy Bypass -File "%SCRIPT%" -Apply -ApplyThreshold medium -ConfirmToken MOVE_ITEMS
  goto :eof
)

if /I "%~1"=="all" (
  powershell -ExecutionPolicy Bypass -File "%SCRIPT%" -IncludeLowConfidence
  goto :eof
)

powershell -ExecutionPolicy Bypass -File "%SCRIPT%"
