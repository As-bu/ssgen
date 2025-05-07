import unittest

from textnode import TextNode, TextType


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


if __name__ == '__main__':
    unittest.main()
