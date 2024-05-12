import os
import shutil
sourceAddress = r'C:\Users\udgo1\OneDrive\Escritorio\tdir\Hacked'

# This moves al files to a directory made by us and creates the note in desktop.
Destination = r'C:\Users\udgo1\OneDrive\Escritorio\tdir'                             # Create directory for storing the things in Desktop.

# This moves all of the files from desktop to the directory.
for file_name1 in os.listdir(sourceAddress):                         # Scan the desktop.
   
    source1 = os.path.join(sourceAddress, file_name1)                            # Join path with file name.
    destination1 = os.path.join(Destination, file_name1)                               # Join new path with filename.     
    shutil.move(source1, destination1)                                           # Move it to directory.
