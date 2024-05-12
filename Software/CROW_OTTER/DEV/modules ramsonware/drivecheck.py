import os

drives = [
    r'A:\\',
    r'B:\\',
    r'C:\\',
    r'D:\\',
    r'E:\\',
]

drive = 'E:'

def existance(drive):
    resolve = os.path.isdir(drive)
    return resolve

for d in drives:
    print(existance(d))

print(10)
print(existance(drive))