from textnode import *
from htmlnode import *
from block_md import *
from page_gen import *
    
import shutil
import os
import logging

from copy_source import copy_source_to_destination

destination = "./public"
source = "./static"

def main():
    print("Deleting old files...")
    if os.path.exists(destination): # if the destination directory exists, delete it
        shutil.rmtree(destination)

    print("Copying files...")
    copy_source_to_destination(source, destination)

    print("Generating pages...")
    generate_pages_recursive("./content", "./template.html", "./public")

main()