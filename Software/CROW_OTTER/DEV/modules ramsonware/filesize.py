import os

file_name = r'C:\Users\udgo1\Downloads\jytrhd.png'
exten = os.path.splitext(file_name)[-1]

file_stats = os.stat(file_name)
fsize = file_stats.st_size
size_mb = fsize / (1024 * 1024)

sz_mb = os.path.getsize(file_name) 

print(exten)

print(f'File Size in MegaBytes is {size_mb}')
