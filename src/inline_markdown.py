from textnode import TextNode, TextType

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
                if index % 2 == 0:
                    new_nodes.append(TextNode(x, TextType.TEXT))
                else:
                    new_nodes.append(TextNode(x, text_type))
        else:
            raise Exception("Invalid Markdown syntax.")
    return new_nodes