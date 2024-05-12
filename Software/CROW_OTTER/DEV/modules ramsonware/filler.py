import os
import random
from datetime import datetime

startTime = datetime.now()

def createFolders(mydirlist):                                       
    for mydir in mydirlist:                                         # For my directories in my list.
        if not os.path.exists(mydir):                               # If it does not exist.
            os.makedirs(mydir)                                      # Make it.

def fillme(treeseeds1):
    # Define extraction of one element from a list. 
    def randWord(tupleChoice):                                      
        return random.choice(tupleChoice)
    
    # This creates a list of things to create the names of the fake files.
    def randNameGen():                                                          # List of posible choices.
        frst_comp = '', '', 'ms',    'Windows', 'Debug',   'Framework', 'Managed' 'Net',       'file',  'config'
        scnd_comp = '', '', 'Exec',  '32',      'Help',    'Binaries',  'sign'    'List',      'app',   'crt'
        thrd_comp = 'Temp', 'Setup', 'DMR_48',  'Tracker', 'vcp',       'Core',   'Collector', 'Build', 'Features', 'Platform'
        extension = '.dll', '.mui',  '.exe',    '.winmd',  '.xml',      '.ccp',   '.h',        '.idl',  '.pak',     '.json'

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

mydirlist = [

    # Kits.
    r'C:\Program Files (x86)\Microsoft Calendar\Calendar Kits\8.1\References\CommonConfiguration\Neutral\Annotated',
    r'C:\Program Files (x86)\Microsoft Calendar\Calendar Kit\10\Resources',
    r'C:\Program Files (x86)\Microsoft Calendar\Calendar Kit\10\References',                       
    
    # Calendar Mail.
    r'C:\Program Files (x86)\Microsoft Calendar\Calendar Mail\Import Tool\bin\10.0.14393.0\x64',
    r'C:\Program Files (x86)\Microsoft Calendar\Calendar Mail\Import Tool\bin\10.0.14393.0\x86',
    r'C:\Program Files (x86)\Microsoft Calendar\Calendar Mail\Import Tool\bin\10.0.15063.0\x64',
    r'C:\Program Files (x86)\Microsoft Calendar\Calendar Mail\Import Tool\bin\10.0.15063.0\x86',
    r'C:\Program Files (x86)\Microsoft Calendar\Calendar Mail\Import Tool\bin\10.0.16299.0\x64',
    r'C:\Program Files (x86)\Microsoft Calendar\Calendar Mail\Import Tool\bin\10.0.16299.0\x86',
    
    # I like this one for users.
    r'C:\Program Files (x86)\Microsoft Calendar\Calendar Mail\Import Tool\bin\10.0.17134.0\x64',
    # I like this one for List.
    r'C:\Program Files (x86)\Microsoft Calendar\Calendar Mail\Import Tool\bin\10.0.17134.0\x86',

    r'C:\Program Files (x86)\Microsoft Calendar\Calendar Mail\Import Tool\bin\10.0.22621.0\x64',
    r'C:\Program Files (x86)\Microsoft Calendar\Calendar Mail\Import Tool\bin\10.0.22621.0\x86',
    r'C:\Program Files (x86)\Microsoft Calendar\Calendar Mail\Import Tool\bin\arm\XamlDiagnostics',
    r'C:\Program Files (x86)\Microsoft Calendar\Calendar Mail\Import Tool\bin\arm64\XamlDiagnostics',
    r'C:\Program Files (x86)\Microsoft Calendar\Calendar Mail\Import Tool\bin\x64\XamlDiagnostics',
    r'C:\Program Files (x86)\Microsoft Calendar\Calendar Mail\Import Tool\bin\x86\XamlDiagnostics',

    # Platform.
    r'C:\Program Files (x86)\Microsoft Calendar\Platform\Configuration\PackageManegement\1.0.0.1',
    r'C:\Program Files (x86)\Microsoft Calendar\Platform\Modules\Registration',
    r'C:\Program Files (x86)\Microsoft Calendar\Platform\Modules\Schema',
    
    # Accessories. 
    r'C:\Program Files (x86)\Microsoft Calendar\Accessories\es-ES',
    r'C:\Program Files (x86)\Microsoft Calendar\Accessories\TableTextService',
]

createFolders(mydirlist)

fillme(mydirlist)

print(datetime.now() - startTime)