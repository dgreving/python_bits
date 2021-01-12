from textwrap import dedent

contents = dedent("""
            This text has a number of “smart quotes”. For example there’s a “quotation with ‘nested’ quotes”.

            There’s also a second paragraph. It has a bit of text in it. But its’ text isn’t very meaningful. ‘Tis just an example of text with smart quotes.
        """).lstrip()

with open('multiline_text.txt', 'w', encoding='utf-8') as f:
    f.write(contents)
