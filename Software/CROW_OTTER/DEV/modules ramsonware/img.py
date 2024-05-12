import os
import ctypes
import urllib.request

url = "https://github.com/AlexanderBissett/Yurii-is-a-idiot/raw/main/victim.png"
filename, headers = urllib.request.urlretrieve(url, filename="C:\\Users\\udgo1\\OneDrive\\Escritorio\\victim.png")
ctypes.windll.user32.SystemParametersInfoW(20, 0, r'C:\Users\udgo1\OneDrive\Escritorio\victim.png' , 0)