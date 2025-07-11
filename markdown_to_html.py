from parsimonious.grammar import Grammar
from parsimonious.nodes import NodeVisitor


class Parser:
    def __init__( self ):
        self.markdown_grammar = Grammar(
        r"""line_content        = image / link / wikilink / progress_bar / bold_italic_text / bold_text / italic_text

            image               = "![" alt_text "](" uri ")"
            link                = "[" alt_text "](" uri ")"
            wikilink            = "[[" path "]]"
            progress_bar        = "[" number "]=>[" number "]"
            bold_italic_text    = "***" text "***"
            bold_text           = "**" text "**"
            italic_text         = "*" text "*"

            alt_text            = ~r"[^\[\]\(\)\n]+"
            uri                 = ~r"[a-zA-Z][a-zA-Z0-9+.-_]*:[^\s\)]+"
            number              = ~r"[0-9]+"
            path                = ~r"[/a-zA-Z0-9._-]+"
            text                = ~r"[^\*\n]+"
        """
        )

    def parse_lines( self, content ) -> str:
        lines = content.splitlines()
        return [self.markdown_grammar.parse(line) for line in lines]

class Visitor( NodeVisitor ):
    def visit_line_content(self, node, children): return children[0]
    def visit_line_content(self, node, children): return children[0]

    def visit_image(self, node, children): return f'<img src="{children[3]}" alt="{children[1]}" />'
    def visit_link(self, node, children): return f'<a href="{children[3]}">{children[1]}</a>'
    def visit_wikilink(self, node, children): return f'<a href="{children[1]}">{children[1]}</a>'
    def visit_progress_bar(self, node, children): return f'<progress value="{children[1]}" max="{children[3]}">{children[1]}%</progress>'
    def visit_bold_italic_text(self, node, children): return f'<b><i>{children[2]}</i></b>'
    def visit_bold_text(self, node, children): return f'<b>{children[1]}</b>'
    def visit_italic_text(self, node, children): return f'<i>{children[1]}</i>'

    def visit_alt_text(self, node, children): return node.text
    def visit_uri(self, node, children): return node.text
    def visit_path(self, node, children): return node.text
    def visit_number(self, node, children): return node.text
    def visit_text(self, node, children): return node.text

    def generic_visit(self, node, children): return children or node


with open('./example.md', 'r') as markdown_file:
    markdown_content = markdown_file.read()

#content = """*italic mf*
#**bold mf**
#[linked mf](https://example.com)
#[10]=>[100]
#![imaged mf](https://example.com)
#[[wikilinked_mf]]"""


parser = Parser()
visitor = Visitor()

# for tree in parser.parse_lines(markdown_content):
#     print(visitor.visit(tree))


html_content = "\n<br/>\n".join([visitor.visit(tree) for tree in parser.parse_lines(markdown_content)])

with open('./example.html', 'w') as html_file:
    html_file.write(html_content)



