from textnode import TextNode, Text_Type
from enum import Enum

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