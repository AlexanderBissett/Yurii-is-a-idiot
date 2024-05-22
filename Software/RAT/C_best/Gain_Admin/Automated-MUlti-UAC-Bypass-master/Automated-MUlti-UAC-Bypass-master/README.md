
# Compile DLL
You can do it with the .ps1 or manual wit these one liners.
* output to working dir
`Add-Type -TypeDefinition ([IO.File]::ReadAllText("$pwd\sl0puacb.cs")) -ReferencedAssemblies "System.Windows.Forms" -OutputAssembly "sl0p.dll"`
* output to system 32
`Add-Type -TypeDefinition ([IO.File]::ReadAllText("$pwd\sl0puacb.cs")) -ReferencedAssemblies "System.Windows.Forms" -OutputAssembly "C:\Windows \system32\sl0p.dll`

# Setup
* `Set-ExecutionPolicy -ExecutionPolicy {Unrestricted or Bypass} -Scope CurrentUser`   
* Or use one of the bypasses like `type file.ps1 | poweshell.exe -no-profile` or what ever suites
* Add a automation process to disable tamper once uac been invoked (this can be done!!)  

# Setup 23h2 (see additional fixes, i've added automated fix, or you can do it manual like this below section.)
* Fetch the location of powershell.exe for either v2 or v7. 
* add a variable or make it auto check the exec location of powershell.exe
* add that dir to Start-Process {location}powershell.exe -Verb RunAs -ArgumentList ('-noprofile -noexit -file "{0}" -elevated' -f ($myinvocation.MyCommand.Definition))
* `Set-ExecutionPolicy -ExecutionPolicy {Unrestricted or Bypass} -Scope CurrentUser`   
* Or use one of the bypasses like `type file.ps1 | poweshell.exe -no-profile` or what ever suites
* Add a automation process to disable tamper once uac been invoked (this can be done!!) 
* run the ps1 file 

# Usage
* Download these files from either this repo directly if machine has inet capabilities. (Or download these files and serve them with python :D)
* Get the files on the system 
* cd to dir
* ./{File}.ps1



# Issues 
* Feel free to make issue ticket, if sum is not working, or support blocks missing.
* To assist me when creating a ticket, list ur windows version pulled with powershell and list it with the ticket. 