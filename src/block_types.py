from enum import Enum

class BlockTypes(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def block_to_bloc_type(markdown_block):

    if markdown_block == "":
        raise ValueError("Empty block")

    if "#" in markdown_block[0:5]:
        return BlockTypes.HEADING
    if "```" == markdown_block[0:3] and "```" == markdown_block[-3:]:
        return BlockTypes.CODE
    if ">" == markdown_block[0]:
        for i in markdown_block.split("\n"):
            if not i.startswith(">"):
                raise ValueError(f"Missing > in line: {i}")
        return BlockTypes.QUOTE
    if "*" == markdown_block[0] or "-" == markdown_block[0]:
        for i in markdown_block.split("\n"):
            if not i.startswith("* ") and not i.startswith("- "):
                raise ValueError(f"Missing * or - in line: {i}")
        return BlockTypes.UNORDED_LIST
    if markdown_block[0].isdigit():
        for index, value in enumerate(markdown_block.split("\n")):
            if index + 1 != int(value[0]):
                raise ValueError(f"Count not incremental on line: {value}")
            if ". " != value[1:3]:
                raise ValueError(f"Syntax error on line: {value}")
        return BlockTypes.ORDERED_LIST
    return BlockTypes.PARAGRAPH

if __name__ == "__main__":
    print(block_to_bloc_type(block))

    
    