from textnode import TextNode
from leafnode import LeafNode

import re

def main(): 
    dummy_node = TextNode("The women *who I adore* is Stacey", "text", url="https://theloveofmylife.com")
    print(split_nodes_delimiter([dummy_node], "*", "italic"))
    dummy_image_text ="This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) doodahdiii doo doo and ![another](https://i.goingagain.com/zjjcJKZ.png)"
    print(extract_markdown_images(dummy_image_text))
    dummy_link_text = "This is text with a [link](https://www.example.com) and another one doodahdiii doo doo and [another](https://i.goingagain.com/zjjcJKZ.png)"
    print(extract_markdown_links(dummy_link_text))

    image_node = TextNode(dummy_image_text, "text")
    print(split_nodes_image([image_node]))
    link_node = TextNode(dummy_link_text, "text")
    print(split_nodes_link([link_node]))

def text_node_to_html_node(text_node):

    value = text_node.value
    tag = text_node.text_type
    url = text_node.url

    if text_node is not None:
        if tag == "text":
            return LeafNode(value)
        if tag == "bold":
            return LeafNode(value, tag="b")
        if tag == "italic":
            return LeafNode(value, tag="i")
        if tag == "code":
            return LeafNode(value, tag="code")
        if tag == "link":
            return LeafNode(value, tag="a", props={"href": f"{url}"})
        if tag == "image":
            return LeafNode("", tag="img", props={"src": f"{url}", "alt": f"{value}"})

    raise Exception

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []

    for node in old_nodes:
        if not isinstance(node, TextNode):
            new_nodes.append(node)
            continue
        split_node = node.text.split(delimiter)
        if len(split_node) % 2 == 0:
            raise ValueError("Invalid markdown, formatted section not closed")
        for i, section in enumerate(split_node):
            if i % 2 == 1:
                if len(section) > 0:
                    new_nodes.append(TextNode(section, text_type))
            else :
                if len(section) > 0:
                    new_nodes.append(TextNode(section, "text"))

    return new_nodes

def split_nodes_image(old_nodes):
    new_nodes = []

    for node in old_nodes:
        if not isinstance(node, TextNode):
            new_nodes.append(node)
            continue
        tupples = extract_markdown_images(node.text)
        for tup in tupples:
            split_node = node.text.split(f"![{tup[0]}]({tup[1]})",1)
            if len(split_node) % 2 == 1:
                raise ValueError("Invalid Image Link")
            if len(split_node[0]) > 0:
                new_nodes.append(TextNode(split_node[0], "text"))
            new_nodes.append(TextNode(tup[0], "image", tup[1]))
            if len(split_node[1]) > 0:
                new_nodes.append(TextNode(split_node[1], "text"))

                
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []

    for node in old_nodes:
        if not isinstance(node, TextNode):
            new_nodes.append(node)
            continue
        tupples = extract_markdown_links(node.text)
        for tup in tupples:
            split_node = node.text.split(f"[{tup[0]}]({tup[1]})",1)
            if len(split_node) % 2 == 1:
                raise ValueError("Invalid Link")
            if len(split_node[0]) > 0:
                new_nodes.append(TextNode(split_node[0], "text"))
            new_nodes.append(TextNode(tup[0], "link", tup[1]))
            if len(split_node[1]) > 0:
                new_nodes.append(TextNode(split_node[1], "text"))

                
    return new_nodes

def extract_markdown_images(text):
    return re.findall(r"!\[(.*?)\]\((.*?)\)", text)

def extract_markdown_links(text):
    return re.findall(r"\[(.*?)\]\((.*?)\)", text)

if __name__ == "__main__":
    main()