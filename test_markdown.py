import unittest
from block_markdown import markdown_to_blocks

class TestMarkdown(unittest.TestCase):
    
    def test_markdown_to_blocks(self):
        text = """
        # This is a heading

        This is a paragraph of text. It has some **bold** and *italic* words inside of it.

        * This is the first list item in a list block
        * This is a list item
        * This is another list item
        """

        text1 = """
        This is a paragraph

        This is a paragraph of text. It has some **bold** and *italic* words inside of it.

        * This is the first list item in a list block
        """

        expected_output = ['# This is a heading', 'This is a paragraph of text. It has some **bold** and *italic* words inside of it.', '* This is the first list item in a list block\n* This is a list item\n* This is another list item']
        expected_output1 = ['This is a paragraph\nThis is a paragraph of text. It has some **bold** and *italic* words inside of it.', '* This is the first list item in a list block']

        output = markdown_to_blocks(text)
        output1 = markdown_to_blocks(text1)

        self.assertListEqual(output, expected_output)
        self.assertListEqual(output1, expected_output1)