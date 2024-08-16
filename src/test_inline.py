import unittest
from inline import TextNode, Text_Type, split_nodes_delimiter
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




if __name__ == "__main__":
    unittest.main()