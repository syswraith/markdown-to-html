from parsimonious.grammar import Grammar


markdown_grammar = Grammar(
r"""
    line_content        = image / link / bold_italic_text / bold_text / italic_text

    image               = "![" alt_text "](" source ")"
    link                = "[" alt_text "](" source ")"
    bold_italic_text    = "***" text "***"
    bold_text           = "**" text "**"
    italic_text         = "*" text "*"

    alt_text            = ~r"[^\[\]\(\)\n]+"
    text                = ~r"[^\*\n]+"
    source              = ~r"[a-zA-Z][a-zA-Z0-9+.-]*:[^\s\)]+"
"""
)


content = """*italic mf*
**bold mf**
[linked_mf](https://example.com)
![imaged_mf](https://example.com)""".splitlines()


for line in content: print(markdown_grammar.parse(line))
