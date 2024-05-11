Dim WShell
Set WShell = CreateObject("WScript.Shell")
WShell.Run "C:\%HOMEPATH%\R.exe", 0
Set WShell = Nothing