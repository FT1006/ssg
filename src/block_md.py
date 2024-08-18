from enum import Enum

class Block_Type(Enum):
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"
    PARAGRAPH = "paragraph"

def markdown_to_blocks(markdown):
    if not isinstance(markdown, str):
        raise TypeError("Input must be a string")
    blocks = markdown.split("\n\n")
    filtered_blocks = []
    for block in blocks:
        if block == "":
            continue
        block = block.strip()
        filtered_blocks.append(block)
    return filtered_blocks

def block_to_block_type(block):
    lines = block.split("\n")
    if (
        block.startswith("#") 
        or block.startswith("##") 
        or block.startswith("###") 
        or block.startswith("####") 
        or block.startswith("#####") 
        or block.startswith("######")
    ):
        return Block_Type.HEADING
    if len(lines) > 1 and lines[0].startswith("```") and lines[-1].startswith("```"):
        return Block_Type.CODE
    if block.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return Block_Type.PARAGRAPH
        return Block_Type.QUOTE
    if block.startswith("* ") or block.startswith("- "):
        for line in lines:
            if not line.startswith("* ") and not line.startswith("- "):
                return Block_Type.PARAGRAPH
        return Block_Type.UNORDERED_LIST
    if block.startswith("1. "):
        for i in range(len(lines)):
            if not lines[i].startswith(f"{i+1}. "):
                return Block_Type.PARAGRAPH
        return Block_Type.ORDERED_LIST
    return Block_Type.PARAGRAPH