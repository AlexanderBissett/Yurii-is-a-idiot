import subprocess

def RunPwsh(code):
    p = subprocess.run(['powershell', code], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
    return p.stdout.decode()

RunPwsh("cwd")