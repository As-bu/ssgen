import os, shutil

from htmlnode import HTMLNode, LeafNode, ParentNode
from block_transformers import (
    markdown_to_blocks,
    BlockType,
    block_to_blocktype,
    markdown_to_html_node,
    extract_title,
)

def copy_paste_dir(src, dst):
    if not os.path.exists(dst):
        os.mkdir(dst)
    
    for obj in os.listdir(src):
        src_path = os.path.join(src, obj)
        dst_path = os.path.join(dst, obj)
    
        if os.path.isfile(src_path):
            shutil.copy(src_path, dst)
        else:
            copy_paste_dir(src_path, dst_path)

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    
    from_file = open(from_path, 'r')
    markdown = from_file.read()
    from_file.close()
    
    template_file = open(template_path, 'r')
    template = template_file.read()
    template_file.close()

    html_node = markdown_to_html_node(markdown)
    html = html_node.to_html()
    
    title = extract_title(markdown)
    finished_html = template.replace('{{ Title }}', title)
    finished_html = finished_html.replace('{{ Content }}', html)

    if os.path.dirname(os.path.dirname(dest_path)) != '':
        os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    
    dest_file = open(dest_path, 'w')
    dest_file.write(finished_html)









    




