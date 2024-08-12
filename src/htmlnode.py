from enum import Enum
from textnode import TextNode, Text_Type

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

def text_node_to_html_node(text_node: TextNode):
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
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case Text_Type.IMAGE:
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
