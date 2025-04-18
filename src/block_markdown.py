from enum import Enum

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def markdown_to_blocks(markdown):
    block = []
    
    previous_delimiter = " "

    if markdown == "":
        raise ValueError("Empty markdown")
    
    for index,  value in enumerate(markdown.split("\n")):
        if index + 1 == len(markdown.split("\n")):
            break
        if value == "```":
            block.append(markdown)
            break
        if value != "":
            string = value.strip()
            current_delimiter = string[0]
            if previous_delimiter != current_delimiter and not current_delimiter.islower():
                block.append(string)
            else:
                block[-1] = block[-1] + "\n" + string
            previous_delimiter = current_delimiter
    
    return block

def block_to_block_type(block):
    block = block.strip()
    lines = block.split("\n")

    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    if len(lines) > 1 and lines[0].startswith("```") and lines[-1].startswith("```"):
        return BlockType.CODE
    if block.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE
    if block.startswith("* "):
        for line in lines:
            if not line.startswith("* "):
                return BlockType.PARAGRAPH
        return BlockType.UNORDERED_LIST
    if block.startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                return BlockType.PARAGRAPH
        return BlockType.UNORDERED_LIST
    if block.startswith("1. "):
        i = 1
        for line in lines:
            if not line.startswith(f"{i}. "):
                return BlockType.PARAGRAPH
            i += 1
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH