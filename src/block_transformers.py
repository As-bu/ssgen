import re
from enum import Enum

from textnode import TextType, TextNode, text_node_to_html_node
from htmlnode import HTMLNode, ParentNode, LeafNode
from inline_transformers import text_to_textnodes


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

def block_to_blocktype(text):
    if re.search(r'\#+ (.*)', text):
        return BlockType.HEAD
    elif re.search(r'^\`\`\`(.*)', text):
        return BlockType.CODE
    elif re.search(r'\>(.*)', text):
        return BlockType.QUOTE
    elif re.search(r'\- (.*)', text):
        return BlockType.ULIST
    elif re.search(r'\d+\. (.*)', text):
        matches = re.findall(r'\d+. (.*)', text, re.MULTILINE)

        for i, match in enumerate(matches, 1):
            line = f'{i}. {match}'
            number = int(line.split('.')[0])
            if number != i:
                raise Exception("Formatting error, the list indices are not in order")
            else:
                return BlockType.OLIST
    else:
        return BlockType.PARA


def markdown_to_html_node(markdown):
    blocks = [b for b in markdown_to_blocks(markdown) if b.strip()]
    #print(blocks)
    child_nodes = []
    for block in blocks:
        html_node = block_to_html_node(block)
        if html_node is not None:
            child_nodes.append(html_node)
    return ParentNode('div', child_nodes, None)
        
def block_to_html_node(block):
    block_type = block_to_blocktype(block)
    if block_type == BlockType.PARA:
        return paragraph_to_html_node(block)
    if block_type == BlockType.HEAD:
        return heading_to_html_node(block)
    if block_type == BlockType.CODE:
        return code_to_html_node(block)
    if block_type == BlockType.QUOTE:
        return quote_to_html_node(block)
    if block_type == BlockType.ULIST:
        return ulist_to_html_node(block)
    if block_type == BlockType.OLIST:
        return olist_to_html_node(block)
    raise ValueError("invalid block type")

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    child_nodes = []
    for text_node in text_nodes:
        #print(text_node.text)
        child_node = text_node_to_html_node(text_node)
        child_nodes.append(child_node)
        #for text_node in text_nodes:
            #if text_node.text is None:
                #print("Found text_node with None text!")
    return child_nodes

def paragraph_to_html_node(block):
    lines = block.split('\n')
    paragraph = ' '.join(lines).strip()
    if not paragraph:
        return None
    children = text_to_children(paragraph)
    return ParentNode('p', children)

def heading_to_html_node(block):
    depth = 0
    for char in block:
        if char == '#':
            depth += 1
        else:
            break
    if depth + 1 >= len(block):
        raise ValueError(f"invalid heading at level: {level}")
    text = block[depth + 1:]
    children = text_to_children(text)
    return ParentNode(f'h{depth}', children)

def code_to_html_node(block):
    if not block.startswith('```') or not block.endswith('```'):
        raise ValueError("invalid formatting")
    text = block[4:-3]
    code_text_node = TextNode(text, TextType.TEXT)
    child = text_node_to_html_node(code_text_node)
    code_node = ParentNode('code', [child])
    return ParentNode('pre', [code_node])

def quote_to_html_node(block):
    lines = block.split('\n')
    new_lines = []
    for line in lines:
        if not line.startswith('>'):
            raise ValueError("invalid quote block")
        new_lines.append(line.lstrip('>').strip())
    text = ' '.join(new_lines)
    children = text_to_children(text)
    return ParentNode('blockquote', children)

def olist_to_html_node(block):
    items = block.split('\n')
    html_items = []
    for item in items:
        text = item[3:]
        children = text_to_children(text)
        html_items.append(ParentNode('li', children))
    return ParentNode('ol', html_items)

def ulist_to_html_node(block):
    items = block.split('\n')
    html_items = []
    for item in items:
        text = item[2:]
        children = text_to_children(text)
        html_items.append(ParentNode('li', children))
    return ParentNode('ul', html_items)

def extract_title(markdown):
    header = re.findall(r'\# (.*)', markdown)
    if header == []:
        raise Exception("no header found")
    return header[0].strip('#')
