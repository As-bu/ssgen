import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_tag(self):
        node = HTMLNode(
            'p', 'This is a value', None,
            {'class': 'text', 'href': 'https://boot.dev'},
        )
        self.assertEqual(node.props_to_html(),
                         " class='text' href='https://boot.dev'",
                         )

    def test_val(self):
        node = HTMLNode('span', 'Text is a value',)
        self.assertEqual(node.tag, 'span',)
        self.assertEqual(node.value, 'Text is a value',)
        self.assertEqual(node.children, None,)
        self.assertEqual(node.props, None,)

    def test_repr(self):
        node = HTMLNode('div', 'Valueable text', None, {'class': 'hazard'},)
        self.assertEqual(node.__repr__(),
                         "HTMLNode(div, Valueable text, children: None, {'class': 'hazard'})"
                         )

    def test_leaf_to_html_p(self):
        node = LeafNode('p', 'Hello, world!')
        self.assertEqual(node.to_html(), '<p>Hello, world!</p>')

    def test_leaf_to_html_a(self):
        node = LeafNode('a', 'Click me!', {'href': 'https://boot.dev'})
        self.assertEqual(
            node.to_html(), "<a href='https://boot.dev'>Click me!</a>")

    def test_leaf_no_tag(self):
        node = LeafNode(None, 'Text')
        self.assertEqual(node.to_html(), 'Text')

    def test_leaf_no_val(self):
        node = LeafNode('p', None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_leaf_img(self):
        node = LeafNode('img', 'Peppa pic', {
                        'src': 'pic.jpg', 'alt': 'A picture', 'width': '420'})
        self.assertEqual(
            node.to_html(), "<img src='pic.jpg' alt='A picture' width='420'>Peppa pic</img>")

    def test_to_html_with_children(self):
        child_node = LeafNode('span', 'child')
        parent_node = ParentNode('div', [child_node])
        self.assertEqual(parent_node.to_html(),
                         '<div><span>child</span></div>')

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode('b', 'grandchild')
        child_node = ParentNode('span', [grandchild_node])
        parent_node = ParentNode('div', [child_node])
        self.assertEqual(
            parent_node.to_html(),
            '<div><span><b>grandchild</b></span></div>',
        )

    def test_to_html_with_multi_children(self):
        node = ParentNode(
            'p',
            [
                LeafNode('b', 'First word'),
                LeafNode(None, 'Test text'),
                LeafNode('i', 'Last word'),
            ],
        )
        self.assertEqual(
        node.to_html(),
        '<p><b>First word</b>Test text<i>Last word</i></p>',
    )


if __name__ == '__main__':
    unittest.main()
