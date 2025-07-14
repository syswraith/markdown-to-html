import sys
from parsimonious.grammar import Grammar
from parsimonious.nodes import NodeVisitor

class Parser:
    def __init__(self):
        self.grammar = Grammar(
        r"""
        line_content        = image / progress_bar / h1 / h2 / h3 / text / empty

        image               = "![" alt_text "](" uri ")"
        progress_bar        = "[" number "]=>[" number "]"
        h1                  = "# " inline+
        h2                  = "## " inline+
        h3                  = "### " inline+
        text                = inline+
        empty               = ""

        inline              = bold_italic / bold / italic / link / wikilink / plain
        bold_italic         = "***" plain "***"
        bold                = "**" plain "**"
        italic              = "*" plain "*"
        link                = "[" link_text "](" uri ")"
        wikilink            = "[[" path "]]"
        plain               = ~r"[^\\*\[\]()\n]+"

        alt_text            = ~r"[^\[\]\(\)\n]+"
        link_text           = ~r"[^\[\]\(\)\n]+"
        uri                 = ~r"[a-zA-Z][a-zA-Z0-9+.-_]*:[^\s\)]+"
        number              = ~r"[0-9]+"
        path                = ~r"[/a-zA-Z0-9._-]+"
        """
        )

    def parse_lines(self, content):
        lines = content.splitlines()
        return [self.grammar.parse(line) for line in lines if line.strip() or line == ""]

def flatten(lst):
    out = []
    for item in lst:
        if isinstance(item, list):
            out.extend(flatten(item))
        else:
            out.append(item)
    return out

class Visitor(NodeVisitor):
    def visit_line_content(self, node, children): return children[0]
    def visit_image(self, node, children): return f'<img src="{children[3]}" alt="{children[1]}" />'
    def visit_progress_bar(self, node, children): return f'<progress value="{children[1]}" max="{children[3]}">{children[1]}%</progress>'
    def visit_h1(self, node, children): return f"<h1>{''.join(flatten(children[1:]))}</h1>"
    def visit_h2(self, node, children): return f"<h2>{''.join(flatten(children[1:]))}</h2>"
    def visit_h3(self, node, children): return f"<h3>{''.join(flatten(children[1:]))}</h3>"
    def visit_text(self, node, children): return f"<p>{''.join(flatten(children))}</p>"
    def visit_empty(self, node, children): return ""

    def visit_bold_italic(self, node, children): return f"<b><i>{children[1]}</i></b>"
    def visit_bold(self, node, children): return f"<b>{children[1]}</b>"
    def visit_italic(self, node, children): return f"<i>{children[1]}</i>"
    def visit_link(self, node, children): return f'<a href="{children[3]}">{children[1]}</a>'
    def visit_wikilink(self, node, children): return f'<a href="{children[1]}">{children[1]}</a>'
    def visit_plain(self, node, children): return node.text

    def visit_alt_text(self, node, children): return node.text
    def visit_link_text(self, node, children): return node.text
    def visit_uri(self, node, children): return node.text
    def visit_number(self, node, children): return node.text
    def visit_path(self, node, children): return node.text
    def generic_visit(self, node, children): return children or node

parser = Parser()
visitor = Visitor()

with open(sys.argv[1], 'r') as markdown_file:
    markdown_content = markdown_file.read()

html_content = [visitor.visit(tree) for tree in parser.parse_lines(markdown_content)]
html_content.insert(0, '<link href="https://cdn.jsdelivr.net/npm/uniformcss@1.0.0/dist/uniform.min.css" rel="stylesheet" />')
html_content.insert(1, '<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/sakura.css/css/sakura.css" type="text/css">')
html_content_str = "".join(html_content)

with open(f'{sys.argv[1][:-3]}.html', 'w') as html_file:
    html_file.write(html_content_str)

