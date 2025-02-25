import unittest
from block_to_block_types import block_to_block_type, BlockType

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


if __name__ == '__main__':  
    unittest.main()