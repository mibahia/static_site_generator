from block_markdown import markdown_to_blocks, block_to_block_type, BlockType
from htmlnode import ParentNode
from split_nodes import text_to_textnode
from text_node import text_node_to_html_node
import re

def find_heading(block):
    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        match = re.match(r"#+", block)
        if match:
            return str(len(match.group()))
        return ""
    

def outer_find_html_tag(block_type):
    if block_type == BlockType.QUOTE:
        return "blockquote"
    if block_type == BlockType.UNORDERED_LIST:
        return "ul"
    if block_type == BlockType.ORDERED_LIST:
        return "ol"
    if block_type == BlockType.CODE:
        return "code"
    if block_type == BlockType.HEADING:
        return "h"
    if block_type == BlockType.PARAGRAPH:
        return "p"

def inner_find_html_tag(block_type):
    if block_type == BlockType.UNORDERED_LIST or block_type == BlockType.ORDERED_LIST:
        return "li"
    if block_type == BlockType.CODE:
        return "pre"


# TO DO: add the proper child logic step 3
# And resolve the code block special logic
def block_to_html_node(block, block_type):
    if block_type == BlockType.QUOTE:
        tag = outer_find_html_tag(block_type)
        text = extract_text_from_block(block, block_type)
        children = text_to_children(text)
        return ParentNode(tag=tag, children=children)
    if block_type == BlockType.UNORDERED_LIST:
        tag = outer_find_html_tag(block_type)
        text = extract_text_from_block(block, block_type)
        children = text_to_children(text)
        return ParentNode(tag=tag, children=children)
    if block_type == BlockType.ORDERED_LIST:
        tag = outer_find_html_tag(block_type)
        text = extract_text_from_block(block, block_type)
        children = text_to_children(text)
        return ParentNode(tag=tag, children=children)
    if block_type == BlockType.HEADING:
        heading = outer_find_html_tag(block_type)
        heading_number = find_heading(block)
        tag = f"{heading}{heading_number}"
        text = extract_text_from_block(block, block_type)
        children = text_to_children(text)
        return ParentNode(tag=tag, children=children)
    if block_type == BlockType.PARAGRAPH:
        tag = outer_find_html_tag(block_type)
        text = extract_text_from_block(block, block_type)
        children = text_to_children(text)
        return ParentNode(tag=tag, children=children)
    if block_type == BlockType.CODE:
        tag = outer_find_html_tag(block_type)
        return ParentNode(tag=tag, children=None)



def text_to_children(text):
    children = []
    text_node_list = text_to_textnode(text)

    for text_node in text_node_list:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)

    if not children:
        return None
    return children

def extract_text_from_block(block, block_type):
    block = block.strip()
    lines = block.split("\n")
    if block_type == BlockType.CODE:
        
        return "\n".join(lines[1:-1])
    
    elif block_type == BlockType.HEADING:
        return re.sub(r"^#+ ", "", block)
        
    
    elif block_type == BlockType.PARAGRAPH:
        return block
    
    elif block_type in [BlockType.UNORDERED_LIST, BlockType.ORDERED_LIST]:
        processed_lines = []
        for line in lines:
            if block_type == BlockType.UNORDERED_LIST:
                line = re.sub(r"^\* |^- ", "", line.lstrip())
            else:
                line = re.sub(r"^\d+\. ", "", line.lstrip())
            processed_lines.append(line)
        return "\n".join(processed_lines)
    
    elif block_type == BlockType.QUOTE:
        processed_lines = []
        for line in lines:
            line = re.sub(r"^> ", "", line.lstrip())
            processed_lines.append(line)
        return "\n".join(processed_lines)
    
    return block
    

# This is the main function
def create_html_node(blocks):
    for block in blocks:
        block_to_block_type(block)
    
    pass

# Converts a full markdown document into a HTMLNode + child
def markdown_to_html_node(markdown):
    # Split markdown into blocks
    blocks = markdown_to_blocks(markdown)
    pass


if __name__ == "__main__":
    md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""
    text = extract_text_from_block(md, BlockType.PARAGRAPH)
    print(text)
    Node = block_to_html_node(md, BlockType.PARAGRAPH)
    print(Node.to_html())

# Next: modify block_to_html_node to add the children