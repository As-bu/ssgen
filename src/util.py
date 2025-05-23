import os, shutil

from pathlib import Path

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

def generate_pages_recursive(content_path, template_path, dest_path, base_path):
    print(f"Generating page from {content_path} to {dest_path} using {template_path}")

    for obj in os.listdir(content_path):
        src_path = Path(content_path) / (obj)
        dst_path = Path(dest_path) / (obj)
        tmp_path = Path(template_path)

        if os.path.isfile(src_path):
            if src_path.suffix == '.md':
                with src_path.open(mode='r', encoding='utf-8') as md_file:
                    markdown = md_file.read()
                    with tmp_path.open(mode='r', encoding='utf-8') as tmp_file:
                        template = tmp_file.read()

                        html_node = markdown_to_html_node(markdown)
                        html = html_node.to_html()

                        title = extract_title(markdown)
                        title_replace = template.replace('{{ Title }}', title)
                        html_replace = title_replace.replace('{{ Content }}', html)
                        href_replace = html_replace.replace('href="/', f'href="{base_path}')
                        src_replace = href_replace.replace('src="/', f'src="{base_path}')

                        if dst_path.parent != '':
                            os.makedirs(dst_path.parent, exist_ok=True)

                        final_dst = Path(dst_path.parent) / f'{src_path.stem}.html'
                        open_final = open(final_dst, 'w')
                        open_final.write(src_replace)

        else:
            generate_pages_recursive(src_path, template_path, dst_path, base_path)
