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
