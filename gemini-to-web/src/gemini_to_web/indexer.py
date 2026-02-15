import argparse
import pathlib
import re
import sys

from gemini_to_web import parser
from gemini_to_web import html


ENTRY_ELEMENT_TITLE = re.compile(r"^(\d{4}-\d{2}-\d{2}) (.*)$")


def cli_indexer():
    argument_parser = argparse.ArgumentParser()
    argument_parser.add_argument("base_path", type=pathlib.Path)
    args = argument_parser.parse_args()

    paths = sys.stdin.read()
    paths = paths.split("\0")[:-1]

    posts = []

    for path  in paths:
        path = pathlib.Path(path)
        parsed = parser.parse(path.read_text())
        parsed = list(parsed)
        first_header_title = html.first_header_title_extractor(parsed)
        match = ENTRY_ELEMENT_TITLE.match(first_header_title)
        if match:
            posts.append((match.group(1), path.relative_to(args.base_path), match.group(2)))
    posts = sorted(posts, reverse=True)
    for date, path, title in posts:
        print(f"=> {path} {date} {title}")
