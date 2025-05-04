import unittest

from textnode import TextType, TextNode
from htmlnode import HTMLNode, LeafNode, ParentNode
from util import tnode_to_hnode, split_nodes_delimiter


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
    def test_wrong_delim(self):
        with self.assertRaises(Exception) as context:
            node = TextNode("This is a text with a `code` like it's the Matrix", TextType.NORMAL)
            new_nodes = split_nodes_delimiter([node], '_', TextType.CODE)
    
    def test_delim_italic(self):
        node = TextNode("This is not _Italian_, you should know that by now!", TextType.NORMAL)
        new_nodes = split_nodes_delimiter([node], '_', TextType.ITALIC)
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
        new_nodes = split_nodes_delimiter([node], '**', TextType.BOLD)
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
        new_nodes = split_nodes_delimiter([node], '**', TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("THIS IS A BOLD MESSAGE IN A BOLD NODE FROM A BALD MAN", TextType.BOLD),
            ],
            new_nodes,
        )

    def test_delim_bold_and_code(self):
        node = TextNode("It ain't much, **but** it's honest `code`", TextType.NORMAL)
        new_nodes = split_nodes_delimiter([node], '**', TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, '`', TextType.CODE)
        self.assertListEqual(
            [
                TextNode("It ain't much, ", TextType.NORMAL),
                TextNode("but", TextType.BOLD),
                TextNode(" it's honest ", TextType.NORMAL),
                TextNode("code", TextType.CODE),
            ],
            new_nodes,
        )




if __name__ == '__main__':
    unittest.main()
