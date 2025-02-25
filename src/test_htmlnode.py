import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode, text_node_to_html_node
from text_node import TextNode, TextType

class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        html_node = HTMLNode(tag="p", value="this is a test")
        html_node1 = HTMLNode(tag="p", value="this is a test")

        self.assertEqual(html_node, html_node1)
    
    def test_in(self):
        html_node2 = HTMLNode(tag="a", value="this is a test")
        html_node3 = HTMLNode(tag="p", value="this is a test")

        self.assertNotEqual(html_node2, html_node3)

    def test_props_to_html(self):
        props = {"href": "https://www.google.com", "target": "_blank"}
        html_node2 = HTMLNode(tag="a", value="this is a test", props=props)

        props_html = html_node2.props_to_html()

        expected_output = ' href="https://www.google.com" target="_blank"'

        self.assertEqual(props_html, expected_output)

    def test_leaf_eq(self):
        leaf_node = LeafNode(tag="a", value="this is a test")
        leaf_node1 = LeafNode(tag="a", value="this is a test")
        

        self.assertEqual(leaf_node, leaf_node1)
    
    def test_to_html(self):
        leaf_node3 = LeafNode(tag="a", value="Click me!", props={"href": "https://www.google.com"})

        expected_output = '<a href="https://www.google.com">Click me!</a>'

        self.assertEqual(leaf_node3.to_html(), expected_output)

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

    def test_to_html_many_children(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>",
        )

    def test_headings(self):
        node = ParentNode(
            "h2",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<h2><b>Bold text</b>Normal text<i>italic text</i>Normal text</h2>",
        )
    
    def test_text_node_to_html_node(self):
        node = TextNode("Hello, world!", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        assert html_node.tag == None
        assert html_node.value == "Hello, world!"
        assert html_node.props == {}