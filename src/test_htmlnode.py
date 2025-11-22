import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_basic(self):
        n = HTMLNode(tag="a", props={"href":"https://x.com", "target":"_blank"})
        out = n.props_to_html()
        self.assertIn(' href="https://x.com"', out)
        self.assertIn(' target="_blank"', out)

    def test_props_to_html_none(self):
        n = HTMLNode(props=None)
        self.assertEqual(n.props_to_html(), "")

    def test_repr(self):
        n = HTMLNode("p", "hi", None, {"class":"lead"})
        s = repr(n)
        self.assertIn("HTMLNode(", s)
        self.assertIn("tag=", s)
        self.assertIn("value=", s)

    def test_constructor_fields(self):
        n = HTMLNode("p", "v", ["child"], {"id":"x"})
        self.assertEqual(n.tag, "p")
        self.assertEqual(n.value, "v")
        self.assertEqual(n.children, ["child"])
        self.assertEqual(n.props, {"id":"x"})

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

if __name__ == "__main__":
    unittest.main()