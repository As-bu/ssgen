from textnode import TextType, TextNode
from htmlnode import HTMLNode, ParentNode, LeafNode

class text_to_html:
    def text_node_to_html_node(text_node):
        if text_node.text_type == TextType.NORMAL:
            return LeafNode(None, text_node.text)

        if text_node.text_type == TextType.BOLD:
            return LeafNode('b', text_node.text)

        if text_node.text_type == TextType.ITALIC:
            return LeafNode('i', text_node.text)

        if text_node.text_type == TextType.CODE:
            return LeafNode('code', text_node.text)

        if text_node.text_type == TextType.LINK:
            return LeafNode('a', text_node.text, {'href': text_node.url})

        if text_node.text_type == TextType.IMAGE:
            return LeafNode('img', '', {'src': text_node.url, 'alt': text_node.text})

        raise Exception('Unsupported text type')
