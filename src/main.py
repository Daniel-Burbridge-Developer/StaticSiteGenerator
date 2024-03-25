from textnode import TextNode
from leafnode import LeafNode

import re

def main(): 
    text = "This is **text** with an *italic* word and a `code block` and an ![image](https://i.imgur.com/zjjcJKZ.png) and a [link](https://boot.dev)"
    text_to_textnodes(text)

def text_to_textnodes(text):
    nodes = []
    nodes.append(TextNode(text, "text"))
    nodes = split_nodes_delimiter(nodes, "**", "bold")
    nodes = split_nodes_delimiter(nodes, "*", "italic")
    nodes = split_nodes_delimiter(nodes, "`", "code")
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)

    print(nodes)
    return nodes

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
        if node.text_type != "text":
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

    # print(new_nodes)
    return new_nodes

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if not isinstance(node, TextNode):
            new_nodes.append(node)
            continue
        if node.text_type != "text":
            new_nodes.append(node)
            continue
        tupples = extract_markdown_images(node.text)
        if len(tupples) == 0:
            new_nodes.append(node)
            continue
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
        if node.text_type != "text":
            new_nodes.append(node)
            continue
        tupples = extract_markdown_links(node.text)
        if len(tupples) == 0:
            new_nodes.append(node)
            continue
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