from enum import Enum
from textnode import TextNode, Text_Type
from block_md import *
from inline_md import *

class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("to_html method not implemented")

    def props_to_html(self):
        if self.props is None:
            return ""
        props_html = ""
        for prop in self.props:
            props_html += f' {prop}="{self.props[prop]}"'
        return props_html

    def __repr__(self):
        return f"HTMLNode(tag: {self.tag}, value: {self.value}, children: {self.children}, props: {self.props})"

    def text_node_to_html_node(text_node):
        return LeafNode(None, text_node)

    def __eq__(self, other):
        if not isinstance(other, HTMLNode):
            return False
        return (self.tag == other.tag and
            self.value == other.value and
            self.children == other.children and
            self.props == other.props)

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError("Invalid HTML: no value")
        if self.tag is None:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    def __repr__(self):
        return f"LeafNode(tag: {self.tag}, value: {self.value}, props: {self.props})"

    def __eq__(self, other):
        if not isinstance(other, LeafNode):
            return False
        return (self.tag == other.tag and
            self.value == other.value and
            self.props == other.props)

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("Invalid HTML: no tag")
        if self.children is None:
            raise ValueError("Invalid HTML: no children")
        children_html = ""
        for child in self.children:
            children_html += child.to_html()
        return f"<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>"

    def __repr__(self):
        return f"ParentNode(tag: {self.tag}, children: {self.children}, props: {self.props})"

    def __eq__(self, other):
        if not isinstance(other, ParentNode):
            return False
        return (self.tag == other.tag and
            self.children == other.children and
            self.props == other.props)

def text_node_to_html_node(text_node):
    if not isinstance(text_node, TextNode):
        raise TypeError("Input must be a TextNode instance")
    match text_node.text_type:
        case Text_Type.TEXT:
            return LeafNode(None, text_node.text)
        case Text_Type.BOLD:
            return LeafNode("b", text_node.text)
        case Text_Type.ITALIC:
            return LeafNode("i", text_node.text)
        case Text_Type.CODE:
            return LeafNode("code", text_node.text)
        case Text_Type.LINK:
            if text_node.url is None:
                raise ValueError("URL must be provided for link type TextNode")
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case Text_Type.IMAGE:
            if text_node.url is None:
                raise ValueError("URL must be provided for image type TextNode")
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
        case _:
            raise ValueError(f"Unsupported Text_Type: {text_node.text_type}")

def markdown_to_html_node(markdown):
    """
    Converts markdown text to a list of HTML nodes.
    
    This function takes markdown text as input, breaks it down into blocks, and then converts each block into an HTML node.
    The type of HTML node created depends on the type of markdown block. The function returns a list of these HTML nodes.
    """
    blocks = markdown_to_blocks(markdown)  # Breaks markdown into blocks
    children = []
    for block in blocks:
        children.append(block_to_html_node(block))  # Converts each block to an HTML node
    return ParentNode("div", children)

def block_to_html_node(block):
    """
    Converts a markdown block to an HTML node based on its type.
    
    This function determines the type of the markdown block and calls the appropriate function to convert it into an HTML node.
    """
    block_type = block_to_block_type(block)  # Determines the type of the block
    match block_type:
        case Block_Type.PARAGRAPH:
            return paragraph_to_html_node(block)  # Converts to paragraph HTML node
        case Block_Type.HEADING:
            return heading_to_html_node(block)  # Converts to heading HTML node
        case Block_Type.CODE:
            return code_to_html_node(block)  # Converts to code HTML node
        case Block_Type.QUOTE:
            return quote_to_html_node(block)  # Converts to quote HTML node
        case Block_Type.UNORDERED_LIST:
            return unordered_list_to_html_node(block)  # Converts to unordered list HTML node
        case Block_Type.ORDERED_LIST:
            return ordered_list_to_html_node(block)  # Converts to ordered list HTML node
        case _:
            raise ValueError(f"Unsupported block type: {block_type}")  # Raises error for unsupported block types

def text_to_children(text):
    """
    Converts text into a list of HTML nodes.
    
    This function takes text as input, breaks it down into text nodes, and then converts each text node into an HTML node.
    The function returns a list of these HTML nodes.
    """
    text_nodes = text_to_textnodes(text)  # Breaks text into text nodes
    html_nodes = []
    for text_node in text_nodes:
        html_nodes.append(text_node_to_html_node(text_node))  # Converts each text node to an HTML node
    return html_nodes

def paragraph_to_html_node(block):
    """
    Converts a markdown paragraph block to an HTML paragraph node.
    
    This function takes a markdown paragraph block, joins its lines into a single string, converts the string into HTML nodes,
    and returns a ParentNode representing a paragraph with the converted HTML nodes as children.
    """
    lines = block.split("\n")  # Splits the block into lines
    paragraph = " ".join(lines)  # Joins lines into a single string
    children = text_to_children(paragraph)  # Converts the string into HTML nodes
    return ParentNode("p", children)  # Returns a ParentNode representing a paragraph

def heading_to_html_node(block):
    """
    Converts a markdown heading block to an HTML heading node.
    
    This function determines the level of the heading based on the number of '#' characters at the start of the block,
    converts the heading text into HTML nodes, and returns a ParentNode representing the heading with the converted HTML nodes as children.
    """
    for i in range(len(block)):
        if block[i] != "#":
            break
    children = text_to_children(block[i+1:])  # Converts the heading text into HTML nodes
    return ParentNode(f"h{i}", children)  # Returns a ParentNode representing the heading

def code_to_html_node(block):
    """
    Converts a markdown code block to an HTML code node.
    
    This function extracts the code content from the block, converts it into HTML nodes, and returns a ParentNode representing a preformatted code block
    with the converted HTML nodes as children.
    """
    children = text_to_children(block[3:-3])  # Extracts and converts the code content into HTML nodes
    return ParentNode("pre", [ParentNode("code", children)])  # Returns a ParentNode representing a preformatted code block

def quote_to_html_node(block):
    """
    Converts a markdown quote block to an HTML blockquote node.
    
    This function extracts the quote content from the block, converts it into HTML nodes, and returns a ParentNode representing a blockquote
    with the converted HTML nodes as children.
    """
    text_list = []
    lines = block.split("\n")
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("Invalid quote block: quote lines must start with '>'")
        text_list.append(line[2:])
    quote = " ".join(text_list)
    children = text_to_children(quote.strip())  # Extracts and converts the quote content into HTML nodes
    return ParentNode("blockquote", children)  # Returns a ParentNode representing a blockquote

def unordered_list_to_html_node(block):
    """
    Converts a markdown unordered list block to an HTML unordered list node.
    
    This function splits the block into list items, converts each item into HTML nodes, and returns a ParentNode representing an unordered list
    with the converted HTML nodes as children.
    """
    text_list = []
    lines = block.split("\n")
    for line in lines:
            children = text_to_children(line[2:])  # Converts each list item into HTML nodes
            text_list.append(ParentNode("li", children))  # Adds the HTML nodes to a list
    return ParentNode("ul", text_list)  # Returns a ParentNode representing an unordered list

def ordered_list_to_html_node(block):
    """
    Converts a markdown ordered list block to an HTML ordered list node.
    
    This function splits the block into list items, converts each item into HTML nodes, and returns a ParentNode representing an ordered list
    with the converted HTML nodes as children.
    """
    text_list = []
    lines = block.split("\n")
    for line in lines:
            children = text_to_children(line[3:])  # Converts each list item into HTML nodes
            text_list.append(ParentNode("li", children))  # Adds the HTML nodes to a list
    return ParentNode("ol", text_list)  # Returns a ParentNode representing an ordered list