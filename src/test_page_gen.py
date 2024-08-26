import unittest
from page_gen import *

class TestExtractTitle(unittest.TestCase):
    def test_extract_title(self):
        md = """
# This is a title

This is a paragraph
"""
        self.assertEqual(extract_title(md), "This is a title")

    def test_extract_title_with_multiple_headings(self):
        md = """
# This is a title

# This is another title

This is a paragraph
"""
        self.assertEqual(extract_title(md), "This is a title")

    def test_extract_title_with_no_headings(self):
        md = """
This is a paragraph
"""
        with self.assertRaises(Exception):
            extract_title(md)

    def test_extract_title_with_empty_string(self):
        md = ""
        with self.assertRaises(Exception):
            extract_title(md)
    
    def test_extract_title_with_none(self):
        md = None
        with self.assertRaises(Exception):
            extract_title(md)

if __name__ == '__main__':
    unittest.main()