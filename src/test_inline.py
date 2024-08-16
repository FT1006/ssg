import unittest
from inline import TextNode, Text_Type, split_nodes_delimiter, extract_markdown_images, extract_markdown_links
from textnode import TextNode
from enum import Enum



class TestSplitNodesDelimiter(unittest.TestCase): 
    def test_split_nodes_delimiter_single_nodes(self): 
        old_nodes = [TextNode("This is text with a `code block` word", Text_Type.TEXT)]
        print(old_nodes)
        actual = split_nodes_delimiter(old_nodes, "`", Text_Type.CODE)
        expected = [
            TextNode("This is text with a ", Text_Type.TEXT), 
            TextNode("code block", Text_Type.CODE), 
            TextNode(" word", Text_Type.TEXT)
        ]
        try:
            self.assertEqual(actual, expected)
            print(f"Test Passed: The actual output matches the expected output.")
        except AssertionError:
            print(f"Test Failed: The actual output does not match the expected output.")
            print(f"Expected: {self.format_nodes(expected)}")
            print(f"Actual: {self.format_nodes(actual)}")
            raise  #

    def test_split_nodes_delimiter_multiple_nodes(self):
        old_nodes = [TextNode("This is text with a `code block` word", Text_Type.TEXT),
                     TextNode("This is text with a **bold text** word", Text_Type.TEXT),
                     TextNode("This is text with a *italic text* word", Text_Type.TEXT),
                     TextNode("This is text with a ~strikethrough text~ word", Text_Type.CODE)]
        actual = split_nodes_delimiter(old_nodes, "`", Text_Type.CODE)
        expected = [
            TextNode("This is text with a ", Text_Type.TEXT), 
            TextNode("code block", Text_Type.CODE), 
            TextNode(" word", Text_Type.TEXT),
            TextNode("This is text with a **bold text** word", Text_Type.TEXT), 
            TextNode("This is text with a *italic text* word", Text_Type.TEXT), 
            TextNode("This is text with a ~strikethrough text~ word", Text_Type.CODE)
        ]
        try:
            self.assertEqual(actual, expected)
            print(f"Test Passed: The actual output matches the expected output.")
        except AssertionError:
            print(f"Test Failed: The actual output does not match the expected output.")
            print(f"Expected: {self.format_nodes(expected)}")
            print(f"Actual: {self.format_nodes(actual)}")
            raise  #
                         
    def test_split_nodes_empty_string(self):
        old_nodes = [TextNode("", Text_Type.TEXT)]
        actual = split_nodes_delimiter(old_nodes, "`", Text_Type.CODE)
        expected = [TextNode("", Text_Type.TEXT)]
        try:
            self.assertEqual(actual, expected)
            print(f"Test Passed: The actual output matches the expected output.")
        except AssertionError:
            print(f"Test Failed: The actual output does not match the expected output.")
            print(f"Expected: {self.format_nodes(expected)}")
            print(f"Actual: {self.format_nodes(actual)}")
            raise  #

    def test_split_nodes_no_delimiter(self):
        old_nodes = [TextNode("This is a regular text without code", Text_Type.TEXT)]
        actual = split_nodes_delimiter(old_nodes, "`", Text_Type.CODE)
        expected = [TextNode("This is a regular text without code", Text_Type.TEXT)]
        try:
            self.assertEqual(actual, expected)
            print(f"Test Passed: The actual output matches the expected output.")
        except AssertionError:
            print(f"Test Failed: The actual output does not match the expected output.")
            print(f"Expected: {self.format_nodes(expected)}")
            print(f"Actual: {self.format_nodes(actual)}")
            raise  #

    def test_split_nodes_delimiter_at_edges(self):
        old_nodes = [TextNode("`code at start` and at `end`", Text_Type.TEXT)]
        actual = split_nodes_delimiter(old_nodes, "`", Text_Type.CODE)
        expected = [
            TextNode("", Text_Type.TEXT),
            TextNode("code at start", Text_Type.CODE),
            TextNode(" and at ", Text_Type.TEXT),
            TextNode("end", Text_Type.CODE),
            TextNode("", Text_Type.TEXT)
        ]
        try:
            self.assertEqual(actual, expected)
            print(f"Test Passed: The actual output matches the expected output.")
        except AssertionError:
            print(f"Test Failed: The actual output does not match the expected output.")
            print(f"Expected: {self.format_nodes(expected)}")
            print(f"Actual: {self.format_nodes(actual)}")
            raise  #

    def test_split_nodes_consecutive_delimiters(self):
        old_nodes = [TextNode("This is `` empty `` code blocks", Text_Type.TEXT)]
        actual = split_nodes_delimiter(old_nodes, "`", Text_Type.CODE)
        expected = [
            TextNode("This is ", Text_Type.TEXT),
            TextNode("", Text_Type.CODE),
            TextNode(" empty ", Text_Type.TEXT),
            TextNode("", Text_Type.CODE),
            TextNode(" code blocks", Text_Type.TEXT)
        ]
        try:
            self.assertEqual(actual, expected)
            print(f"Test Passed: The actual output matches the expected output.")
        except AssertionError:
            print(f"Test Failed: The actual output does not match the expected output.")
            print(f"Expected: {self.format_nodes(expected)}")
            print(f"Actual: {self.format_nodes(actual)}")
            raise  # Reraise to let unittest handle the failure as usual

    @staticmethod
    def format_nodes(nodes):
        return ', '.join([f"TextNode({node.text}, {node.text_type})" for node in nodes])
    
    def test_extract_markdown_images(self):
        edge_cases = [
            # No Exclamation Mark
            ("This is text with a [rick roll](https://i.imgur.com/aKaOqIh.gif) and [obi wan](https://i.imgur.com/fJRm4Vk.jpeg)", []),
            # Empty Alt Text
            ("This is text with a ![](https://i.imgur.com/aKaOqIh.gif) and ![](https://i.imgur.com/fJRm4Vk.jpeg)", 
             [("", "https://i.imgur.com/aKaOqIh.gif"), ("", "https://i.imgur.com/fJRm4Vk.jpeg")]),
            # Empty URL
            ("This is a text with a ![rick roll]() and ![obi wan]()", 
             [("rick roll", ""), ("obi wan", "")]),
            # Spaces Around Text
            ("This is text with a ![ rick roll ](https://i.imgur.com/aKaOqIh.gif) and ![ obi wan ](https://i.imgur.com/fJRm4Vk.jpeg)", 
             [(" rick roll ", "https://i.imgur.com/aKaOqIh.gif"), (" obi wan ", "https://i.imgur.com/fJRm4Vk.jpeg")]),
            # Nested Brackets or Parentheses
            ("This is text with a ![[image]rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan [the only one]](https://i.imgur.com/fJRm4Vk.jpeg)", 
             [("[image]rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan [the only one]", "https://i.imgur.com/fJRm4Vk.jpeg")]),
            # Special Characters in Alt Text or URL
            ("This is text with a ![rick *roll &^%$#@!](https://i.imgur.com/aKaOqIh.gif) and ![obi wan *&*&*&](https://i.imgur.com/fJRm4Vk.jpeg)", 
             [("rick *roll &^%$#@!", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan *&*&*&", "https://i.imgur.com/fJRm4Vk.jpeg")]),
            # No URL but Parentheses Present
            ("This is text with a ![rick roll](   ) and ![obi wan](  )", 
             [("rick roll", "   "), ("obi wan", "  ")]),
            # Alt Text with Newline Characters
            ("This is text with a ![rick\nroll](https://i.imgur.com/aKaOqIh.gif) and ![obi\nwan](https://i.imgur.com/fJRm4Vk.jpeg)", 
             []),
        ]
        
        for text, expected in edge_cases:
            with self.subTest(text=text):
                actual = extract_markdown_images(text)
                self.assertEqual(actual, expected)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a [link](https://boot.dev) and [another link](https://blog.boot.dev)"
        )
        self.assertListEqual(
            [
                ("link", "https://boot.dev"),
                ("another link", "https://blog.boot.dev"),
            ],
            matches,
        )



if __name__ == "__main__":
    unittest.main()