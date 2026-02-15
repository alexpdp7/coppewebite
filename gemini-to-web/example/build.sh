#!/bin/bash

set -eu

rm -rf target
mkdir target

{
    cat <<HEAD
# Welcome to my blog

HEAD
    find . -path './source/2???/??/*.gmi' -type f -print0 | uv --project .. run coppewebite-indexer source/
} >target/index.gmi

cp -r source/* target/
