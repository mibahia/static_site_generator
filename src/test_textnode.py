import unittest

from extract_markdown import extract_markdown_images, extract_markdown_links
from split_nodes import split_nodes_delimiter, split_nodes_image, split_nodes_link
from text_node import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_in(self):
        node3 = TextNode("This is a text node", TextType.TEXT)
        node4 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node3, node4)

    def test_url(self):
        node5 = TextNode("This is a text node", TextType.TEXT)
        self.assertEqual(node5.url, None)

    def test_text_type(self):
        node6 = TextNode("This is a text node", "TEXT")
        self.assertFalse(isinstance(node6.text_type, TextType))

    def test_split_nodes_delimiter_node(self):
        node = TextNode("This is a text with a *bold block* word", TextType.TEXT)

        expected_output1 = [
            TextNode("This is a text with a ", TextType.TEXT),
            TextNode("bold block", TextType.BOLD),
            TextNode(" word", TextType.TEXT),
        ]
        output1 = split_nodes_delimiter([node], "*", TextType.BOLD)

        node1 = TextNode("This is a test with a **bold block** word", TextType.TEXT)
        node2 = TextNode("This is a text with a **bold** word", TextType.TEXT)

        expected_output2 = [
            TextNode("This is a test with a ", TextType.TEXT),
            TextNode("bold block", TextType.BOLD),
            TextNode(" word", TextType.TEXT),
            TextNode("This is a text with a ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" word", TextType.TEXT),
        ]
        output2 = split_nodes_delimiter([node1, node2], "**", TextType.BOLD)

        self.assertEqual(output1, expected_output1)
        self.assertEqual(output2, expected_output2)

    def test_extract_markdown_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        expected_output = [
            ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
            ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg"),
        ]
        output = extract_markdown_images(text)

        self.assertEqual(expected_output, output)

    def test_extract_markdown_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        expected_output = [
            ("to boot dev", "https://www.boot.dev"),
            ("to youtube", "https://www.youtube.com/@bootdotdev"),
        ]
        output = extract_markdown_links(text)

        self.assertEqual(expected_output, output)

    def test_split_nodes_links_and_images(self):
        text_node = TextNode("Text node", TextType.TEXT)
        image_node = TextNode(
            "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)",
            TextType.IMAGE,
        )
        link_node = TextNode(
            "Look at this link [to dev](https://www.dev) and [to guardian](https://www.guardian.com)",
            TextType.TEXT,
        )

        output_link = split_nodes_link([link_node, text_node])
        output_image = split_nodes_image([image_node])

        expected_output_image = [
            TextNode("This is text with a ", TextType.TEXT, None),
            TextNode("rick roll", TextType.IMAGE, "https://i.imgur.com/aKaOqIh.gif"),
            TextNode(" and ", TextType.TEXT, None),
            TextNode("obi wan", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
        ]
        expected_output_link = [
            TextNode("Look at this link ", TextType.TEXT, None),
            TextNode("to dev", TextType.LINK, "https://www.dev"),
            TextNode(" and ", TextType.TEXT, None),
            TextNode("to guardian", TextType.LINK, "https://www.guardian.com"),
            TextNode("Text node", TextType.TEXT, None),
        ]

        self.assertEqual(output_link, expected_output_link)
        self.assertEqual(output_image, expected_output_image)


if __name__ == "__main__":
    unittest.main()
