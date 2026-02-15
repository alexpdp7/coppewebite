#!/bin/bash

set -eu

rm -rf target
mkdir target

cp -r source/* target/

{
    cat <<HEAD
# Welcome to my blog

HEAD
    find . -path './source/2???/??/*.gmi' -type f -print0 | uv --project .. run coppewebite-indexer source/
} >target/index.gmi

uv --project .. run coppewebite-to-rss <target/index.gmi >target/index.rss --title Example --subtitle Subtitle --base-url https://www.example.com target/

find target -name '*.gmi' -exec sh -c 'uv --project .. run coppewebite-to-html <{} >$(echo {} | sed s/.gmi/.html/)' ';'

uv --project .. run coppewebite-to-html <target/index.gmi >target/index.html --feed-href index.rss --feed-title foo
