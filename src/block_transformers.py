import re
from enum import Enum

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

class BlockType(Enum):
    PARA = 'paragraph'
    HEAD = 'heading'
    CODE = 'code'
    QUOTE = 'quote'
    ULIST = 'unordered list'
    OLIST = 'ordered list'

def block_to_blocktype(textblock):
    if re.search(r'\# (.*)', textblock):
        return BlockType.HEAD
    elif re.search(r'\`(.*?)\`', textblock):
        return BlockType.CODE
    elif re.search(r'\>(.*)', textblock):
        return BlockType.QUOTE
    elif re.search(r'\- (.*)', textblock):
        return BlockType.ULIST
    elif re.search(r'\d+\. (.*)', textblock):
        matches = re.findall(r'\d+. (.*)', textblock, re.MULTILINE)

        for i, match in enumerate(matches, 1):
            line = f'{i}. {match}'
            number = int(line.split('.')[0])
            if number != i:
                raise Exception("Formatting error, the list indices are not in order")
            else:
                return BlockType.OLIST
    else:
        return BlockType.PARA


