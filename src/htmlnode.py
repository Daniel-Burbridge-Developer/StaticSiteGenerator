class HTMLNode:
    def __init__(self, value=None, tag=None, children=None, props=None):
        self.value = value
        self.tag = tag
        self.children = children
        self.props = props or {}

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        returnString = ""

        if not self.props:
            return returnString
        
        for key, value in self.props.items():
            returnString += f' {key}="{value}"'

        return returnString

    def __repr__(self):
        return f"Tag: {self.tag}, Value: {self.value}, Children: {self.children}, Props: {self.props}"


