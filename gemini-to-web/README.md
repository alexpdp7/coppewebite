# `gemini-to-web`

## Installation

With [uv](https://docs.astral.sh/uv/):

```
uv tool install git+https://ñix.es/cgit/alex/coppewebite.git/#subdirectory=gemini-to-web
```

With [pipx](https://pipx.pypa.io/stable/):

```
pipx install git+https://ñix.es/cgit/alex/coppewebite.git/#subdirectory=gemini-to-web
```

## Usage

```console
$ uv run coppewebite-parse <<EOT
> # Hello
> 
> World.
> EOT
[{"level": 1, "heading_text": "Hello", "type": "HeadingLine"}, {"text": "", "type": "TextLine"}, {"text": "World.", "type": "TextLine"}]
```

```console
$ uv run coppewebite-to-html <<EOT
> # Hello
> 
> World.
> EOT
<html>
  <head>
    <meta charset="utf-8"/>
    <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
    <title>Hello</title>
  </head>
  <body>
    <h1>Hello</h1>
    <p>World.</p>
  </body>
</html>
```

`coppewebite-indexer` reads from standard input a `\0`-separated list of files (such as the output of `find -print0`).
`coppewebite-indexer` parses all files as gemtext, extracting the first header, and matching the header text as a Gemini page subscription entry element label.
`coppewebite-indexer` outputs a list of gemtext links, sorted in reverse chronological order, suitable for use as a Gemini page subscription.

You can use `coppewebite-indexer` to create a gemlog index automatically.

`coppewebite-to-rss` reads from standard input a gemtext file and produces the equivalent RSS to the gemtext subscription.

Refer to the [`example`](example) directory for an example.

## Writing gemtext manipulations

You can also use the parser to build tools that manipulate gemtext.
For example:

```python
# /// script
# dependencies = [
#   "gemini_to_web @ git+https://ñix.es/cgit/alex/coppewebite.git/#subdirectory=gemini-to-web",
# ]
# ///
import pathlib

from gemini_to_web import parser


for gmi in pathlib.Path("source").glob("**/*.gmi"):
    parsed = parser.parse(gmi.read_text())
    parsed = list(parsed)
    for i, line in enumerate(parsed):
        match line:
            case parser.LinkLine(url, link_name):
                if url.startswith("/") and url.endswith(".gmi"):
                    parsed[i] = parser.LinkLine(url.removesuffix(".gmi"), link_name)
            case _:
                pass
    gmi.write_text("\n".join(map(str, parsed)))
```

This script removes `.gmi` from link URLs in `source/**/*.gmi`.
This script uses script dependencies that [`uv run` can use](https://docs.astral.sh/uv/guides/scripts/#creating-a-python-script).
