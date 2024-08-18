import unittest
from block_md import *
from enum import Enum

class TestBlockMD(unittest.TestCase):
    def test_markdown_to_blocks(self):
        test_cases = [
            # Sample input
            {
                "input": "# This is a heading\n\nThis is a paragraph of text. It has some **bold** and *italic* words inside of it.\n\n* This is the first list item in a list block\n* This is another list item\n* This is another list item",
                "expected": ["# This is a heading","This is a paragraph of text. It has some **bold** and *italic* words inside of it.","* This is the first list item in a list block\n* This is another list item\n* This is another list item"],
                "exception": None
            },
        ]

        for case in test_cases:
            with self.subTest(case=case):
                if case["exception"]:
                    with self.assertRaises(case["exception"]):
                        markdown_to_blocks(case["input"])
                else:
                    actual = markdown_to_blocks(case["input"])
                    self.assertEqual(actual, case["expected"])

    def test_block_to_block_type(self):
        test_cases = [
            # start with "###"
            {
                "input": "### This is a heading",
                "expected": Block_Type.HEADING,
                "exception": None
            },
            # start with "```"
            {
                "input": "``` This is a code block\n```\nThis is a code block\n```",
                "expected": Block_Type.CODE,
                "exception": None
            },
            # every line starts with ">"
            {
                "input": "> This is a quote\n> This is another quote\n> This is the last quote",
                "expected": Block_Type.QUOTE,
                "exception": None
            },
            # every line starts with "* "
            {
                "input": "* This is a list item\n* This is another list item\n* This is the last list item",
                "expected": Block_Type.UNORDERED_LIST,
                "exception": None
            },
            # every line starts with "- "
            {
                "input": "- This is a list item\n- This is another list item\n- This is the last list item",
                "expected": Block_Type.UNORDERED_LIST,
                "exception": None
            },
            # every line starts with "x. " x += 1
            {
                "input": "1. This is a list item\n2. This is another list item\n3. This is the last list item",
                "expected": Block_Type.ORDERED_LIST,
                "exception": None
            },
            # normal single line
            {
                "input": "This is a paragraph",
                "expected": Block_Type.PARAGRAPH,
                "exception": None
            },
            # normal multi line
            {
                "input": "This is a paragraph\nThis is another paragraph",
                "expected": Block_Type.PARAGRAPH,
                "exception": None
            },
            # edge case
            {
                "input": "...This is a paragraph...This is another paragraph",
                "expected": Block_Type.PARAGRAPH,
                "exception": None
            },
        ]

        for case in test_cases:
            with self.subTest(case=case):
                if case["exception"]:
                    with self.assertRaises(case["exception"]):
                        block_to_block_type(case["input"])
                else:
                    actual = block_to_block_type(case["input"])
                    self.assertEqual(actual, case["expected"])

if __name__ == "__main__":
    unittest.main()