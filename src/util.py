import re
from textnode import TextType, TextNode
from htmlnode import HTMLNode, ParentNode, LeafNode

#Constant dict for TextType/Delim, add more as needed
DELIMITER_TO_TEXT_TYPE = {
        '**': TextType.BOLD,
        '_': TextType.ITALIC,
        '`': TextType.CODE,
}

def tnode_to_hnode(text_node):
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

    raise Exception("Unsupported text type")


def split_nodes_delimiter(old_nodes, delim, text_type):
    if delim in DELIMITER_TO_TEXT_TYPE and DELIMITER_TO_TEXT_TYPE[delim] != text_type:
        raise Exception(f"Delimiter {delim} does not match text type {text_type}")

    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.NORMAL:
            new_nodes.append(node)
            continue

        splt_node = node.text.split(delim)
        new_nodes_from_splt = []
        
        if len(splt_node) == 1:
            new_nodes.append(node)
            continue

        if len(splt_node) % 2 == 0:
            raise Exception("The node has a missing delimiter")

        for i in range(len(splt_node)):
            if splt_node[i] == '':
                continue
            if i % 2 == 0:
                new_nodes_from_splt.append(TextNode(splt_node[i], TextType.NORMAL))
            else:
                new_nodes_from_splt.append(TextNode(splt_node[i], text_type))
        
        new_nodes.extend(new_nodes_from_splt)

    return new_nodes

def extract_markdown_images(text):
    return list(re.findall(r"\!\[(.*?)\]\((.*?)\)", text))

def extract_markdown_links(text):
    return list(re.findall(r"\[(.*?)\]\((.*?)\)", text))
    


