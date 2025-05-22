import re
from textnode import TextType, TextNode
from htmlnode import HTMLNode, ParentNode, LeafNode

#Constant dict for TextType/Delim, add more as needed
DELIMITER_TO_TEXT_TYPE = {
        TextType.BOLD: '**',
        TextType.ITALIC: '_',
        TextType.CODE: '`',
}

def split_nodes_delimiter(old_nodes, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        delim = DELIMITER_TO_TEXT_TYPE[text_type]
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
                new_nodes_from_splt.append(TextNode(splt_node[i], TextType.TEXT))
            else:
                new_nodes_from_splt.append(TextNode(splt_node[i], text_type))
        
        new_nodes.extend(new_nodes_from_splt)
        #for node in new_nodes:
            #print(f"In splitter: {type(node)}, text: {getattr(node, 'text', None)}")
    return new_nodes

def extract_markdown_images(text):
    return re.findall(r'!\[(.*?)\]\((.*?)\)', text)

def extract_markdown_links(text):
    return re.findall(r'\[(.*?)\]\((.*?)\)', text)

def split_nodes_images(old_nodes): 
    new_nodes = []
    for node in old_nodes:
        extracted_images = extract_markdown_images(node.text)
        
        if extracted_images == []:
            new_nodes.append(node) 
            continue

        splt_node = re.split(r'(!\[[^\]]*\]\([^)]*\))', node.text)
        new_nodes_from_splt = []

        for splt in splt_node:
            if splt == '':
                continue
            if splt[0] == '!':
                info = extract_markdown_images(splt)
                new_nodes_from_splt.append(
                    TextNode(
                        info[0][0],
                        TextType.IMAGE,
                        info[0][1],
                    )
                )
            else:
                new_nodes_from_splt.append(
                    TextNode(
                            splt,
                            TextType.TEXT,
                    )
                )

        new_nodes.extend(new_nodes_from_splt)
        #for node in new_nodes:
            #print(f"In splitter: {type(node)}, text: {getattr(node, 'text', None)}")

    return new_nodes

def split_nodes_links(old_nodes): 
    new_nodes = []
    for node in old_nodes:
        extracted_links = extract_markdown_links(node.text)
        
        if extracted_links == []:
            new_nodes.append(node) 
            continue

        splt_node = re.split(r'(\[[^\]]*\]\([^)]*\))', node.text)
        new_nodes_from_splt = []

        for splt in splt_node:
            if splt == '':
                continue
            if splt[0] == '[':
                info = extract_markdown_links(splt)
                new_nodes_from_splt.append(
                    TextNode(
                        info[0][0],
                        TextType.LINK,
                        info[0][1],
                    )
                )
            else:
                new_nodes_from_splt.append(
                    TextNode(
                            splt,
                            TextType.TEXT,
                    )
                )

        new_nodes.extend(new_nodes_from_splt)
        #for node in new_nodes:
            #print(f"In splitter: {type(node)}, text: {getattr(node, 'text', None)}")

    return new_nodes

def text_to_textnodes(text):
    if not text:
        return []
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, TextType.CODE)
    nodes = split_nodes_images(nodes)
    nodes = split_nodes_links(nodes)
    
    return nodes

