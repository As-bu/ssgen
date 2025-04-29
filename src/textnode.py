from enum import Enum

class TextType(Enum):
	NORMAL = 'normal'
	BOLD = 'bold'
	ITALIC = 'italic'
	CODE = 'code'
	LINK = 'link'
	IMAGE = 'image'

class TextNode:
	def __init__(self, text, text_type, url=None):
		self.text = text
		self.text_type = text_type
		self.url = url

	def __eq__(self, Node_2):
		if self.text == Node_2.text and self.text_type == Node_2.text_type and self.url == Node_2.url:
			return True
		return False

	def __repr__(self):
		return f'TextNode({self.text}, {self.text_type.value}, {self.url})'
