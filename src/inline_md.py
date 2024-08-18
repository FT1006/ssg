from textnode import TextNode, Text_Type
from enum import Enum
import re

def split_nodes_delimiter(old_nodes, delimiter, text_type: Text_Type):
    if not isinstance(delimiter, str):
        raise TypeError("Delimiter must be a string")
    
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
    if not isinstance(text, str):
        raise TypeError("Input must be a string")
    image_pattern = r"!\[(.*?)\]\((.*?)\)"
    matched_images = re.findall(image_pattern, text)
    return matched_images

def extract_markdown_links(text):
    if not isinstance(text, str):
        raise TypeError("Input must be a string")
    regular_link_pattern = r"(?<!!)\[(.*?)\]\((.*?)\)"
    matched_links = re.findall(regular_link_pattern, text)
    return matched_links

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if not isinstance(node, TextNode) or node.text_type != Text_Type.TEXT:
            raise TypeError("Node must be a TextNode instance with text_type set to Text_Type.TEXT")
        if node.text_type != Text_Type.TEXT:
            new_nodes.append(node)
            continue
        image_list = list(extract_markdown_images(node.text))
        processing_node = node.text
        for image in image_list:
            sections = processing_node.split(f"![{image[0]}]({image[1]})", 1)
            if len(sections) != 2:
                raise ValueError("Invalid markdown, image section not closed")
            new_nodes.append(TextNode(image[0], Text_Type.IMAGE, image[1]))
            processing_node = sections[1]
        if processing_node != "":
            new_nodes.append(TextNode(processing_node, Text_Type.TEXT))
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if not isinstance(node, TextNode) or node.text_type != Text_Type.TEXT:
            raise TypeError("Node must be a TextNode instance with text_type set to Text_Type.TEXT")
        if node.text_type != Text_Type.TEXT:
            new_nodes.append(node)
            continue
        link_list = list(extract_markdown_links(node.text))
        processing_node = node.text
        for link in link_list:
            sections = processing_node.split(f"[{link[0]}]({link[1]})", 1)
            if len(sections) != 2:
                raise ValueError("Invalid markdown, link section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], Text_Type.TEXT))
            new_nodes.append(TextNode(link[0], Text_Type.LINK, link[1]))
            processing_node = sections[1]
        if processing_node != "":
            new_nodes.append(TextNode(processing_node, Text_Type.TEXT))
    return new_nodes

def text_to_textnodes(text):
    if not isinstance(text, str):
        raise TypeError("Input must be a string")
    input_node = TextNode(
        text,
        Text_Type.TEXT,
    )
    code_nodes = split_nodes_delimiter(input_node, "`", Text_Type.CODE)
    image_nodes = split_nodes_image(code_nodes)
    link_nodes = split_nodes_link(image_nodes)
    bold_nodes = split_nodes_delimiter(link_nodes, "**", Text_Type.BOLD)
    italic_nodes = split_nodes_delimiter(bold_nodes, "*", Text_Type.ITALIC)
    return italic_nodes