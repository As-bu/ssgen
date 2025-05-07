import unittest

from textnode import TextType, TextNode, tnode_to_hnode
from htmlnode import HTMLNode, LeafNode, ParentNode
from block_transformers import markdown_to_blocks


class test_markdown_to_blocks(unittest.TestCase):
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

    def test_markdown_to_one_block(self):
        md = """
This is just one **BLOCK**!
"""
        blocks = markdown_to_blocks(md)
        self.assertListEqual(
            [
                "This is just one **BLOCK**!",
            ],
            blocks,
        )

    def test_markdown_to_blocks_heavyhanded(self):
        md = """
My enter key gets stuck all the time!






It's _really_ annoying **!!!!!!** Here's some reasons:






- It messes up space in the code
- Looks bad
- Takes up an extra few bytes
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "My enter key gets stuck all the time!",
                "It's _really_ annoying **!!!!!!** Here's some reasons:",
                "- It messes up space in the code\n- Looks bad\n- Takes up an extra few bytes",
            ],
        )



if __name__ == '__main__':
    unittest.main()
