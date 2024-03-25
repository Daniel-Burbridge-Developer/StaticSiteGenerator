import unittest

from leafnode import LeafNode

class TestLeafNode(unittest.TestCase):

    def test_to_html_no_tag(self):
        node = LeafNode(value="Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")

    def test_to_html_with_tag(self):
        node = LeafNode(tag="h1", value="My Heading")
        self.assertEqual(node.to_html(), "<h1>My Heading</h1>")

    def test_to_html_with_props(self):
        node = LeafNode(tag="img", value="", props={"src": "image.jpg", "alt": "My Image"})
        self.assertEqual(node.to_html(), '<img src="image.jpg" alt="My Image"></img>')  # Image is self-closing

    def test_to_html_no_value(self):
        node = LeafNode(tag="p")
        with self.assertRaises(ValueError):
            node.to_html()

if __name__ == '__main__':
    unittest.main()