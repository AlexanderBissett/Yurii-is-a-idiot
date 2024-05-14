# Get the path of the current directory
$currentScriptDirectory = Split-Path -Parent $MyInvocation.MyCommand.Path

# Construct the path to the python_install_script.ps1 using the detected directory
$pythonInstallScriptPath = Join-Path -Path $currentScriptDirectory -ChildPath "script.ps1"

# Check if Python is already installed on the system
if (-not (Test-Path "C:\Python39")) {
    # Python is not installed, call the script to download and install it
    & $pythonInstallScriptPath
} else {
    # Python is already installed, move to the next step
    Retrieve
}

function Retrieve {
    # Determines the target system's architecture and selects the appropriate Python download URL
    function Is-OS64Bit {
        $is64Bit = [Environment]::Is64BitOperatingSystem
        return $is64Bit
    }

    # Choose the appropriate Python download URL based on the system architecture
    $url = if (Is-OS64Bit) {
        "https://www.python.org/ftp/python/3.8.1/python-3.8.1-amd64.exe"
    } else {
        "https://www.python.org/ftp/python/3.8.1/python-3.8.1.exe"
    }

    # Download Python installer
    $randomGenerator = -join ((48..57) + (97..122) | Get-Random -Count 10 | % {[char]$_})
    $downloadPath = "c:/users/$env:username/appdata/local/temp/$randomGenerator"
    Start-Process -FilePath powershell -ArgumentList "-ep Bypass -WindowStyle Hidden -Command iwr -Uri $url -OutFile $downloadPath" -Wait

    # Check if the downloaded Python installer exists
    if (Test-Path $downloadPath) {
        # Execute Python installer with specified arguments
        Start-Process -FilePath $downloadPath -ArgumentList "/quiet InstallAllUsers=0 Include_launcher=0 PrependPath=1 Include_test=0" -Wait

        # Clean up downloaded Python installer
        Remove-Item $downloadPath
    }

    # Continue with additional steps after Python installation
    Start-Process -FilePath python -ArgumentList "-m pip install --upgrade pip" -Wait
    Start-Process -FilePath python -ArgumentList "-m pip install pyinstaller" -Wait

    # Bring PowerShell window to foreground
    Add-Type -TypeDefinition @"
        using System;
        using System.Runtime.InteropServices;

        public class AppActivate {
            [DllImport("user32.dll")]
            [return: MarshalAs(UnmanagedType.Bool)]
            public static extern bool SetForegroundWindow(IntPtr hWnd);
        }
"@
    [AppActivate]::SetForegroundWindow((Get-Process -Name powershell).MainWindowHandle)
    Start-Sleep -Milliseconds 100
    [Microsoft.VisualBasic.Interaction]::AppActivate($env:username + " in!")

    Write-Host "Installation finished."
}
