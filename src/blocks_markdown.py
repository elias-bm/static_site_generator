from enum import Enum
from htmlnode import ParentNode
from inline_markdown import text_to_textnodes
from textnode import text_node_to_html_node, TextNode, TextType

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
    
def block_type_to_tag(block, type):
    if type == BlockType.QUOTE:
        return "blockquote"
    if type == BlockType.UNORDERED_LIST:
        return "ul"
    if type == BlockType.ORDERED_LIST:
        return "ol"
    if type == BlockType.CODE:
        return "pre"
    if type == BlockType.HEADING:
        if block[0:6] == "######":
            return "h6"
        if block[0:5] == "#####":
            return "h5"
        if block[0:4] == "####":
            return "h4"
        if block[0:3] == "###":
            return "h3"
        if block[0:2] == "##":
            return "h2"
        if block[0] == "#":
            return "h1"
    if type == BlockType.PARAGRAPH:
        return "p"

def text_to_children(block):
    text_nodes = text_to_textnodes(block)
    html_nodes = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        html_nodes.append(html_node)
    return html_nodes

def code_block_children(block):
    block = block[4:-3]
    text_node = TextNode(block, TextType.TEXT)
    return [text_node_to_html_node(text_node)]

def unordered_list_to_children(block):
    html_nodes = []
    lines = block.split("\n")
    for line in lines:
        text = line.split("- ", 1)[1]
        children = text_to_children(text)
        html_nodes.append(ParentNode("li", children))
    return html_nodes

def ordered_list_to_children(block):
    html_nodes = []
    lines = block.split("\n")
    for line in lines:
        text = line.split(". ", 1)[1]
        children = text_to_children(text)
        html_nodes.append(ParentNode("li", children))
    return html_nodes

def heading_to_children(block):
        level = len(block) - len(block.lstrip("#"))
        text = block[level:].strip()
        return text_to_children(text)

def quote_to_children(block):
        lines = block.split("\n")
        stripped_lines = [line.lstrip(">").strip() for line in lines]
        text = " ".join(stripped_lines)
        return text_to_children(text) 

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    block_nodes = []
    for block in blocks:
        type = block_to_block_type(block)
        tag = block_type_to_tag(block, type)
        if type == BlockType.CODE:
            children = code_block_children(block)
        elif type == BlockType.UNORDERED_LIST:
            children = unordered_list_to_children(block)
        elif type == BlockType.ORDERED_LIST:
            children = ordered_list_to_children(block)
        elif type == BlockType.HEADING:
            children = heading_to_children(block)
        elif type == BlockType.QUOTE:
            children = quote_to_children(block) 
        else:
            lines = block.split("\n")
            block = " ".join(lines)
            children = text_to_children(block)
        if tag == "pre":
            code_node = ParentNode("code", children)
            pre_node = ParentNode(tag, [code_node])
            block_nodes.append(pre_node)
        else:
            parent = ParentNode(tag, children)
            block_nodes.append(parent)
    return ParentNode ("div", block_nodes)
