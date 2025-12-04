import unittest
from blocks_markdown import markdown_to_blocks, block_to_block_type, BlockType

class TestBlocksMarkdown(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_block_to_block_type_heading(self):
        block = block_to_block_type("###### heading")
        self.assertEqual(block, BlockType.HEADING)

    def test_block_to_block_type_code(self):
        block = block_to_block_type("``` code ```")
        self.assertEqual(block, BlockType.CODE)

    def test_block_to_block_type_quote(self):
        block = block_to_block_type("> quote")
        self.assertEqual(block, BlockType.QUOTE)

    def test_block_to_block_type_quote(self):
        block = block_to_block_type("- list")
        self.assertEqual(block, BlockType.UNORDERED_LIST)

    def test_block_to_block_type_quote(self):
        block = block_to_block_type("1. list")
        self.assertEqual(block, BlockType.ORDERED_LIST)

if __name__ == "__main__":
    unittest.main()