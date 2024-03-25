#  This is a decryption software that is designed to deecrypt files encrypted by a malware called ana3.
#  It works the following way:

#  First it will open a list of encrypted files and their locations when they were encrypted, later it
#  will open the encryption key, create a counter of files decrypted and ask the user for a password, 
#  if the password is correct it will start the decryption loop that reads the files in the list and 
#  uses the key to decrypt them.

#  After all of this is done it will locate the threat file that ana3 left in the desktop and delete it.
#  Then it will create a "Thank you" file and put it in the desktop as well.
#  To end the decryption software will delete the fake directory tree created by ana3.

### THE CODE STARTS HERE ###

# Necesary imports.
import os
from os.path import abspath, dirname
import shutil
from cryptography.fernet import Fernet, MultiFernet
import sys

# Opens the list and reads the individual lines.
with open(r'C:\Program Files (x86)\Microsoft Agenda\Windows Agenda Mail\list.txt') as f:
    files = f.read().splitlines()

# Opems and reas the key.
with open(r'C:\Program Files (x86)\Microsoft Agenda\Windows Agenda Mail\key.txt', 'rb') as f:
    key = content = f.read()

# Defines the password.
codeword = 'ma1ta'

# Asks for the password.
user_phrase = input('Palabra clave: ')

# Creates counter.
count = 0

# This is the decryption loop. If the password was correct it will start
if user_phrase == codeword:
    for file in files:
        with open (file, 'rb') as f:                        # Open the list and read it
            content_encripted = f.read()
        if 0 == count%50:                                   # Every 50 files decrypted, give feedback
                print(f'Files Cured {count}')
        content = Fernet(key).decrypt(content_encripted)    # Use the key to decrypt the files
        with open (file, 'wb') as f:                        # Writte over the files with the decrypted data.
            f.write(content)
        count += 1                                          # Add one file decrypted to the counter.

# If the password was incorrect it will close the decrypter.
else :
    print ("Wrong!")
    sys.exit()

# Gives feedback of how many files have been decrypted.
print (f'{count}')

# Gets the username that is currently logged in.
username = os.getlogin() 

# Defines the two posibilities of where the desktop is.
threatAddress1 = fr'C:\Users\{username}\Desktop'
threatAddress2 = fr'C:\Users\{username}\OneDrive\Desktop'

# Deletes the threat note in the case that the desktop is not inside of OneDrive.
eliminar1 = fr'{threatAddress1}\AVISO_ATAQUE.txt'
if os.path.isfile(eliminar1):
    os.remove(eliminar1)

# Deletes the threat note in the case that the desktop is inside of OneDrive.
eliminar2 = fr'{threatAddress2}\AVISO_ATAQUE.txt'
if os.path.isfile(eliminar2):
    os.remove(eliminar2)

# This writtes the "Thank you" note that will be left in the victims desktop.
contents = 'Muchas gracias por cooperar con nosotros. \n\
Esperamos de todo corazon que se lo hayan pasado tan bien como nosotros en este ciberataque. \n\
Que tengan un buen dia y recordad, la seguridad es lo mas importante. Un abrazo.'

# This checks if the desktop is not in OneDrive and writes the "Thank you" note.
if os.path.isdir(threatAddress1):
    with open(fr'{threatAddress1}\AGRADECIMIENTO.txt', 'w') as f:
        f.write(contents)

# This checks if the desktop is in OneDrive and writes the "Thank you" note.
if os.path.isdir(threatAddress2):
    with open(fr'{threatAddress2}\AGRADECIMIENTO.txt', 'w') as f:
        f.write(contents)

# Defines the route of the fake directory tree.
eliminar3 = r'C:\Program Files (x86)\Microsoft Agenda'

# Deletes the fake tree and everything inside it.
shutil.rmtree(eliminar3)
