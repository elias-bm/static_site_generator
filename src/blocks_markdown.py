from enum import Enum

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def markdown_to_blocks(markdown):
    blocks = []
    block_pieces = markdown.split("\n\n")
    for block_piece in block_pieces:
        if block_piece == "":
            continue
        blocks.append(block_piece.strip())
    return blocks

def block_to_block_type(block):
    pieces = block.split()
    
    if len(pieces[0]) <= 6:
        for piece in pieces[0]:
            if piece != "#":
                break
        else:
            return BlockType.HEADING

    if block[0:3] == "```" and block[-3:] == "```":
        return BlockType.CODE

    if block[0] == ">":
        return BlockType.QUOTE

    if block[0:2] == "- ":
        return BlockType.UNORDERED_LIST
    
    if block[0:3] == "1. ":
        return BlockType.ORDERED_LIST

    else:
        return BlockType.PARAGRAPH