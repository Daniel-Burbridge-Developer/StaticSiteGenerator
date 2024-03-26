from textnode import TextNode
from leafnode import LeafNode
from htmlnode import HTMLNode

import re

def main(): 
    # text = "This is **text** with an *italic* word and a `code block` and an ![image](https://i.imgur.com/zjjcJKZ.png) and a [link](https://boot.dev)"
    # text_to_textnodes(text)
    # markdown = (
    # """
    # This is **bolded** paragraph

    # This is another paragraph with *italic* text and `code` here
    # This is the same paragraph on a new line

    # 1. this is an ordered list
    # 2. with stuff

    # * This is a unordered list
    # * with items

    # > This is a quote

    # ``` this is a codeblock ```

    # # this is a heading with 1 hash
    
    # ### this is a heading with 3 hashs

    # ###### this is a heading with 6 hashs

    # ######### this isn't a heading it has 9 hashs and therefore is a paragraph

    # This is just a normal paragraph
    # """
    # )
    # blocks = markdown_to_blocks(markdown)

    # for block in blocks:
    #     print(block_to_block_type(block))

    heading = "### THIS IS A HEADING"
    print(heading_to_htmlnode(heading))

    code = "``` this is a codeblock ```"
    print(code_to_htmlnode(code))

    quote = "> This is a quote"
    print(quote_to_htmlnode(quote))

    # UL For sure not working
    ul = """* This is a unordered list
    * with items"""
    print(ul_to_htmlnode(ul))

    #OL For sure not working
    ol ="""1. this is an ordered list
    2. with stuff"""
    print(ol_to_htmlnode(ol))

def paragraph_to_htmlnode(block):
    pass

def heading_to_htmlnode(block):
    heading = r"^#{1,6}"
    value = re.sub(heading, "", block)
    return HTMLNode(value, tag="heading")

def code_to_htmlnode(block):
    code = r"^`{3}|`{3}$"
    value = re.sub(code, "", block)
    return HTMLNode(value, tag="code")

def quote_to_htmlnode(block):
    quote = r"^>"
    value = re.sub(quote, "", block)
    return HTMLNode(value, tag="quote")

def ul_to_htmlnode(block):
    ul = r"^\*|^\-"
    value = re.sub(ul, "", block)
    # this might need to be unordered_list not ul I'm not sure
    return HTMLNode(value, tag="ul")

def ol_to_htmlnode(block):
    ol = r"^[0-9]\."
    value = re.sub(ol, "", block)
    return HTMLNode(value, tag="ol")

def markdown_to_blocks(markdown):
    new_blocks = []
    original_blocks = markdown.split("\n\n")
    for o_block in original_blocks:
        block = ""
        lines = o_block.split("\n")
        for i, line in enumerate(lines):
            block += line.strip()
            if i != len(lines)-1:
                block += "\n"
        if block != "":
            new_blocks.append(block)
    return new_blocks

def block_to_block_type(block):
    heading = r"^#{1,6}"
    code = r"^`{3}.*`{3}$"
    quote = r"^>"
    unordered_list = r"^\*|-"
    ordered_list = r"^[0-9]\."

    if re.match(heading, block):
        return "heading"
    if re.match(code, block):
        return "code"
    if re.match(quote, block):
        return "quote"
    if re.match(unordered_list, block):
        return "unordered_list"
    if re.match(ordered_list, block):
        return "ordered_list"
    
    return "paragraph"



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