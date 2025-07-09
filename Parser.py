from parsimonious.grammar import Grammar


class Parser:
    def __init__( self ):
        self.markdown_grammar = Grammar(
                r"""line_content        = image / link / wikilink / bold_italic_text / bold_text / italic_text

            image               = "![" alt_text "](" uri ")"
            link                = "[" alt_text "](" uri ")"
            wikilink            = "[[" path "]]"
            bold_italic_text    = "***" text "***"
            bold_text           = "**" text "**"
            italic_text         = "*" text "*"

            alt_text            = ~r"[^\[\]\(\)\n]+"
            uri                 = ~r"[a-zA-Z][a-zA-Z0-9+.-_]*:[^\s\)]+"
            path                = ~r"[/a-zA-Z0-9._-]+"
            text                = ~r"[^\*\n]+"
        """
        )

    def printTree( self, content ) -> str:
        lines = content.splitlines()
        for line in lines: print(self.markdown_grammar.parse(line))


content = """*italic mf*
**bold mf**
[linked mf](https://example.com)
![imaged mf](https://example.com)
[[wikilinked_mf]]"""

myParser = Parser()
myParser.printTree(content)
