import unittest

from textnode import TextType, TextNode, tnode_to_hnode
from htmlnode import HTMLNode, LeafNode, ParentNode
from block_transformers import markdown_to_blocks, BlockType, block_to_blocktype


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


class test_block_to_blocktypes(unittest.TestCase):

    def test_block_is_para(self):
        textblock = "This is just text to test this function"
        transform = block_to_blocktype(textblock)
        self.assertEqual(
            transform,
            BlockType.PARA,
        )

    def test_block_is_heading(self):
        textblock = "### This is a heading."
        transform = block_to_blocktype(textblock)
        self.assertEqual(
            transform,
            BlockType.HEAD,
        )

    def test_block_is_code(self):
        textblock = "```This might not look like it, but it's a bunch of code.```"
        transform = block_to_blocktype(textblock)
        self.assertEqual(
            transform,
            BlockType.CODE,
        )

    def test_block_is_quote(self):
        textblock = ">This is a quote of a famous person or something.\n>Really!"
        transform = block_to_blocktype(textblock)
        self.assertEqual(
            transform,
            BlockType.QUOTE,
        )

    def test_block_is_ulist(self):
        textblock = "- This is a list of tests.\n- I hope it works.\n- We won't know until I run them."
        transform = block_to_blocktype(textblock)
        self.assertEqual(
            transform,
            BlockType.ULIST,
        )

    def test_block_is_olist(self):
        textblock = "1. This is an ordered list.\n2. You can tell, because it uses numbers.\n3. That's pretty much it."
        transform = block_to_blocktype(textblock)
        self.assertEqual(
            transform,
            BlockType.OLIST,
        )

    def test_block_is_olist_error(self):
        with self.assertRaises(Exception) as context:
            textblock = "2. This should throw an error.\n1. I hope.\n3. Please don't let me down."
            transform = block_to_blocktype(textblock)
            self.assertTrue("Formatting error, the list indices are not in order" in context.exception)

if __name__ == '__main__':
    unittest.main()
