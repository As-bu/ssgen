import re
from textnode import TextType, TextNode
from htmlnode import HTMLNode, ParentNode, LeafNode


def markdown_to_blocks(markdown):
    text_blocks = []
    splt_markdown = markdown.split('\n\n')
    for block in splt_markdown:
        if block == '' or block == '"""':
            continue
        cleanup = block.strip()
        text_blocks.append(cleanup)

    return text_blocks

