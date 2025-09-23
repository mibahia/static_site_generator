import os

from extract_title import extract_title
from markdown_to_block import markdown_to_html_node


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path, "r") as f:
        markdown = f.read()

    with open(template_path, "r") as f:
        template = f.read()

    html_string = markdown_to_html_node(markdown).to_html()

    title = extract_title(markdown)

    new_html = template.replace("{{ Title }}", title).replace(
        "{{ Content }}", html_string
    )

    directories = os.path.dirname(dest_path)

    if not os.path.exists(directories):
        os.makedirs(directories, exist_ok=True)

    with open(dest_path, "w") as f:
        f.write(new_html)
