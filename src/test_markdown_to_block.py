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
    
    def test_heading(self):
        md = """
        ### This is a heading

        This is a paragraph.

        ## This is another heading

        This is another paragraph.

        # This is another heading

        This is another paragraph.
        """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h3>This is a heading</h3><p>This is a paragraph.</p><h2>This is another heading</h2><p>This is another paragraph.</p><h1>This is another heading</h1><p>This is another paragraph.</p></div>",
        )
    
    def test_orderedlist(self):
        md = """
        1. First item
        2. Second item
        3. Third item
        4. Fourth item
        """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>First item</li></ol><p>2. Second item</p><p>3. Third item</p><p>4. Fourth item</p></div>",
        )
    
    def test_unorderedlist(self):
        md = """
        - First item
        - Second item
        - Third item
        - Fourth item
        """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>First item</li><li>Second item</li><li>Third item</li><li>Fourth item</li></ul></div>",
        )


if __name__ == '__main__':  
    unittest.main()