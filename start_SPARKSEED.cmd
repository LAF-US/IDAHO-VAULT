@echo off
setlocal

where py >nul 2>nul
if not errorlevel 1 (
    py -3 "%~dp0sta***REMOVED***SPARKSEED.py" %*
    exit /b %ERRORLEVEL%
)

where python >nul 2>nul
if not errorlevel 1 (
    python "%~dp0sta***REMOVED***SPARKSEED.py" %*
    exit /b %ERRORLEVEL%
)

echo SPARKSEED failed: Python was not found on PATH. 1>&2
exit /b 1
