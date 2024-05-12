import os
import shutil

threatAddress = r'C:\Users\udgo1\OneDrive\Escritorio\tdir'

# This moves al files to a directory made by us and creates the note in desktop.
Temp1 = fr'{threatAddress}\Hacked'                                # Create directory for storing the things in Desktop.
os.makedirs(Temp1)                                                  # Make it.

# This moves all of the files from desktop to the directory.
for file_name1 in os.listdir(threatAddress):                         # Scan the desktop.
    if 'Hacked' == file_name1:
            continue
    source1 = os.path.join(threatAddress, file_name1)                            # Join path with file name.
    destination1 = os.path.join(Temp1, file_name1)                               # Join new path with filename.     
    shutil.move(source1, destination1)                                           # Move it to directory.
