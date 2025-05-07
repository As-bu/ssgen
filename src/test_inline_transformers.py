import unittest

from textnode import TextType, TextNode
from htmlnode import HTMLNode, LeafNode, ParentNode
from inline_transformers import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_images, split_nodes_links, text_to_textnodes


class test_split_nodes_delimiter(unittest.TestCase):
    def test_delim_italic(self):
        node = TextNode("This is not _Italian_, you should know that by now!", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("This is not ", TextType.TEXT),
                TextNode("Italian", TextType.ITALIC),
                TextNode(", you should know that by now!", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_delim_multi_bold(self):
        node = TextNode("In my native language it's not **bold** it's **FAT**, weird, right?", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("In my native language it's not ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" it's ", TextType.TEXT),
                TextNode("FAT", TextType.BOLD),
                TextNode(", weird, right?", TextType.TEXT),
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
        node = TextNode("It ain't much, **but** it's honest `code`", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, TextType.CODE)
        self.assertListEqual(
            [
                TextNode("It ain't much, ", TextType.TEXT),
                TextNode("but", TextType.BOLD),
                TextNode(" it's honest ", TextType.TEXT),
                TextNode("code", TextType.CODE),
            ],
            new_nodes,
        )

    def test_delim_start_and_end_bold(self):
        node = TextNode("**This** is a test, you got it? **BRO**", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This", TextType.BOLD),
                TextNode(" is a test, you got it? ", TextType.TEXT),
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
            TextType.TEXT,
        )
        new_nodes = split_nodes_images([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_links([node])
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"),
            ],
            new_nodes,
        )

    def test_split_just_img(self):
        node = TextNode(
            "![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
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
                TextType.TEXT
        )
        new_nodes = split_nodes_links([node])
        self.assertListEqual(
                [
                    TextNode("This is text with a link ", TextType.TEXT),
                    TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                    TextNode(".", TextType.TEXT),
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
                TextNode("This is the ", TextType.TEXT),
                TextNode("ULTIMATE", TextType.BOLD),
                TextNode(" test! It's not ", TextType.TEXT),
                TextNode("fancy", TextType.ITALIC),
                TextNode(" but this ", TextType.TEXT),
                TextNode("code", TextType.CODE),
                TextNode(" took some time. ", TextType.TEXT),
                TextNode("Boot.dev", TextType.LINK, "https://boot.dev"),
                TextNode(" has been great! Thanks, guys!", TextType.TEXT),
                TextNode("Celebration", TextType.IMAGE, "https://imgur.com/P9LqjBX"),
            ],
            nodes,
        )


if __name__ == '__main__':
    unittest.main()
