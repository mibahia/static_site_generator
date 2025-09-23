import re
import textwrap

from block_markdown import BlockType, block_to_block_type, markdown_to_blocks
from htmlnode import ParentNode
from split_nodes import text_to_textnode
from text_node import TextNode, TextType, text_node_to_html_node


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
    if block_type == BlockType.QUOTE:
        return quote_to_html(block)
    raise ValueError("invalid block type")


def text_to_children(text):
    children = []
    text_node_list = text_to_textnode(text)

    for text_node in text_node_list:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children


# def extract_text_from_block(block, block_type):
#     block = block.strip()
#     lines = block.split("\n")
#     if block_type == BlockType.CODE:
#         return "\n".join(lines[1:-1])

#     elif block_type == BlockType.PARAGRAPH:
#         return block

#     elif block_type in [BlockType.UNORDERED_LIST, BlockType.ORDERED_LIST]:
#         processed_lines = []
#         for line in lines:
#             if block_type == BlockType.UNORDERED_LIST:
#                 line = re.sub(r"^\* |^- |^\+ ", "", line.lstrip())
#             else:
#                 line = re.sub(r"^\d+\. ", "", line.lstrip())
#             processed_lines.append(line)
#         return processed_lines

#     elif block_type == BlockType.QUOTE:
#         processed_lines = []
#         for line in lines:
#             line = re.sub(r"^> ", "", line.lstrip())
#             processed_lines.append(line)
#         return "\n".join(processed_lines)

#     return block


# Converts a full markdown document into a HTMLNode + child
def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    nodes = []
    for block in blocks:
        node = block_to_html_node(block)
        nodes.append(node)
    return ParentNode("div", nodes, None)


# Handles paragraph
def paragraph_to_html_node(block):
    lines = block.split("\n")
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return ParentNode(tag="p", children=children)


# Handles heading
def heading_to_html(block):
    level = 0
    for char in block:
        if char == "#":
            level += 1
        else:
            break
    if level + 1 >= len(block):
        raise ValueError(f"invalid heading level: {level}")
    text = block[level + 1 :]
    children = text_to_children(text)
    return ParentNode(f"h{level}", children)


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
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("invalid quote block")
        new_lines.append(line.lstrip(">").strip())
    content = " ".join(new_lines)
    children = text_to_children(content)
    return ParentNode("blockquote", children)


# Handles unordered list
def unordered_list_to_html(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[2:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ul", html_items)


# Handles ordered list
def ordered_list_to_html(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[3:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ol", html_items)
