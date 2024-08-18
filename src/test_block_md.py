import unittest
from block_md import markdown_to_blocks

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

if __name__ == "__main__":
    unittest.main()