from textnode import *
from enum import Enum
import re

def split_nodes_delimiter(old_nodes, delimiter, text_type: Text_Type):
    # Ensure all items in old_nodes are TextNode instances
    if not all(isinstance(node, TextNode) for node in old_nodes):
        raise TypeError("All items in old_nodes must be TextNode instances")
    new_nodes = []
    for node in old_nodes:
        if node.text_type == Text_Type.TEXT:
            node_split = node.text.split(delimiter)
            i = 0
            for item in node_split:
                if i % 2 == 0:
                    new_nodes.append(TextNode(item, Text_Type.TEXT))
                else:
                    new_nodes.append(TextNode(item, text_type))
                i += 1
        else:
            new_nodes.append(node)
    return new_nodes

def extract_markdown_images(text):
    # Ensure text is a string
    if not isinstance(text, str):
        raise TypeError("Input must be a string")
    image_pattern = r"!\[(.*?)\]\((.*?)\)"
    matched_images = re.findall(image_pattern, text)
    return matched_images

def extract_markdown_links(text):
    # Ensure text is a string
    if not isinstance(text, str):
        raise TypeError("Input must be a string")
    regular_link_pattern = r"(?<!!)\[(.*?)\]\((.*?)\)"
    matched_links = re.findall(regular_link_pattern, text)
    return matched_links

def split_nodes_image(old_nodes):
    # Ensure all items in old_nodes are TextNode instances
    if not all(isinstance(node, TextNode) for node in old_nodes):
        raise TypeError("All items in old_nodes must be TextNode instances")
    new_nodes = []
    for node in old_nodes:
        # If the node is not a TextNode instance, add it to the new nodes
        if node.text_type is not Text_Type.TEXT:
            new_nodes.append(node)
            continue
        processing_node = node.text
        image_list = extract_markdown_images(processing_node)
        # For each image in the list, split the processing node at the image
        for image in image_list:
            sections = processing_node.split(f"![{image[0]}]({image[1]})", 1)
            # If the image section is not closed, raise an error
            if len(sections) != 2:
                raise ValueError("Invalid markdown, image section not closed")
            # If the text before the image is not empty, add it to the new nodes
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], Text_Type.TEXT))
            new_nodes.append(TextNode(image[0], Text_Type.IMAGE, image[1]))
            processing_node = sections[1]
        # If the processing node is not empty, add it to the new nodes
        if processing_node != "":
            new_nodes.append(TextNode(processing_node, Text_Type.TEXT))
    return new_nodes

def split_nodes_link(old_nodes):
    # Ensure all items in old_nodes are TextNode instances
    if not all(isinstance(node, TextNode) for node in old_nodes):
        raise TypeError("All items in old_nodes must be TextNode instances")
    new_nodes = []
    for node in old_nodes:
        # If the node is not a TextNode instance, add it to the new nodes
        if node.text_type is not Text_Type.TEXT:
            new_nodes.append(node)
            continue
        processing_node = node.text
        link_list = extract_markdown_links(processing_node)
        # For each link in the list, split the processing node at the link
        for link in link_list:
            sections = processing_node.split(f"[{link[0]}]({link[1]})", 1)
            # If the link section is not closed, raise an error
            if len(sections) != 2:
                raise ValueError("Invalid markdown, link section not closed")
            # If the text before the link is not empty, add it to the new nodes
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], Text_Type.TEXT))
            new_nodes.append(TextNode(link[0], Text_Type.LINK, link[1]))
            processing_node = sections[1]
        # If the processing node is not empty, add it to the new nodes
        if processing_node != "":
            new_nodes.append(TextNode(processing_node, Text_Type.TEXT))
    return new_nodes

def text_to_textnodes(text):
    """
    This function takes a string of text and converts it into a list of TextNode instances.
    It first creates a single TextNode instance for the entire text.
    Then it splits the text at each delimiter in the order of '![', '[', '**', '*', and '`'.
    The order of splitting is important to ensure that images and links are processed before text formatting.
    This is because images and links can contain text that might be mistakenly interpreted as formatting delimiters.
    For example, an image URL might contain '**' or '*', which could be mistaken for bold or italic formatting.
    By processing images and links first, we ensure that these delimiters are correctly identified as part of the image or link.
    After processing images and links, the function splits the text at '**' for bold formatting, then '*', then '`' for code blocks.
    For each split, it creates a new TextNode instance with the appropriate text type.
    Finally, it returns the list of TextNode instances.
    """
    if not isinstance(text, str):
        raise TypeError("Input must be a string")
    nodes = [TextNode(text, Text_Type.TEXT)]
    print(nodes)
    nodes = split_nodes_image(nodes)
    print(nodes)
    nodes = split_nodes_link(nodes)
    print(nodes)
    nodes = split_nodes_delimiter(nodes, "**", Text_Type.BOLD)
    print(nodes)
    nodes = split_nodes_delimiter(nodes, "*", Text_Type.ITALIC)
    print(nodes)
    nodes = split_nodes_delimiter(nodes, "`", Text_Type.CODE)
    print(nodes)
    return nodes