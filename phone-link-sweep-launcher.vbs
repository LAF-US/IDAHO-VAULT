Dim oShell, fso, scriptDir, launcher
Set oShell = CreateObject("WScript.Shell")
Set fso = CreateObject("Scripting.FileSystemObject")

scriptDir = fso.GetParentFolderName(WScript.ScriptFullName)
launcher = fso.BuildPath(scriptDir, "START-PHONE-LINK-SWEEP.cmd")

oShell.Run """" & launcher & """", 0, False

Set fso = Nothing
Set oShell = Nothing
WScript.Quit 0
