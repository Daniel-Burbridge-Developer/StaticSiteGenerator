from textnode import TextNode
from leafnode import LeafNode

def main(): 
    dummyNode = TextNode("Stacey", "Bold", "https://theloveofmylife.com")
    print(dummyNode)

def text_node_to_html_node(text_node):
    print(text_node)

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
        pass

    return new_nodes

if __name__ == "__main__":
    main()