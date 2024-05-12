import string
from ctypes import windll
import win32api

def get_drives():
    drives = []
    bitmask = windll.kernel32.GetLogicalDrives()
    for letter in string.ascii_uppercase:
        if bitmask & 1:
            drives.append(letter)
        bitmask >>= 1

    return drives

if __name__ == '__main__':
    drive_list = get_drives()
    print(drive_list)
    for letter in drive_list:
        winlet = f'{letter}:\\' 
        finfo = win32api.GetVolumeInformation(winlet)
        infoname = finfo[0]
        print(winlet, infoname)