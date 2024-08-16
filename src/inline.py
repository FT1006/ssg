from textnode import TextNode, Text_Type
from enum import Enum
import re

def split_nodes_delimiter(old_nodes, delimiter, text_type: Text_Type):
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
    image_pattern = r"!\[(.*?)\]\((.*?)\)"
    matched_images = re.findall(image_pattern, text)
    return matched_images

def extract_markdown_links(text):
    regular_link_pattern = r"(?<!!)\[(.*?)\]\((.*?)\)"
    matched_links = re.findall(regular_link_pattern, text)
    return matched_links

text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
print(extract_markdown_images(text))
# [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")]

text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
print(extract_markdown_links(text))
# [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")]