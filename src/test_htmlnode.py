import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
	def test_tag(self):
		node = HTMLNode(
			'p','This is a value', None, 
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


if __name__ == '__main__':
	unittest.main()
