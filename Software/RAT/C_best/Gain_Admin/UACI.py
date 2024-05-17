import subprocess

def run(cmd):
    completed = subprocess.run(["powershell", "-Command", cmd], capture_output=True)
    return completed

hello_command = """mkdir C:\\d
Write-Host 'Hello Wolrd!'"""
hello_info = run(hello_command)

if hello_info.returncode != 0:
    print(f"Error - {hello_info.stderr}")
else:
    print("Executed successfully!")