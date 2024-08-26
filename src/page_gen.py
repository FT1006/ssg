from htmlnode import *
from block_md import *

import os

def extract_title(markdown):
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        if block_to_block_type(block) == Block_Type.HEADING:
            if heading_to_html_node(block).tag == "h1":
                return heading_to_html_node(block).children[0].value # return = break?
    else: # if no title is found, raise an exception
        raise Exception("No title found in markdown")

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using template {template_path}")
    with open(from_path, "r") as f:
        md = f.read()
    with open(template_path, "r") as f:
        temp = f.read()
    html = markdown_to_html_node(md)
    title = extract_title(md)

    # Debug prints to check values
    print(f"Extracted Title: {title}")
    print(f"Generated HTML: {html.to_html()}")

    # Replace the title in the template
    temp = temp.replace("{{ Title }}", title)
    
    # Replace the content in the template
    temp = temp.replace("{{ Content }}", html.to_html())
    
    print(f"Generated HTML: {temp}")

    # Write the generated page to the destination
    with open(dest_path, "w") as f: # write the template to the file
        f.write(temp)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    print(f"Generating pages from {dir_path_content} to {dest_dir_path} using template {template_path}")
    
    # loop through all files in the content directory
    for file in os.listdir(dir_path_content):
        # get the source and destination paths for the current file
        source_file_path = os.path.join(dir_path_content, file)
        dest_file_path = os.path.join(dest_dir_path, file)

        # if the current file is an .md file, generate the corresponding HTML page
        if file.endswith(".md"):
            print(f"A .md file found: {source_file_path}")
            generate_page(source_file_path, template_path, dest_file_path.replace(".md", ".html")) 
        # if the current file is a directory, recursively generate the corresponding HTML pages
        elif os.path.isdir(source_file_path):
            os.makedirs(dest_file_path, exist_ok=True) # create the destination directory if it doesn't exist
            generate_pages_recursive(source_file_path, template_path, dest_file_path)
