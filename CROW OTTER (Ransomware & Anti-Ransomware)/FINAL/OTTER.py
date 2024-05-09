#  This is OTTER (Operation to Terminate Threats, Erase Ransomware) a decryption software that is designed 
#  to deecrypt files encrypted by a malware called CROW.
#  It works the following way:

#  First it will go to the desktop and take out all of the files that CROW put in the 'hacked' directory. 
#  Second it will open a list of encrypted files and their locations when they were encrypted, later it
#  will extract the encryption key that was stenographicaly inserted in the image that we use as background, 
#  and after that it will create a counter of files decrypted and ask for a password, if the password is correct 
#  it will start the decryption loop that reads the files in the list and uses the key to decrypt them.

#  After all of this is done it will locate the threat file that CROW left in the desktop and delete it.
#  Then it will create a "Thank you" file and put it in the desktop as well.
#  To end the decryption software will delete all files and directories created by CROW and restore the wallpaper,
#  as well as restarting the computer.

### THE CODE STARTS HERE ###

# Necesary imports.
import os
import shutil
import sys
import ctypes
import png
import base64
import os.path 
import time
from cryptography.fernet import Fernet

# Declares THE START OF TIME.
start = time.time()

ENDOFMESSAGE = "0100100101010101010101100100111101010010010001010011100101000111010101000101010101010110010101000101010100110000010001100100100001010010010100110100010100111101"

def encode_message_as_bytestring(message):
	b64 = message.encode("utf8")
	bytes_ = base64.encodebytes(b64)
	bytestring = "".join(["{:08b}".format(x) for x in bytes_])
	bytestring += ENDOFMESSAGE
	return bytestring

def get_pixels_from_image(fname):
	img = png.Reader(fname).read()
	pixels = img[2]
	return pixels

def encode_pixels_with_message(pixels, bytestring):
	'''modifies pixels to encode the contents from bytestring'''

	enc_pixels = []
	string_i = 0
	for row in pixels:
		enc_row = []
		for i, char in enumerate(row):
			if string_i >= len(bytestring): 
				pixel = row[i]
			else:
				if row[i] % 2 != int(bytestring[string_i]):
					if row[i] == 0:
						pixel = 1
					else:
						pixel = row[i] - 1
				else:
					pixel = row[i]
			enc_row.append(pixel)
			string_i += 1

		enc_pixels.append(enc_row)
	return enc_pixels

def write_pixels_to_image(pixels, fname):
	png.from_array(pixels, 'RGB').save(fname)

def decode_pixels(pixels):
	bytestring = []
	for row in pixels:
		for c in row:
			bytestring.append(str(c % 2))
	bytestring = ''.join(bytestring)
	message = decode_message_from_bytestring(bytestring)
	return message

def decode_message_from_bytestring(bytestring):
	bytestring = bytestring.split(ENDOFMESSAGE)[0]
	message = int(bytestring, 2).to_bytes(len(bytestring) // 8, byteorder='big')
	message = base64.decodebytes(message).decode("utf8")
	return message

# This will find the users.
def findUsers(directory):
    users = []          
    # Scan the users that exist inside of C:\Users.                                                         
    for f in os.scandir(directory):                                                
        if f.name[0].isalpha() and f.is_dir() and not f.name == 'Default User' and not f.name == 'All Users' and not f.name == 'Default' and not f.name == 'Public':     
            users.append(f.path)                                                
    return users                                                           

# This will find the desktops of every user.
def findDesktops(users, desk_sys):
    desktops = []                                                  
    for user in users:                                           
        for target in desk_sys:                             
            join = os.path.join(user, target)                     
            desktops.append(join)                           
    return desktops

# This will find the dektop and restore the files to it as well as replathin the threat with a thank you note.
def desktop_mv(threatAddress):

    # This writtes the contents of the "Thank you" note that will be left in the victims desktop.
    contents = 'Muchas gracias por cooperar con nosotros. \n\
Esperamos de todo corazon que se lo hayan pasado tan bien como nosotros en este ciberataque. \n\
Que tengan un buen dia y recordad, la seguridad es lo mas importante. Un abrazo.'

    # Define location of Hacked folder in desktop and the desktop.
    hacked = fr'{threatAddress}\Infectado'

    # Checks where the desktop actually exists 
    if os.path.isdir(threatAddress):
        # This moves all of the files from Hacked to the Desktop.
        for file_name1 in os.listdir(hacked):                            
            source1 = os.path.join(hacked, file_name1)                
            destination1 = os.path.join(threatAddress, file_name1)        
            shutil.move(source1, destination1)                       

        # Deletes the threat note.
        del_note = fr'{threatAddress}\INSTRUCCIONES_DEL_ATAQUE.txt'
        if os.path.isfile(del_note):
            os.remove(del_note)
        
        # This writes the "Thank you" note. 
        with open(fr'{threatAddress}\AGRADECIMIENTO.txt', 'w') as f:
            f.write(contents)
        
        # Remove directory that we used to store desktop files.
        os.rmdir(hacked)
			
# Starts decryption process.
def decrypter():

    # Opens the list and reads the individual lines.
    with open(r'C:\Program Files (x86)\Microsoft Calendar\Calendar Mail\Import Tool\bin\10.0.17134.0\x86\ConfigListTracker.txt') as f:
        files = f.read().splitlines()
    
    # Gets the image where the key is stored
    in_image = r'C:\Program Files (x86)\Microsoft Calendar\Calendar Mail\Import Tool\bin\10.0.15063.0\x64\jytrhd.png'
    pixels = get_pixels_from_image(in_image + "D.png")
    text = decode_pixels (pixels)
    # Extracts the key
    key = text.encode('ascii')

    count = 0
    for file in files:
        with open (file, 'rb') as f:                      
            content_encripted = f.read()
        if 0 == count%50:                                  
                print(f'Files Cured {count}')
        content = Fernet(key).decrypt(content_encripted)    
        with open (file, 'wb') as f:                 
            f.write(content)
        count += 1         

    # Gives feedback of how many files have been decrypted.
    print (f'{count}')

 # This leaves the computer as it was before being attacked by ana4.
def cleaner():
    # Defines the route of the fake directory tree.
    fake_tree = r'C:\Program Files (x86)\Microsoft Calendar'
    # Deletes the fake tree and everything inside it.
    shutil.rmtree(fake_tree)

    # Restores original windows background. (We could put back the one they had, but they are lucky we give them this.)
    ctypes.windll.user32.SystemParametersInfoW(20, 0, r'C:\Windows\Web\Wallpaper\Windows\img0.jpg' , 3)

def lana():
    
    # Defines the password.
    codeword = '8569efc4ed5a6273140c2b6ec0ab8d99f4398210808fbb7c0cbbae4fbcc21350'
    # Asks for the password.
    user_phrase = input('Palabra clave: ')

    # List of all posible locations for the desktop.
    desk_sys = [
    r'Desktop\\',
    r'OneDrive\Desktop\\',
    r'Escritorio\\',
    r'OneDrive\Escritorio\\'
    ]

    # This tells the malware were the users are in windows.
    directory = r'C:\Users'
    users = findUsers(directory)

    # Gets the full addresses for desktop posibilities.
    desktops = findDesktops(users, desk_sys)

    # This is the decryption loop. If the password was correct it will start.
    if user_phrase == codeword:

        # Loop that goes through the options for the possible locations of desktop.
        for options in desktops:
            desktop_mv(options)
	
	# Calls the Decypter module.
        decrypter()

	# Calls the Cleaner moudle.
        cleaner()

        # Declares THE END OF TIME.
        end = time.time()

        # Print how long the code took to run.
        print (end-start)

        # Wait 5 seconds.
        time.sleep (5)

        # This reestarts the computer at the end of the attack, this is done mainly to anoy.
        os.system("shutdown -r -t 1")

    # If the password was incorrect it will close the decrypter.
    else :
        print ("Wrong!")
        sys.exit()

lana()
