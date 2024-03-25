from htmlnode import HTMLNode
class LeafNode(HTMLNode):
    def __init__(self, value, tag=None, children=None, props=None):
        super().__init__(value,tag,children,props)

    
    def to_html(self):
        if self.value == None:
            raise ValueError
        
        if self.tag == None:
            return self.value
        
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
        
