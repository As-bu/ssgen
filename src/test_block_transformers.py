import unittest

from textnode import TextType, TextNode, text_node_to_html_node
from htmlnode import HTMLNode, LeafNode, ParentNode
from block_transformers import (
    markdown_to_blocks,
    BlockType,
    block_to_blocktype,
    markdown_to_html_node,
)

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


class test_markdown_to_html_node(unittest.TestCase):
    def test_paragraphs(self):
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

    def test_lists(self):
        md = """
- This is a list
- with items
- and _more_ items

1. This is an `ordered` list
2. with items
3. and more items

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>This is a list</li><li>with items</li><li>and <i>more</i> items</li></ul><ol><li>This is an <code>ordered</code> list</li><li>with items</li><li>and more items</li></ol></div>",
        )

    def test_headings(self):
        md = """
# this is an h1

this is paragraph text

## this is an h2
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>this is an h1</h1><p>this is paragraph text</p><h2>this is an h2</h2></div>",
        )

    def test_blockquote(self):
        md = """
> This is a
> blockquote block

this is paragraph text

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a blockquote block</blockquote><p>this is paragraph text</p></div>",
        )

    def test_code(self):
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
