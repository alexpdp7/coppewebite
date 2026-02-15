#!/bin/bash

# This script demonstrates how to use coppewebite to build a blog from gemtext, including RSS feeds.
#
# This scripts uses "uv --process .. run coppewebite-*" to run the coppewebite commands from the source in this repository.
# If you have installed coppewebite following the instructions, then you can replace that by only "coppewebite-*".

set -eu

# Ensure target is an empty directory.
rm -rf target
mkdir target

# Copy all content to target.
cp -r source/* target/

# Create an index page with all posts, from a header followed by the results of coppewebite-indexer.
{
    cat <<HEAD
# Welcome to my blog

## Subtitle

HEAD
    find . -path './source/2???/??/*.gmi' -type f -print0 | uv --project .. run coppewebite-indexer source/
} >target/index.gmi

# Generate an RSS feed.
uv --project .. run coppewebite-to-rss <target/index.gmi >target/index.rss https://www.example.com target/

# Convert all gemtext to HTML.
find target -name '*.gmi' -exec sh -c 'uv --project .. run coppewebite-to-html <{} >$(echo {} | sed s/.gmi/.html/)' ';'

# Convert index.gmi again, linking the RSS feed.
uv --project .. run coppewebite-to-html <target/index.gmi >target/index.html --feed-href index.rss --feed-title foo
