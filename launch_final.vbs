Set WshShell = CreateObject("WScript.Shell")
Set objFSO = CreateObject("Scripting.FileSystemObject")

' Get the directory where this script is located
strScriptPath = objFSO.GetParentFolderName(WScript.ScriptFullName)
strExePath = strScriptPath & "\dist\CS2-Ping-Monitor.exe"

' Check if the executable exists
If objFSO.FileExists(strExePath) Then
    ' Launch the application completely hidden
    WshShell.Run """" & strExePath & """", 0, False
Else
    ' Show error if executable not found
    MsgBox "CS2-Ping-Monitor.exe not found in dist folder!", vbCritical, "Error"
End If
