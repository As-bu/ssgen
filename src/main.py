import os, shutil, sys

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
from util import copy_paste_dir, generate_pages_recursive

if len(sys.argv) > 1:
    base_path = sys.argv[1]
else:
    base_path = '/'

static_path = f'./static'
public_path = f'./docs'
content_path = f'./content'
template_path = f'template.html'


def main():
    print("Deleting public directory...")
    if os.path.exists(public_path):
        shutil.rmtree(public_path)

    print("Copying static files to public...")
    copy_paste_dir(static_path, public_path)

    print("Generating Page...")
    generate_pages_recursive(content_path, template_path, public_path, base_path)


if __name__ == '__main__':
    main()
