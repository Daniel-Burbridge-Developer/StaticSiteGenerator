from htmlnode import HTMLNode
from leafnode import LeafNode

class ParentNode(HTMLNode):
    def __init__(self, children, tag=None, props=None):
        super().__init__(tag, children, props)

    def to_html(self):
        if self.tag == None:
            raise ValueError("no tag given")
        
        if self.children == None:
            raise ValueError("This absolutely should never happen *no children on parent node*")

        my_big_string = ""
        for child in self.children:
            my_big_string += f"<{self.tag}{self.props_to_html()}>{child.to_html()}</{self.tag}>"
        return my_big_string
        
        
