@echo off
setlocal enabledelayedexpansion

:: Process each dotfolder sequentially
set count=0
for /D %%d in ("C:\Users\loganf\Documents\IDAHO-VAULT\.*") do (
  set /a count+=1
  echo [!count!] Processing %%~nxd...
  powershell -Command "& 'C:\Users\loganf\Documents\IDAHO-VAULT\dotfolder-reconcile.ps1' '%%~nxd' -Apply -Force -Quiet"
  if errorlevel 1 (
    echo Error processing %%~nxd. Continuing...
  )
)
echo Done.
pause