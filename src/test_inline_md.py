import unittest
from inline_md import *
from textnode import TextNode
from htmlnode import HTMLNode
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
            # Empty URL (Text, Expected)
            ("This is a text with a ![rick roll]() and ![obi wan]()", 
             [("rick roll", ""), ("obi wan", "")]),
            # Spaces Around Text 
            ("This is text with a ![ rick roll ](https://i.imgur.com/aKaOqIh.gif) and ![ obi wan ](https://i.imgur.com/fJRm4Vk.jpeg)", 
             [(" rick roll ", "https://i.imgur.com/aKaOqIh.gif"), (" obi wan ", "https://i.imgur.com/fJRm4Vk.jpeg")]),
            # Nested Brackets or Parentheses (Text, Expected)
            ("This is text with a ![[image]rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan [the only one]](https://i.imgur.com/fJRm4Vk.jpeg)", 
             [("[image]rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan [the only one]", "https://i.imgur.com/fJRm4Vk.jpeg")]),
            # Special Characters in Alt Text or URL 
            ("This is text with a ![rick *roll &^%$#@!](https://i.imgur.com/aKaOqIh.gif) and ![obi wan *&*&*&](https://i.imgur.com/fJRm4Vk.jpeg)", 
             [("rick *roll &^%$#@!", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan *&*&*&", "https://i.imgur.com/fJRm4Vk.jpeg")]),
            # No URL but Parentheses Present 
            ("This is text with a ![rick roll](   ) and ![obi wan](  )", 
             [("rick roll", "   "), ("obi wan", "  ")]),
            # Alt Text with Newline Characters (Text, Expected)
            ("This is text with a ![rick\nroll](https://i.imgur.com/aKaOqIh.gif) and ![obi\nwan](https://i.imgur.com/fJRm4Vk.jpeg)", 
             []),
            # No text
            ("![rick roll](https://i.imgur.com/aKaOqIh.gif)![Google](https://www.google.com)", [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("Google", "https://www.google.com")]),
        ]
        
        for text, expected in edge_cases:
            with self.subTest(text=text):
                actual = extract_markdown_images(text)
                self.assertEqual(actual, expected)

    def test_extract_markdown_links(self):
        edge_cases = [
            # One Link (Text, Expected)
            ("This is text with a [link](https://boot.dev)", [("link", "https://boot.dev")]),
            # Multiple Links (Text, Expected)
            ("This is text with a [link](https://boot.dev) and [another link](https://22222.boot.dev) and [third link](https://33333.boot.dev)", [("link", "https://boot.dev"), ("another link", "https://22222.boot.dev"), ("third link", "https://33333.boot.dev")]),
        ]

        for text, expected in edge_cases:
            with self.subTest(text=text):
                actual = extract_markdown_links(text)
                self.assertListEqual(actual, expected)

    def test_split_nodes_link(self):
        edge_cases = [
            # Single TextNode (Text, Expected)
            ([TextNode(
                "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
                Text_Type.TEXT,
            )], 
            [
        TextNode("This is text with a link ", Text_Type.TEXT),
        TextNode("to boot dev", Text_Type.LINK, "https://www.boot.dev"),
        TextNode(" and ", Text_Type.TEXT),
        TextNode("to youtube", Text_Type.LINK, "https://www.youtube.com/@bootdotdev"),
            ],
            ),
            # Multiple TextNodes (Text, Expected)
            ([TextNode(
                "1st text with a [link](https://boot.dev)",
                Text_Type.TEXT,
            ),
            TextNode(
                "2nd text with a [link](https://22222.boot.dev)",
                Text_Type.TEXT,
            ),
            TextNode(
                "3rd text with a [link](https://33333.boot.dev)",
                Text_Type.TEXT,
            )], 
            [
                TextNode("1st text with a ", Text_Type.TEXT),
                TextNode("link", Text_Type.LINK, "https://boot.dev"),
                TextNode("2nd text with a ", Text_Type.TEXT),
                TextNode("link", Text_Type.LINK, "https://22222.boot.dev"),
                TextNode("3rd text with a ", Text_Type.TEXT),
                TextNode("link", Text_Type.LINK, "https://33333.boot.dev"),
            ],
            ),
            # No text at the front (Text, Expected)
            ([TextNode(
                "[1st link](https://boot.dev) is a link",
                Text_Type.TEXT,
            ),
            TextNode(
                "[2nd link](https://22222.boot.dev) is the second link",
                Text_Type.TEXT,
            ),
            ], 
            [
                TextNode("1st link", Text_Type.LINK, "https://boot.dev"),
                TextNode(" is a link", Text_Type.TEXT),
                TextNode("2nd link", Text_Type.LINK, "https://22222.boot.dev"),
                TextNode(" is the second link", Text_Type.TEXT),
            ],
            ),
            # No text at the end (Text, Expected)
            ([TextNode(
                "a link is [1st link](https://boot.dev)",
                Text_Type.TEXT,
            ),
            TextNode(
                "the second link is [2nd link](https://22222.boot.dev)",
                Text_Type.TEXT,
            ),
            ], 
            [
                TextNode("a link is ", Text_Type.TEXT),
                TextNode("1st link", Text_Type.LINK, "https://boot.dev"),
                TextNode("the second link is ", Text_Type.TEXT),
                TextNode("2nd link", Text_Type.LINK, "https://22222.boot.dev"),
            ],
            ),
            # HTMLNode input (Text, Expected)
            ([HTMLNode("p", "a link is ", None, {"class": "primary"}),
                HTMLNode("a", "1st link", None, {"href": "https://boot.dev"}),
                HTMLNode("p", "the second link is ", None, {"class": "secondary"}),
                HTMLNode("a", "2nd link", None, {"href": "https://22222.boot.dev"}),
            ], 
            TypeError
            ),
            # Invalid input (Text, Expected)
            ("a link is [1st link](https://boot.dev)", TypeError),
            # depulicated links (Text, Expected)
            ([TextNode(
                "a link is [1st link](https://boot.dev), 2nd link is [1st link](https://boot.dev), 3rd link is [1st link](https://boot.dev)",
                Text_Type.TEXT,
            ),
            ],
            [
                TextNode("a link is ", Text_Type.TEXT),
                TextNode("1st link", Text_Type.LINK, "https://boot.dev"),
                TextNode(", 2nd link is ", Text_Type.TEXT),
                TextNode("1st link", Text_Type.LINK, "https://boot.dev"),
                TextNode(", 3rd link is ", Text_Type.TEXT),
                TextNode("1st link", Text_Type.LINK, "https://boot.dev"),
            ]
            ),
        ]

        for text, expected in edge_cases:
            with self.subTest(text=text):
                #if isinstance(expected, Exception):
                if isinstance(expected, type) and issubclass(expected, Exception):
                    with self.assertRaises(expected):
                        split_nodes_link(text)
                else:
                    actual = split_nodes_link(text)
                    self.assertListEqual(actual, expected)

    def test_extract_markdown_links(self):
        edge_cases = [
            # One Link (Text, Expected)
            ("This is text with a [link](https://boot.dev)", [("link", "https://boot.dev")]),
            # Multiple Links (Text, Expected)
            ("This is text with a [link](https://boot.dev) and [another link](https://22222.boot.dev) and [third link](https://33333.boot.dev)", [("link", "https://boot.dev"), ("another link", "https://22222.boot.dev"), ("third link", "https://33333.boot.dev")]),
        ]

        for text, expected in edge_cases:
            with self.subTest(text=text):
                actual = extract_markdown_links(text)
                self.assertListEqual(actual, expected)

    def test_split_nodes_link(self):
        edge_cases = [
            # Single TextNode (Text, Expected)
            ([TextNode(
                "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
                Text_Type.TEXT,
            )], 
            [
        TextNode("This is text with a link ", Text_Type.TEXT),
        TextNode("to boot dev", Text_Type.LINK, "https://www.boot.dev"),
        TextNode(" and ", Text_Type.TEXT),
        TextNode("to youtube", Text_Type.LINK, "https://www.youtube.com/@bootdotdev"),
            ],
            ),
            # Multiple TextNodes (Text, Expected)
            ([TextNode(
                "1st text with a [link](https://boot.dev)",
                Text_Type.TEXT,
            ),
            TextNode(
                "2nd text with a [link](https://22222.boot.dev)",
                Text_Type.TEXT,
            ),
            TextNode(
                "3rd text with a [link](https://33333.boot.dev)",
                Text_Type.TEXT,
            )], 
            [
                TextNode("1st text with a ", Text_Type.TEXT),
                TextNode("link", Text_Type.LINK, "https://boot.dev"),
                TextNode("2nd text with a ", Text_Type.TEXT),
                TextNode("link", Text_Type.LINK, "https://22222.boot.dev"),
                TextNode("3rd text with a ", Text_Type.TEXT),
                TextNode("link", Text_Type.LINK, "https://33333.boot.dev"),
            ],
            ),
            # No text at the front (Text, Expected)
            ([TextNode(
                "[Hello! 1st link](https://boot.dev) is a link",
                Text_Type.TEXT,
            ),
            TextNode(
                "[2nd link](https://22222.boot.dev) is the second link",
                Text_Type.TEXT,
            ),
            ], 
            [
                TextNode("Hello! 1st link", Text_Type.LINK, "https://boot.dev"),
                TextNode(" is a link", Text_Type.TEXT),
                TextNode("2nd link", Text_Type.LINK, "https://22222.boot.dev"),
                TextNode(" is the second link", Text_Type.TEXT),
            ],
            ),
            # No text at the end (Text, Expected)
            ([TextNode(
                "a link is [1st link](https://boot.dev)",
                Text_Type.TEXT,
            ),
            TextNode(
                "the second link is [2nd link](https://22222.boot.dev)",
                Text_Type.TEXT,
            ),
            ], 
            [
                TextNode("a link is ", Text_Type.TEXT),
                TextNode("1st link", Text_Type.LINK, "https://boot.dev"),
                TextNode("the second link is ", Text_Type.TEXT),
                TextNode("2nd link", Text_Type.LINK, "https://22222.boot.dev"),
            ],
            ),
            # HTMLNode input (Text, Expected)
            ([HTMLNode("p", "a link is ", None, {"class": "primary"}),
                HTMLNode("a", "1st link", None, {"href": "https://boot.dev"}),
                HTMLNode("p", "the second link is ", None, {"class": "secondary"}),
                HTMLNode("a", "2nd link", None, {"href": "https://22222.boot.dev"}),
            ], 
            TypeError
            ),
            # Invalid input (Text, Expected)
            ("a link is [1st link](https://boot.dev)", TypeError),
            # depulicated links (Text, Expected)
            ([TextNode(
                "a link is [1st link](https://boot.dev), 2nd link is [1st link](https://boot.dev), 3rd link is [1st link](https://boot.dev)",
                Text_Type.TEXT,
            ),
            ],
            [
                TextNode("a link is ", Text_Type.TEXT),
                TextNode("1st link", Text_Type.LINK, "https://boot.dev"),
                TextNode(", 2nd link is ", Text_Type.TEXT),
                TextNode("1st link", Text_Type.LINK, "https://boot.dev"),
                TextNode(", 3rd link is ", Text_Type.TEXT),
                TextNode("1st link", Text_Type.LINK, "https://boot.dev"),
            ]
            ),
        ]

        for text, expected in edge_cases:
            with self.subTest(text=text):
                #if isinstance(expected, Exception):
                if isinstance(expected, type) and issubclass(expected, Exception):
                    with self.assertRaises(expected):
                        split_nodes_link(text)
                else:
                    actual = split_nodes_link(text)
                    self.assertListEqual(actual, expected)

    def test_text_to_textnodes(self):
        nodes = text_to_textnodes(
            "This is **text** with an *italic* word and a `code block` and an ![image](https://i.imgur.com/zjjcJKZ.png) and a [link](https://boot.dev)"
        )
        print(nodes)
        self.assertListEqual(
            [
                TextNode("This is ", Text_Type.TEXT),
                TextNode("text", Text_Type.BOLD),
                TextNode(" with an ", Text_Type.TEXT),
                TextNode("italic", Text_Type.ITALIC),
                TextNode(" word and a ", Text_Type.TEXT),
                TextNode("code block", Text_Type.CODE),
                TextNode(" and an ", Text_Type.TEXT),
                TextNode("image", Text_Type.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and a ", Text_Type.TEXT),
                TextNode("link", Text_Type.LINK, "https://boot.dev"),
            ],
            nodes,
        )      
    

if __name__ == "__main__":
    unittest.main()