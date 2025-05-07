import unittest

from textnode import TextNode, TextType, tnode_to_hnode
from htmlnode import HTMLNode, ParentNode, LeafNode


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode('This is a text node', TextType.TEXT)
        node2 = TextNode('This is a text node', TextType.TEXT)
        self.assertEqual(node, node2)

    def test_neq_type(self):
        node = TextNode('This is a text node', TextType.TEXT)
        node2 = TextNode('This is a text node', TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_neq_val(self):
        node = TextNode('This is a text node', TextType.ITALIC)
        node2 = TextNode('This is not a text node', TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_url(self):
        node = TextNode('This is a link', TextType.LINK, 'https://boot.dev')
        node2 = TextNode('This is a link', TextType.LINK, 'https://boot.dev')
        self.assertEqual(node, node2)

    def test_repr(self):
        node = TextNode('This is a link', TextType.TEXT, 'https://boot.dev')
        self.assertEqual(node.__repr__(),
                         "TextNode(This is a link, text, https://boot.dev)"
                         )


class test_node_to_node(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
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


if __name__ == '__main__':
    unittest.main()
