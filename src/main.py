from textnode import TextType, TextNode
from htmlnode import HTMLNode, LeafNode, ParentNode
from util import text_to_html

def main():
    TN1 = TextNode('This is some anchor text',
                   TextType.LINK, 'https://www.boot.dev')
    print(TN1)


if __name__ == '__main__':
    main()
