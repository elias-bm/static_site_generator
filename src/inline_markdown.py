from textnode import TextNode, TextType
import re

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        
        if delimiter not in old_node.text:
            new_nodes.append(old_node)
            continue
              
        split_delimiter = old_node.text.split(delimiter)

        if len(split_delimiter) % 2 != 0:
            for index, x in enumerate(split_delimiter):
                if x == "":
                    continue
                if index % 2 == 0:
                    new_nodes.append(TextNode(x, TextType.TEXT))
                else:
                    new_nodes.append(TextNode(x, text_type))
        else:
            raise Exception("Invalid Markdown syntax.")
    return new_nodes

def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def split_nodes_image(old_nodes):
    new_nodes = []

    def extract(old_node):
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            return
        if not old_node.text:
            return
        extraction = extract_markdown_images(old_node.text)
        if not extraction:
            new_nodes.append(old_node)
            return
        section = old_node.text.split(f"![{extraction[0][0]}]({extraction[0][1]})", 1)
        if section[0]:
            new_nodes.append(TextNode(section[0], TextType.TEXT))
        new_nodes.append(TextNode(extraction[0][0], TextType.IMAGE, extraction[0][1]))
        if len(section) > 1 and len(section[1]):
            section_node = TextNode(section[1], TextType.TEXT)
            extract(section_node)
    
    for old_node in old_nodes:
        extract(old_node)
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []

    def extract(old_node):
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            return
        if not old_node.text:
            return
        extraction = extract_markdown_links(old_node.text)
        if not extraction:
            new_nodes.append(old_node)
            return
        section = old_node.text.split(f"[{extraction[0][0]}]({extraction[0][1]})", 1)
        if section[0]:
            new_nodes.append(TextNode(section[0], TextType.TEXT))
        new_nodes.append(TextNode(extraction[0][0], TextType.LINK, extraction[0][1]))
        if len(section) > 1 and len(section[1]):
            section_node = TextNode(section[1], TextType.TEXT)
            extract(section_node)
    
    for old_node in old_nodes:
        extract(old_node)
    return new_nodes