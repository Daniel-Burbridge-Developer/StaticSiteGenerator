import unittest

from parentnode import ParentNode
from htmlnode import HTMLNode

class TestHTMLStructure(unittest.TestCase):

    def test_complex_nested_structure(self):
        structure = ParentNode(tag="div", children=[
            HTMLNode(tag="h1", value="Main Title"),
            ParentNode(tag="section", children=[
                HTMLNode(tag="p", value="Paragraph 1"),
                HTMLNode(tag="p", value="Paragraph 2"),
                ParentNode(tag="ul", children=[
                    HTMLNode(tag="li", value="Item 1"),
                    HTMLNode(tag="li", value="Item 2")
                ])
            ]),
            HTMLNode(tag="img", value="", props={"src": "image.jpg", "alt": "Description"})
        ])

        expected_output = """
        <div>
            <h1>Main Title</h1>
            <section>
                <p>Paragraph 1</p>
                <p>Paragraph 2</p>
                <ul>
                    <li>Item 1</li>
                    <li>Item 2</li>
                </ul>
            </section>
            <img src="image.jpg" alt="Description" />
        </div>
        """

        self.assertEqual(structure.to_html(), expected_output)

if __name__ == '__main__':
    unittest.main()

if __name__ == '__main__':
    unittest.main()
