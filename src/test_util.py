import unittest

from textnode import TextType, TextNode
from htmlnode import HTMLNode, LeafNode, ParentNode
from util import tnode_to_hnode, split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_images, split_nodes_links, text_to_textnodes, markdown_to_blocks


class test_node_to_node(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.NORMAL)
        html_node = tnode_to_hnode(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_italic(self):
        node = TextNode('Italian food is great', TextType.ITALIC)
        html_node = tnode_to_hnode(node)
        self.assertEqual(html_node.tag, 'i')
        self.assertEqual(html_node.value, 'Italian food is great')

    def test_link(self):
        node = TextNode('This is a link(to the past?)', TextType.LINK, 'https://boot.dev')
        html_node = tnode_to_hnode(node)
        self.assertEqual(html_node.tag, 'a')
        self.assertEqual(html_node.value, 'This is a link(to the past?)')
        self.assertEqual(
            html_node.props,
            {'href': 'https://boot.dev'},
        )

class test_split_nodes_delimiter(unittest.TestCase):
    def test_delim_italic(self):
        node = TextNode("This is not _Italian_, you should know that by now!", TextType.NORMAL)
        new_nodes = split_nodes_delimiter([node], TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("This is not ", TextType.NORMAL),
                TextNode("Italian", TextType.ITALIC),
                TextNode(", you should know that by now!", TextType.NORMAL),
            ],
            new_nodes,
        )

    def test_delim_multi_bold(self):
        node = TextNode("In my native language it's not **bold** it's **FAT**, weird, right?", TextType.NORMAL)
        new_nodes = split_nodes_delimiter([node], TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("In my native language it's not ", TextType.NORMAL),
                TextNode("bold", TextType.BOLD),
                TextNode(" it's ", TextType.NORMAL),
                TextNode("FAT", TextType.BOLD),
                TextNode(", weird, right?", TextType.NORMAL),
            ],
            new_nodes,
        )

    def test_delim_bold_node(self):
        node = TextNode("THIS IS A BOLD MESSAGE IN A BOLD NODE FROM A BALD MAN", TextType.BOLD)
        new_nodes = split_nodes_delimiter([node], TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("THIS IS A BOLD MESSAGE IN A BOLD NODE FROM A BALD MAN", TextType.BOLD),
            ],
            new_nodes,
        )

    def test_delim_bold_and_code(self):
        node = TextNode("It ain't much, **but** it's honest `code`", TextType.NORMAL)
        new_nodes = split_nodes_delimiter([node], TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, TextType.CODE)
        self.assertListEqual(
            [
                TextNode("It ain't much, ", TextType.NORMAL),
                TextNode("but", TextType.BOLD),
                TextNode(" it's honest ", TextType.NORMAL),
                TextNode("code", TextType.CODE),
            ],
            new_nodes,
        )

    def test_delim_start_and_end_bold(self):
        node = TextNode("**This** is a test, you got it? **BRO**", TextType.NORMAL)
        new_nodes = split_nodes_delimiter([node], TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This", TextType.BOLD),
                TextNode(" is a test, you got it? ", TextType.NORMAL),
                TextNode("BRO", TextType.BOLD),
            ],
            new_nodes,
        )

class test_extract_from_markdown(unittest.TestCase):
    def test_extract_markown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
                "This is a text with a link [to boot dev](https://boot.dev)"
        )
        self.assertListEqual([("to boot dev", "https://boot.dev")], matches)

class test_split_nodes_img_link(unittest.TestCase):
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.NORMAL,
        )
        new_nodes = split_nodes_images([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.NORMAL),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.NORMAL),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.NORMAL,
        )
        new_nodes = split_nodes_links([node])
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.NORMAL),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.NORMAL),
                TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"),
            ],
            new_nodes,
        )

    def test_split_just_img(self):
        node = TextNode(
            "![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.NORMAL,
        )
        new_nodes = split_nodes_images([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )

    def test_split_link(self):
        node = TextNode(
                "This is text with a link [to boot dev](https://www.boot.dev).",
                TextType.NORMAL
        )
        new_nodes = split_nodes_links([node])
        self.assertListEqual(
                [
                    TextNode("This is text with a link ", TextType.NORMAL),
                    TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                    TextNode(".", TextType.NORMAL),
                ],
                new_nodes,
        )

class test_text_to_nodes(unittest.TestCase):
    def test_text_to_textnodes(self):
        nodes = text_to_textnodes(
                "This is the **ULTIMATE** test! It's not _fancy_ but this `code` took some time. [Boot.dev](https://boot.dev) has been great! Thanks, guys!![Celebration](https://imgur.com/P9LqjBX)"
        )
        self.assertListEqual(
            [
                TextNode("This is the ", TextType.NORMAL),
                TextNode("ULTIMATE", TextType.BOLD),
                TextNode(" test! It's not ", TextType.NORMAL),
                TextNode("fancy", TextType.ITALIC),
                TextNode(" but this ", TextType.NORMAL),
                TextNode("code", TextType.CODE),
                TextNode(" took some time. ", TextType.NORMAL),
                TextNode("Boot.dev", TextType.LINK, "https://boot.dev"),
                TextNode(" has been great! Thanks, guys!", TextType.NORMAL),
                TextNode("Celebration", TextType.IMAGE, "https://imgur.com/P9LqjBX"),
            ],
            nodes,
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



if __name__ == '__main__':
    unittest.main()
