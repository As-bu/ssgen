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
from util import copy_paste_dir, generate_page

static_path = "./static"
public_path = "./public"
content_path = "./content"
template_path = "./template.html"
content = ['index.md',
    'blog/glorfindel/index.md',
    'blog/tom/index.md',
    'blog/majesty/index.md',
    'contact/index.md',
           ]
dest = ['index.html',
    'blog/glorfindel/index.html',
    'blog/tom/index.html',
    'blog/majesty/index.html',
    'contact/index.html',
           ]
def main():
    print("Deleting public directory...")
    if os.path.exists(public_path):
        shutil.rmtree(public_path)

    print("Copying static files to public...")
    copy_paste_dir(static_path, public_path)

    print("Generating Page...")
    level = 0
    for md in content:
        generate_page(
            os.path.join(content_path, md),
            template_path,
            os.path.join(public_path, dest[level]),
        )
        level += 1


if __name__ == '__main__':
    main()
