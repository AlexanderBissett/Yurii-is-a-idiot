import os

disk = 'I   :'


for x in os.listdir(disk):
    if os.path.exists(x):
        print(x)

for dirpath, dirnames, filenames in os.walk(disk):
    for filename in filenames:
        print(filename)