import unittest

from textnode import TextNode


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "bold")
        self.assertEqual(node, node2)

    def test_eq_not_equal(self):
        node = TextNode("This is a text node", "italic")
        node2 = TextNode("This is a text node", "bold")
        self.assertNotEqual(node, node2)

    def test_eq_With_URL(self):
        node = TextNode("This is a text node", "italic", "some url")
        node2 = TextNode("This is a text node", "italic", "some url")
        node3 = TextNode("This is a text node", "bold" "some other url")
        self.assertEqual(node, node2)
        self.assertNotEqual(node, node3)



if __name__ == "__main__":
    unittest.main()