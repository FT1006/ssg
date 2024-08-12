import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode, Text_Type, text_node_to_html_node
from textnode import TextNode


class TestHTMLNode(unittest.TestCase):
    def test_to_html_props(self):
        node = HTMLNode(
            "div",
            "Hello, world!",
            None,
            {"class": "greeting", "href": "https://boot.dev"},
        )
        self.assertEqual(
            node.props_to_html(),
            ' class="greeting" href="https://boot.dev"',
        )

    def test_values(self):
        node = HTMLNode(
            "div",
            "I wish I could read",
        )
        self.assertEqual(
            node.tag,
            "div",
        )
        self.assertEqual(
            node.value,
            "I wish I could read",
        )
        self.assertEqual(
            node.children,
            None,
        )
        self.assertEqual(
            node.props,
            None,
        )

    def test_repr(self):
        node = HTMLNode(
            "p",
            "What a strange world",
            None,
            {"class": "primary"},
        )
        self.assertEqual(
            node.__repr__(),
            "HTMLNode(tag: p, value: What a strange world, children: None, props: {'class': 'primary'})",
        )
    
    def test_to_html_no_children(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_to_html_no_tag(self):
        node = LeafNode(None, "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_many_children(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>",
        )

    def test_headings(self):
        node = ParentNode(
            "h2",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<h2><b>Bold text</b>Normal text<i>italic text</i>Normal text</h2>",
        )

class TestTextNodeToHTMLNode(unittest.TestCase):
    
    def test_text_node_to_html_node_text(self):
        node = TextNode("Hello", Text_Type.TEXT)
        expected = LeafNode(None, "Hello")
        self.assertEqual(text_node_to_html_node(node), expected)

    def test_text_node_to_html_node_bold(self):
        node = TextNode("Bold", Text_Type.BOLD)
        expected = LeafNode("b", "Bold")
        self.assertEqual(text_node_to_html_node(node), expected)

    def test_text_node_to_html_node_italic(self):
        node = TextNode("Italic", Text_Type.ITALIC)
        expected = LeafNode("i", "Italic")
        self.assertEqual(text_node_to_html_node(node), expected)

    def test_text_node_to_html_node_code(self):
        node = TextNode("Code", Text_Type.CODE)
        expected = LeafNode("code", "Code")
        self.assertEqual(text_node_to_html_node(node), expected)

    def test_text_node_to_html_node_link(self):
        node = TextNode("Link", Text_Type.LINK, "http://example.com")
        expected = LeafNode("a", "Link", props={"href": "http://example.com"})
        self.assertEqual(text_node_to_html_node(node), expected)

    def test_text_node_to_html_node_image(self):
        node = TextNode("Alt text", Text_Type.IMAGE, "http://image.com/img.png")
        expected = LeafNode("img", "", props={"src": "http://image.com/img.png", "alt": "Alt text"})
        self.assertEqual(text_node_to_html_node(node), expected)

    def test_text_node_to_html_node_unsupported_type(self):
        with self.assertRaises(ValueError):
            text_node_to_html_node(TextNode("Unsupported", Text_Type("unsupported")))

    def test_text_node_to_html_node_link_without_url(self):
        with self.assertRaises(ValueError):
            text_node_to_html_node(TextNode("No URL", Text_Type.LINK))

    def test_text_node_to_html_node_image_without_url(self):
        with self.assertRaises(ValueError):
            text_node_to_html_node(TextNode("No URL", Text_Type.IMAGE))

    def test_text_node_to_html_node_invalid_input(self):
        with self.assertRaises(TypeError):
            text_node_to_html_node("Not a TextNode")


if __name__ == "__main__":
    unittest.main()