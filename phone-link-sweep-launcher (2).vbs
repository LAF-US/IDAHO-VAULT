Dim oShell, oEnv, fso, scriptDir, sweepScript, command
Set oShell = CreateObject("WScript.Shell")
Set oEnv = oShell.Environment("Process")
Set fso = CreateObject("Scripting.FileSystemObject")

scriptDir = fso.GetParentFolderName(WScript.ScriptFullName)
sweepScript = fso.BuildPath(scriptDir, "phone-link-auto-sweep.ps1")
oEnv("SWEEP_SCRIPT") = sweepScript

command = "powershell.exe -NoLogo -NoProfile -ExecutionPolicy Bypass -WindowStyle Hidden -File """ & sweepScript & """"
oShell.Run command, 0, False

Set fso = Nothing
Set oShell = Nothing
WScript.Quit 0
