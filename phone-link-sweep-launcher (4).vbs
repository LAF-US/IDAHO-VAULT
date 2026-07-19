Dim oShell, oEnv, sScript
Set oShell = CreateObject("WScript.Shell")
Set oEnv = oShell.Environment("Process")
oEnv("SWEEP_SCRIPT") = "C:\Users\loganf\Documents\IDAHO-VAULT\phone-link-auto-sweep.ps1"
sScript = "powershell.exe -NoLogo -NoProfile -ExecutionPolicy Bypass -WindowStyle Hidden -File ""%SWEEP_SCRIPT%"""
oShell.Run sScript, 0, False
Set oShell = Nothing
WScript.Quit 0