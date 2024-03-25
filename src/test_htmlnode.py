import unittest

from htmlnode import HTMLNode   


class TestHTMLNode(unittest.TestCase):

    def test_props_to_html_empty(self):
        node = HTMLNode()  # No props
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html_single_attribute(self):
        node = HTMLNode(props={"style": "color: blue;"})
        self.assertEqual(node.props_to_html(), " stylecolor: blue;")

    def test_props_to_html_multiple_attributes(self):
        node = HTMLNode(props={"class": "my-class", "id": "section-1", "data-value": "important"})
        self.assertIn("class: my-class", node.props_to_html())
        self.assertIn("id: section-1", node.props_to_html())
        self.assertIn("data-value: important", node.props_to_html())

    def test_props_to_html_none(self):
        node = HTMLNode(props=None)
        self.assertEqual(node.props_to_html(), "")



if __name__ == "__main__":
    unittest.main()