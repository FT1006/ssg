from enum import Enum

class Text_Type(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode:
    def __init__(self, text, text_type: Text_Type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url
    
    def __eq__(self, other):
        return self.text == other.text and self.text_type == other.text_type and self.url == other.url
    
    def __repr__(self):
        return f"TextNode(\"{self.text}\", {self.text_type}, \"{self.url}\")"

def main():
    text_node = TextNode("Hello", "text", "https://www.google.com")
    print(text_node)

if __name__ == "__main__":
    main()