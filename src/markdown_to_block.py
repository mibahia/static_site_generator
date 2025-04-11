from block_markdown import markdown_to_blocks, block_to_block_type, BlockType
from htmlnode import ParentNode
from split_nodes import text_to_textnode
from text_node import text_node_to_html_node
import re
from text_node import TextNode, TextType
import textwrap

def find_heading_number(block):
    block = block.strip()
    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        match = re.match(r"#+", block)
        if match:
            return str(len(match.group()))
        return ""


def block_to_html_node(block):
    block_type = block_to_block_type(block)
    # Apply each function here
    if block_type == BlockType.PARAGRAPH:
        return paragraph_to_html_node(block)
    elif block_type == BlockType.HEADING:
        return heading_to_html(block)
    elif block_type == BlockType.CODE:
        return code_to_html_node(block)
    elif block_type == BlockType.UNORDERED_LIST:
        return unordered_list_to_html(block)
    elif block_type == BlockType.ORDERED_LIST:
        return ordered_list_to_html(block)

def text_to_children(text):
    children = []
    text_node_list = text_to_textnode(text)

    for text_node in text_node_list:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children

def extract_text_from_block(block, block_type):
    block = block.strip()
    lines = block.split("\n")
    if block_type == BlockType.CODE:
        return "\n".join(lines[1:-1])
    
    elif block_type == BlockType.PARAGRAPH:
        return block
    
    elif block_type in [BlockType.UNORDERED_LIST, BlockType.ORDERED_LIST]:
        processed_lines = []
        for line in lines:
            if block_type == BlockType.UNORDERED_LIST:
                line = re.sub(r"^\* |^- |^\+ ", "", line.lstrip())
            else:
                line = re.sub(r"^\d+\. ", "", line.lstrip())
            processed_lines.append(line)
        return processed_lines
    
    elif block_type == BlockType.QUOTE:
        processed_lines = []
        for line in lines:
            line = re.sub(r"^> ", "", line.lstrip())
            processed_lines.append(line)
        return "\n".join(processed_lines)
    
    return block


# Converts a full markdown document into a HTMLNode + child
def markdown_to_html_node(markdown):
    markdown = textwrap.dedent(markdown)
    # Split markdown into blocks
    blocks = markdown_to_blocks(markdown)
    nodes = []
    for block in blocks:
        node = block_to_html_node(block)
        nodes.append(node)
    return ParentNode(tag="div", children=nodes)

# Handles paragraph
def paragraph_to_html_node(block):
    lines = block.split("\n")
    paragraph = " ".join(lines)
    children = text_to_children(paragraph.strip())
    return ParentNode(tag="p", children=children)

# Handles heading
def heading_to_html(block):
    text = re.sub(r"^#+ ", "", block)
    children = text_to_children(text)
    heading_number = find_heading_number(block)
    return ParentNode(tag=f"h{heading_number}", children=children)

# Handles code
def code_to_html_node(block):
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("invalid code block")
    text = block[4:-3]
    raw_text_node = TextNode(text, TextType.TEXT)
    child = text_node_to_html_node(raw_text_node)
    code = ParentNode("code", [child])
    return ParentNode("pre", [code])

# Handles quote
def quote_to_html(block):
    text = extract_text_from_block(block, BlockType.QUOTE)
    children = text_to_children(text)
    return ParentNode("blockquote", children=children)

# Handles unordered list
def unordered_list_to_html(block):
    text = extract_text_from_block(block, BlockType.UNORDERED_LIST)
    nodes = []
    for item in text:
        children = text_to_children(item)
        node = ParentNode(tag="li", children=None)
        nodes.append(node)
    return ParentNode(tag="ul", children=nodes)

# Handles ordered list
def ordered_list_to_html(block):
    text = extract_text_from_block(block, BlockType.ORDERED_LIST)
    nodes = []
    for item in text:
        children = text_to_children(item)
        node = ParentNode(tag="li", children=None)
        nodes.append(node)
    return ParentNode("ol", children=nodes)


# This is the main function
def create_html_node(blocks):
    for block in blocks:
        block_to_block_type(block)
    
    pass

if __name__ == "__main__":
    md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

    list1 = """
1. First item
2. Second item
3. Third item
4. Fourth item
"""

    heading = """
### Heading level 3
"""
    # print(paragraph_to_html_node(md).to_html())
    # paragraph_to_html_node(md).to_html()
    node = markdown_to_html_node(md)
    print(node.to_html())




# Next: modify block_to_html_node to add the children