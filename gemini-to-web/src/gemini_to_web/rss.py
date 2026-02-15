import argparse
import datetime
import pathlib
import sys

from feedgen import feed
import htmlgenerator

import gemini_to_web
from gemini_to_web import html
from gemini_to_web import parser


def cli_to_rss():
    argument_parser = argparse.ArgumentParser()
    argument_parser.add_argument("--title", default="")
    argument_parser.add_argument("--subtitle", default=None)
    argument_parser.add_argument("--base-url", default="")
    argument_parser.add_argument("base_dir", type=pathlib.Path)
    args = argument_parser.parse_args()

    fg = feed.FeedGenerator()
    fg.title(args.title)
    fg.subtitle(args.subtitle)
    fg.link(href=args.base_url, rel="self")

    input_ = sys.stdin.read()
    parsed = parser.parse(input_)
    parsed = list(parsed)

    entries = []
    for element in parsed:
        match element:
            case parser.LinkLine(url, link_name):
                match = gemini_to_web.ENTRY_ELEMENT_TITLE.match(link_name)
                if match:
                    entries.append((match.group(1), url, match.group(2)))
            case _:
                pass

    entries = sorted(entries, reverse=True)
    entries = entries[0:10]

    for (date, url, title) in entries:
        feed_entry = fg.add_entry()
        feed_entry.link(href=args.base_url + "/" + url)
        feed_entry.published(
            datetime.datetime.combine(
                datetime.date.fromisoformat(date),
                datetime.datetime.min.time(),
                tzinfo=datetime.UTC,
            )
        )
        feed_entry.title(title)
        parsed = parser.parse((args.base_dir / pathlib.Path(url).with_suffix(".gmi")).read_text())
        parsed = list(parsed)
        parsed = parsed[1:]
        content = html.to_html(parsed)
        rendered = htmlgenerator.render(content[1], {})
        rendered = html.pretty(rendered)
        feed_entry.content(rendered.encode("utf8"), type="html")

    print(fg.rss_str(pretty=True).decode("utf8"), end="")
