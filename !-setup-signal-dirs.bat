@echo off
echo Creating Signal credentials directory structure...
mkdir "C:\Users\loganf\Documents\IDAHO-VAULT\.openclaw\credentials\signal\default" 2>nul
if exist "C:\Users\loganf\Documents\IDAHO-VAULT\.openclaw\credentials\signal\default" (
    echo [OK] Directory created
    echo { "status": "unconfigured" } > "C:\Users\loganf\Documents\IDAHO-VAULT\.openclaw\credentials\signal\default\config.json"
    echo [OK] Config file created
) else (
    echo [ERROR] Failed to create directory
    exit /b 1
)
pause
