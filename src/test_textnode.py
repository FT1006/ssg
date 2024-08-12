import unittest
from enum import Enum
from textnode import TextNode, Text_Type

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", Text_Type.BOLD)
        node2 = TextNode("This is a text node", Text_Type.BOLD)
        self.assertEqual(node, node2)

    def test_eq2(self):
        node = TextNode("This is a text node", Text_Type.BOLD, None)
        node2 = TextNode("This is a text node", Text_Type.BOLD)
        self.assertEqual(node, node2)

    def test_eq3(self):
        node = TextNode("This is a text node", Text_Type.ITALIC)
        node2 = TextNode("This is a text node", Text_Type.BOLD)
        self.assertNotEqual(node, node2)

if __name__ == "__main__":
    unittest.main()