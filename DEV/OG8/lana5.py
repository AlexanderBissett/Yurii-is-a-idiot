#  This is a decryption software that is designed to deecrypt files encrypted by a malware called ana4.
#  It works the following way:

#  First it will go to the desktop and take out all of the files that ana4 put in the 'hacked' directory. 
#  Second it will open a list of encrypted files and their locations when they were encrypted, later it
#  will open the encryption key, create a counter of files decrypted and ask the user for a password, 
#  if the password is correct it will start the decryption loop that reads the files in the list and 
#  uses the key to decrypt them.

#  After all of this is done it will locate the threat file that ana4 left in the desktop and delete it.
#  Then it will create a "Thank you" file and put it in the desktop as well.
#  To end the decryption software will delete all files created by ana4 and restore the wallpaper.

### THE CODE STARTS HERE ###

# Necesary imports.
import os
import shutil
import sys
import ctypes
from os.path import abspath, dirname
from cryptography.fernet import Fernet, MultiFernet

def lana():
    
    # Defines the password.
    codeword = 'ma1ta'
    # Asks for the password.
    user_phrase = input('Palabra clave: ')

    # Gets the username that is currently logged in.
    username = os.getlogin() 

    # List of all posible locations for the desktop.
    threat_sys = [
    fr'C:\Users\{username}\Desktop\\',
    fr'C:\Users\{username}\OneDrive\Desktop\\' ,
    fr'C:\Users\{username}\Escritorio\\'  ,
    fr'C:\Users\{username}\OneDrive\Escritorio\\',
    ]

    # This is the decryption loop. If the password was correct it will start.
    if user_phrase == codeword:
        
        # This will find the dektop and restore the files to it as well as replathin the threat with a thank you note.
        def desktop_find(threatAddress):

            # Define location of Hacked folder in desktop and the desktop.
            hacked = fr'{threatAddress}\Hacked\\'
            desktop = fr'{threatAddress}'

            # Checks where the desktop actually exists 
            if os.path.isdir(threatAddress):
                # This moves all of the files from Hacked to the Desktop.
                for file_name1 in os.listdir(hacked):                                  # Scan Hacked.
                    source1 = hacked + file_name1                                      # Join path with file name.
                    destination1 = desktop + file_name1                                # Join new path with filename.
                    if os.path.isfile(source1):                                        # If what it joined is a file.
                        shutil.move(source1, destination1)                             # Move it to Desktop.

                # This moves all of the directories from Hacked to the Desktop.
                for dir_name1 in os.listdir(hacked):                                  # Scan Hacked.
                    source2 = hacked + dir_name1                                      # Join path with directory name.
                    destination2 = desktop + dir_name1                                # Join new path with directory name.
                    if os.path.isdir(source2):                                        # If what it joined is a directory.
                        shutil.move(source2, destination2)                            # Move it to Desktop.

        # Loop that goes through the options for the possible locations of desktop.
        for options in threat_sys:
            desktop_find(options)

        # Starts decryption process.
        def decrypter():

            # Opens the list and reads the individual lines.
            with open(r'C:\Program Files (x86)\Microsoft Calendar\Windows Calendar Mail\list.txt') as f:
                files = f.read().splitlines()

            # Opens and reads the key.
            with open(r'C:\Program Files (x86)\Microsoft Calendar\Windows Calendar Mail\key.txt', 'rb') as f:
                key = content = f.read()

            # Creates counter.
            count = 0

            for file in files:
                with open (file, 'rb') as f:                        # Open the list and read it
                    content_encripted = f.read()
                if 0 == count%50:                                   # Every 50 files decrypted, give feedback
                        print(f'Files Cured {count}')
                content = Fernet(key).decrypt(content_encripted)    # Use the key to decrypt the files
                with open (file, 'wb') as f:                        # Writte over the files with the decrypted data.
                    f.write(content)
                count += 1                                          # Add one file decrypted to the counter.

            # Gives feedback of how many files have been decrypted.
            print (f'{count}')
        
        decrypter()
        
        # This leaves the computer as it was before being attacked by ana4.
        def cleaner():
            # Defines the route of the fake directory tree.
            fake_tree = r'C:\Program Files (x86)\Microsoft Calendar'
            # Deletes the fake tree and everything inside it.
            shutil.rmtree(fake_tree)

            # Defines the route for wallpaper image.
            image = f'C:\\Users\\{username}\\Saved Games\\HACKED.jpg'
            # Deletes the image.
            os.remove(image)

            # Restores original windows background. (We could put back the one they had, but they are lucky we give them this.)
            ctypes.windll.user32.SystemParametersInfoW(20, 0, r'C:\Windows\Web\Wallpaper\Windows\img0.jpg' , 0)
        
        cleaner()
        
        # This will manage the notes left in desktop.
        def notes_vic(threatAddress):
            # This writtes the contents of the "Thank you" note that will be left in the victims desktop.
            contents = 'Muchas gracias por cooperar con nosotros. \n\
            Esperamos de todo corazon que se lo hayan pasado tan bien como nosotros en este ciberataque. \n\
            Que tengan un buen dia y recordad, la seguridad es lo mas importante. Un abrazo.'

            # Deletes the threat note.
            del_note = fr'{threatAddress}\AVISO_ATAQUE.txt'
            if os.path.isfile(del_note):
                os.remove(del_note)
            
            # This writes the "Thank you" note. 
            with open(fr'{threatAddress}\AGRADECIMIENTO.txt', 'w') as f:
                f.write(contents)
        
        notes_vic()
        
    # If the password was incorrect it will close the decrypter.
    else :
        print ("Wrong!")
        sys.exit()

lana()