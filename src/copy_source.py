import shutil
import os
import logging

def copy_source_to_destination(source, destination):
    # Set up logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    if not os.path.exists(destination): # if the destination directory doesn't exist, create it
        os.makedirs(destination)
        
    # Copy all files and subdirectories
    for item in os.listdir(source): # iterate over all items in the source directory
        source_item = os.path.join(source, item) # get the full path of the current item
        destination_item = os.path.join(destination, item) # get the full path of the destination item
        
        if os.path.isdir(source_item):
            # If it's a directory, recursively call the function
            copy_source_to_destination(source_item, destination_item)
        else:
            # If it's a file, copy it
            shutil.copy(source_item, destination_item) # copy the file
            logging.info(f"Copied {source_item} to {destination_item}") # log the action