import subprocess
import time

while 1 :
    subprocess.call("TASKKILL /F /IM msedge.exe", shell=True)
    subprocess.call("TASKKILL /F /IM firefox.exe", shell=True)
    subprocess.call("TASKKILL /F /IM moffice.exe", shell=True)
    subprocess.call("TASKKILL /F /IM swriter.exe", shell=True)
    time.sleep(10)

 
