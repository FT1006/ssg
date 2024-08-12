from textnode import TextNode, Text_Type
from htmlnode import text_node_to_html_node


def main():
    node = TextNode("This is a text node", Text_Type.BOLD)
    html_node = text_node_to_html_node(node)
    print(html_node)


main()