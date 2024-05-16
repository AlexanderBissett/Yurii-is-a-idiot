import subprocess
import sys
p = subprocess.Popen('powershell.exe -ExecutionPolicy RemoteSigned -file "UACI.ps1"', stdout=sys.stdout)
p.communicate()