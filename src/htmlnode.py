class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError('to_html method not implemented')

    def props_to_html(self):
        props = ''
        if self.props is None:
            return props

        for x in self.props:
            props += f" {x}='{self.props[x]}'"

        return props

    def __repr__(self):
        return f'HTMLNode({self.tag}, {self.value}, children: {self.children}, {self.props})'


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if not self.value:
            raise ValueError('All leaf nodes must have a value')

        if not self.tag:
            return self.value

        html_prop = self.props_to_html()

        return f'<{self.tag}{html_prop}>{self.value}</{self.tag}>'


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if not self.tag:
            raise ValueError('All parent nodes must have a tag')

        if not self.children:
            raise ValueError('Children nodes are required for a parent node')

        html_prop = self.props_to_html()
        html_children = ''
        for child in self.children:
            html_children += child.to_html()

        return f'<{self.tag}{html_prop}>{html_children}</{self.tag}>'
