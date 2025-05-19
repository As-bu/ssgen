import os, shutil

from textnode import TextType, TextNode
from htmlnode import HTMLNode, LeafNode, ParentNode
from inline_transformers import (
    split_nodes_delimiter,
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_images,
    split_nodes_links,
    text_to_textnodes,
)
from block_transformers import (
    markdown_to_blocks,
    BlockType,
    block_to_blocktype,
    markdown_to_html_node,
)

def static_to_public(static_dir='static', public_dir='public'):
    if os.path.exists(public_dir):
        shutil.rmtree(public_dir)
    os.mkdir(public_dir)
    
    for obj in os.listdir(static_dir):
        static_path = os.path.join(static_dir, obj)
        public_path = os.path.join(public_dir, obj)
    
        if os.path.isfile(static_path):
            shutil.copy(static_path, public_path)
        else:
            static_to_public(static_path, public_path)

def main():
    static_to_public()


if __name__ == '__main__':
    main()
