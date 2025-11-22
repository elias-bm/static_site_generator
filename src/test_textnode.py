import unittest
from textnode import TextNode, TextType, text_node_to_html_node

class TestTextNode(unittest.TestCase):
    def test_equal_when_all_fields_match(self):
        a = TextNode("hi", TextType.BOLD)
        b = TextNode("hi", TextType.BOLD, None)
        self.assertEqual(a, b)

    def test_not_equal_when_type_differs(self):
        a = TextNode("hi", TextType.BOLD)
        b = TextNode("hi", TextType.ITALIC)
        self.assertNotEqual(a, b)

class TestTextNodeToHTMLNode(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

if __name__ == "__main__":
    unittest.main()