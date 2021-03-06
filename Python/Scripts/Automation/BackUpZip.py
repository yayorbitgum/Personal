# Automate the Boring Stuff, page 240 / 594.
# Copies an entire folder and its contents into a zip file,
#   with incremental naming.
#
# The project in the book simply increments numbers to show a new backup file.
# That would make actual backups really stupid trying to figure out which
#    backup is which, so I looked up timestamps on Google instead for that part.

# ///////////// Imports ////////////////////////////////////////////////////////
import zipfile
import os
import shutil
from datetime import datetime


# ///////////// Functions //////////////////////////////////////////////////////
def backup_to_zip(folder):
    """Back up entire contents of 'folder' into a zip file."""
    folder = os.path.abspath(folder)

    # --------------------------------------------------------------------------
    # Making a timestamp so archiving is simpler.
    # Timestamp formatting is too messy to be used for file name:
    #   (2020-09-19 18:00:50.263646), so I'll make my own.
    # I'll also add zeros to ensure each slot is at least 2 digits long so that
    #   sorting by file name works.
    now = datetime.now()
    timestamp = datetime.timestamp(now)
    time_format = datetime.fromtimestamp(timestamp)

    def add_a_zero(number):
        if len(str(number)) < 2:
            number = f"0{number}"
            return number
        else:
            return number

    year   = time_format.year
    month  = add_a_zero(time_format.month)
    day    = add_a_zero(time_format.day)
    hour   = add_a_zero(time_format.hour)
    minute = add_a_zero(time_format.minute)
    second = add_a_zero(time_format.second)

    time = f"{year}-{month}-{day} {hour}.{minute}.{second}"

    # Setting up the zip file name with an added timestamp.
    zip_name = f"{os.path.basename(folder)} {time}.zip"

    # --------------------------------------------------------------------------
    # Creating the zip file.
    print(f"Creating {zip_name}...")
    # Make zipfile object so we can use ZipFile functions.
    # This creates the actual file, but in the current .py script's location.
    backup_zip = zipfile.ZipFile(zip_name, 'x')
    print(f"Created {backup_zip}")

    # --------------------------------------------------------------------------
    # Walk the whole directory and compress the files in each folder with a
    #   for loop!
    for foldername, subfolders, filenames in os.walk(folder):

        print(f"Adding files in {foldername} to {zip_name}...")
        # Add the current folder.
        backup_zip.write(foldername)

        # Add all the files in that current folder.
        for filename in filenames:
            new_base = f"{os.path.basename(folder)} "

            # Don't backup the backup files lol.
            if filename.startswith(new_base) and filename.endswith('.zip'):
                print("Backup recursion avoided.")
                continue

            backup_zip.write(os.path.join(foldername, filename))
            print(f"Added {filename} to {zip_name}..")

    # --------------------------------------------------------------------------
    # Close the file.
    backup_zip.close()
    # Move the file from the root directory of this script to the location we zipped.
    shutil.move(zip_name, user_folder)

    print(f"\nZip complete! Check {folder}.\n")
    # Opens explorer here.
    os.startfile(folder)


# ///////////// Program ////////////////////////////////////////////////////////

# A little loop so you can enter your own folder path to backup, and restart
# input if the user fucked up.
# If they didn't fuck up, pass in the user's folder path into the zip function.
while True:
    user_folder = input('\nEnter folder path to backup: \n')

    if os.path.exists(user_folder) is False:
        print(f"{user_folder} doesn't exist. "
              f"Double check the path name. "
              f"Make sure you enter the entire file path of the folder you want to backup.")
        continue

    backup_to_zip(user_folder)
