import unittest

from textnode import TextType, TextNode
from htmlnode import HTMLNode, LeafNode, ParentNode
from util import text_to_html


class test_node_to_node(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.NORMAL)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_italic(self):
        node = TextNode('Italian food is great', TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, 'i')
        self.assertEqual(html_node.value, 'Italian food is great')

    def test_link(self):
        node = TextNode('This is a link(to the past?)', TextType.LINK, 'https://boot.dev')
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, 'a')
        self.assertEqual(html_node.value, 'This is a link(to the past?)')
        self.assertEqual(
            html_node.props,
            {'href': 'https://boot.dev'},
        )

if __name__ == '__main__':
    unittest.main()
