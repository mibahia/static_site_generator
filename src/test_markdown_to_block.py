import unittest
from block_markdown import block_to_block_type, BlockType
from markdown_to_block import markdown_to_html_node, markdown_to_blocks

class TestBlockType(unittest.TestCase):

    def test_block_to_block_type(self):
        unordered_list = """* This is the first line\n* This is the second line\n* This is the third line"""

        ordered_list = """1. First item\n2. Second item\n3. Third item"""

        paragraph = """
        In lines of light, the logic flows,
        A dance of thought that softly glows. 
        With whispers clear, the codes align,
        Creating worlds in every line. 
        A simple spark ignites the night,
        As dreams take form in pure delight. 
        In endless loops, we find our way,
        In coded hearts, we weave our play.
        """

        self.assertEqual(block_to_block_type(unordered_list), BlockType.UNORDERED_LIST)
        self.assertEqual(block_to_block_type(ordered_list), BlockType.ORDERED_LIST)
        self.assertEqual(block_to_block_type(paragraph), BlockType.PARAGRAPH)
    
    def test_paragraph(self):
        md = """
        This is **bolded** paragraph
        text in a p
        tag here
            
        This is another paragraph with _italic_ text and `code` here
        """
        
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
        html,
        "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
    )
        
    def test_codeblock(self):
        md = """
        ```
        This is text that _should_ remain
        the **same** even with inline stuff
        ```
        """
    
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )


if __name__ == '__main__':  
    unittest.main()