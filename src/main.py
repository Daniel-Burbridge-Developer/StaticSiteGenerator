from textnode import TextNode
from leafnode import LeafNode
from htmlnode import HTMLNode
from parentnode import ParentNode

import re
import os
import shutil

def main(): 
    # clean_root()
    # recursive_copy("static")
    generate_page('./content/index.md', 'template.html', './public/index.html')


def clean_root():
    if os.path.exists("./public"):
        shutil.rmtree("./public")
    os.mkdir("public")  

def recursive_copy(directory):
    working_dir = os.path.join("./", directory+"/")
    if not os.path.exists(f"./public/{directory}"):
        os.mkdir(f"./public/{directory}")
    dirs = (os.listdir(working_dir))
    for d in dirs:
        if os.path.isfile(f"{working_dir}{d}"):
            shutil.copy(f"{working_dir}{d}", f"./public/{directory}/{d}")
        else:
            recursive_copy(f'{directory}/{d}')

# probably breaks if the h1 isn't a top-level node... but, like, surely that'll never happen. :)
def extract_title(markdown):
    nodes = markdown_to_html_node(markdown).children

    for node in nodes:
        if node.tag == "h1":
            return node.value
        
    raise Exception("markdown must contain h1 tag")

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    title_finder = r"(\{\{ Title \}\}?)"
    content_finder = r"(\{\{ Content \}\})"
    write_to_file = ""
    with open(f"{from_path}") as markdown:
        rm = markdown.read()
        with open(f"{template_path}") as template:
            tm =template.read()
            base_node = markdown_to_html_node(rm)
            html = base_node.to_html()
            title = extract_title(rm)
            write_to_file = re.sub(tm, title_finder, title)
            write_to_file = re.sub(write_to_file, content_finder, html)

            try:
                with open(dest_path, "w") as t:
                    t.write(write_to_file)
                    t.flush()  # Ensure data is written to disk
            except OSError as e:
                print(f"Error writing to file: {e}")



# this should all not be in main, let's hide it down here for now.
def markdown_to_html_node(markdown):
    base_node = ParentNode("", tag="div")
    base_node.children = []
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        block_type = block_to_block_type(block)
        node = None
        if block_type == "paragraph":
            node = paragraph_to_htmlnode(block)
        if block_type == "heading":
            node = heading_to_htmlnode(block)
        if block_type == "code":
            node = code_to_htmlnode(block)
        if block_type == "quote":
            node = quote_to_htmlnode(block)
        if block_type == "unordered_list":
            node = ul_to_htmlnode(block)
        if block_type == "ordered_list":
            node = ol_to_htmlnode(block)
        

        # THIS WOULD BE MUCH BETTER TAKEN CARE OF WITH A RECURSIVE THINGY
        # ALSO FAIRLY SURE THIS IS BROKEN
        text_nodes = text_to_textnodes(node.value)
        if len(text_nodes) > 0:
            if node.children is None:
                node.children = []
            for tn in text_nodes:
                node.children.append(text_node_to_html_node(tn))
        if node.children is not None:
            for n in node.children:
                text_nodes = text_to_textnodes(n.value)
                if len(text_nodes) > 0:
                    if n.children is None:
                        n.children = []
                    for tn in text_to_textnodes(n.value):
                        n.children.append(text_node_to_html_node(tn))
        base_node.children.append(node)
            
    return base_node

def paragraph_to_htmlnode(block):
    return HTMLNode(block, tag="p")

def heading_to_htmlnode(block):
    heading_capture = r"^(#{1,6}?)"
    captured = re.findall(heading_capture, block)
    count_of_hash = len(captured[0])
    value = re.sub(captured[0], "", block)
    return HTMLNode(value, tag=f"h{count_of_hash}")

def code_to_htmlnode(block):
    code = r"^`{3}|`{3}$"
    value = re.sub(code, "", block)
    return HTMLNode(value, tag="pre")

def quote_to_htmlnode(block):
    quote = r"^>"
    value = re.sub(quote, "", block)
    return HTMLNode(value, tag="blockquote")

def ul_to_htmlnode(block):
    ul_capture = r"(\* ?)|(\- ?)"
    ul_node = HTMLNode("", tag="ul")
    ul_node.children = []

    subbed = re.sub(ul_capture, "<li>", block)
    sublists = subbed.split("<li>")
    
    if len(sublists) > 0:
        for sl in (sublists):
            ul_node.children.append(HTMLNode(sl, tag="li"))
        return ul_node

    return ul_node

def ol_to_htmlnode(block):
    ol_capture = r"([0-9]\.{1}?)"
    ol_node = HTMLNode("", tag="ol")
    ol_node.children = []

    subbed = re.sub(ol_capture, "<li>", block)
    sublists = subbed.split("<li>")

    if len(sublists) > 0:
        for sl in (sublists):
            ol_node.children.append(HTMLNode(sl, tag="li"))
        return ol_node
    
    return ol_node

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

    return nodes

def text_node_to_html_node(text_node):

    value = text_node.text
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

def generate_page_dummy(markdown):

    base_node = markdown_to_html_node(markdown)
    html = base_node.to_html()
    print(html)

def supersecretdeletemefunction():
    return """# The Unparalleled Majesty of "The Lord of the Rings"

[Back Home](/)

![LOTR image artistmonkeys](/images/rivendell.png)

> "I cordially dislike allegory in all its manifestations, and always have done so since I grew old and wary enough to detect its presence.
> I much prefer history, true or feigned, with its varied applicability to the thought and experience of readers.
> I think that many confuse 'applicability' with 'allegory'; but the one resides in the freedom of the reader, and the other in the purposed domination of the author."

In the annals of fantasy literature and the broader realm of creative world-building, few sagas can rival the intricate tapestry woven by J.R.R. Tolkien in *The Lord of the Rings*. You can find the [wiki here](https://lotr.fandom.com/wiki/Main_Page).

## Introduction

This series, a cornerstone of what I, in my many years as an **Archmage**, have come to recognize as the pinnacle of imaginative creation, stands unrivaled in its depth, complexity, and the sheer scope of its *legendarium*. As we embark on this exploration, let us delve into the reasons why this monumental work is celebrated as the finest in the world.

## A Rich Tapestry of Lore

One cannot simply discuss *The Lord of the Rings* without acknowledging the bedrock upon which it stands: **The Silmarillion**. This compendium of mythopoeic tales sets the stage for Middle-earth's history, from the creation myth of Eä to the epic sagas of the Elder Days. It is a testament to Tolkien's unparalleled skill as a linguist and myth-maker, crafting:

1. An elaborate pantheon of deities (the `Valar` and `Maiar`)
2. The tragic saga of the Noldor Elves
3. The rise and fall of great kingdoms such as Gondolin and Númenor

```
print("Lord")
print("of")
print("the")
print("Rings")
```

## The Art of **World-Building**

### Crafting Middle-earth
Tolkien's Middle-earth is a realm of breathtaking diversity and realism, brought to life by his meticulous attention to detail. This world is characterized by:

- **Diverse Cultures and Languages**: Each race, from the noble Elves to the sturdy Dwarves, is endowed with its own rich history, customs, and language. Tolkien, leveraging his expertise in philology, constructed languages such as Quenya and Sindarin, each with its own grammar and lexicon.
- **Geographical Realism**: The landscape of Middle-earth, from the Shire's pastoral hills to the shadowy depths of Mordor, is depicted with such vividness that it feels as tangible as our own world.
- **Historical Depth**: The legendarium is imbued with a sense of history, with ruins, artifacts, and lore that hint at bygone eras, giving the world a lived-in, authentic feel.

## Themes of *Timeless* Relevance

### The *Struggle* of Good vs. Evil

At its heart, *The Lord of the Rings* is a timeless narrative of the perennial struggle between light and darkness, a theme that resonates deeply with the human experience. The saga explores:

- The resilience of the human (and hobbit) spirit in the face of overwhelming odds
- The corrupting influence of power, epitomized by the One Ring
- The importance of friendship, loyalty, and sacrifice

These universal themes lend the series a profound philosophical depth, making it a beacon of wisdom and insight for generations of readers.

## A Legacy **Unmatched**

### The Influence on Modern Fantasy

The shadow that *The Lord of the Rings* casts over the fantasy genre is both vast and deep, having inspired countless authors, artists, and filmmakers. Its legacy is evident in:

- The archetypal "hero's journey" that has become a staple of fantasy narratives
- The trope of the "fellowship," a diverse group banding together to face a common foe
- The concept of a richly detailed fantasy world, which has become a benchmark for the genre

## Conclusion

As we stand at the threshold of this mystical realm, it is clear that *The Lord of the Rings* is not merely a series but a gateway to a world that continues to enchant and inspire. It is a beacon of imagination, a wellspring of wisdom, and a testament to the power of myth. In the grand tapestry of fantasy literature, Tolkien's masterpiece is the gleaming jewel in the crown, unmatched in its majesty and enduring in its legacy. As an Archmage who has traversed the myriad realms of magic and lore, I declare with utmost conviction: *The Lord of the Rings* reigns supreme as the greatest legendarium our world has ever known.

Splendid! Then we have an accord: in the realm of fantasy and beyond, Tolkien's creation is unparalleled, a treasure trove of wisdom, wonder, and the indomitable spirit of adventure that dwells within us all."""


if __name__ == "__main__":
    main()