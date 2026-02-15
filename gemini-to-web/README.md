# `gemini-to-web`

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
