import typing

import htmlgenerator
from lxml import etree, html

from gemini_to_web import parser


def first_header_title_extractor(parsed: list[parser.GemElement]):
    heading_lines = [element for element in parsed if isinstance(element, parser.HeadingLine)]
    if heading_lines:
        return heading_lines[0].heading_text


def to_html(parsed: list[parser.GemElement], title_extractor=first_header_title_extractor, extra_head=None):
    body = []
    building_element = None
    building_content = None

    def close(body, building_element, building_content):
        if building_element and building_content:
            body.append(building_element(*building_content))
        return (body, None, None)

    head = []

    if title_extractor:
       head.append(htmlgenerator.TITLE(title_extractor(parsed)))

    if extra_head:
        head += extra_head

    for item in parsed:
        match item:
            case parser.HeadingLine(level, heading_text):
                if building_element:
                    body, building_element, building_content = close(body, building_element, building_content)
                headers = [htmlgenerator.H1, htmlgenerator.H2, htmlgenerator.H3]
                body.append(headers[level-1](heading_text))
            case parser.QuoteLine(text):
                # https://geminiprotocol.net/docs/gemtext.gmi#blockquotes says:
                #
                # > The quoted content is written as a single long line [...]
                if building_element:
                    body, building_element, building_content = close(body, building_element, building_content)
                body.append(htmlgenerator.BLOCKQUOTE(text))
            case parser.PreformattingToggleLine(alt_text):
                if building_element == htmlgenerator.PRE:
                    assert not alt_text, f"Closing preformatting toggle line with alt text {alt_text}"
                    body, building_element, building_content = close(body, building_element, building_content)
                else:
                    body, building_element, building_content = close(body, building_element, building_content)
                    building_element = htmlgenerator.PRE
                    building_content = ""
            case parser.PreformattedTextLine(text):
                assert building_element == htmlgenerator.PRE
                building_content += text
                building_content += "\n"
            case parser.TextLine(""):
                if building_element:
                    body, building_element, building_content = close(body, building_element, building_content)
            case parser.TextLine(text):
                if building_element == htmlgenerator.P:
                    building_content += [htmlgenerator.BR(), text]
                    continue
                elif building_element is not None and building_element != htmlgenerator.P:
                    body, building_element, building_content = close(body, building_element, building_content)
                building_element = htmlgenerator.P
                building_content = [text]
            case parser.LinkLine(url, link_name):
                if building_element == htmlgenerator.P:
                    building_content += [htmlgenerator.BR(), htmlgenerator.A(link_name, href=url)]
                    continue
                elif building_element is not None and building_element != htmlgenerator.P:
                    body, building_element, building_content = close(body, building_element, building_content)
                building_element = htmlgenerator.P
                building_content = [htmlgenerator.A(link_name, href=url)]
            case parser.ListItem(text):
                if building_element == htmlgenerator.UL:
                    building_content.append(htmlgenerator.LI(text))
                    continue
                elif building_element is not None and building_element != htmlgenerator.UL:
                    body, building_element, building_content = close(body, building_element, building_content)
                building_element = htmlgenerator.UL
                building_content = [htmlgenerator.LI(text)]
            case _:
                assert False, f"unknown element {item}"

    close(body, building_element, building_content)
    html = htmlgenerator.HTML(
        htmlgenerator.HEAD(*head),
        htmlgenerator.BODY(*body),
    )
    return html


def pretty(s):
    return etree.tostring(html.fromstring(s), pretty_print=True).decode("utf8")


def cli_to_html():
    import argparse
    import sys

    argument_parser = argparse.ArgumentParser()
    argument_parser.add_argument("--feed-title")
    argument_parser.add_argument("--feed-href")
    args = argument_parser.parse_args()

    assert not bool(args.feed_title) ^ bool(args.feed_href), "--feed-title and --feed-href must be both present or both absent"

    extra_head = []
    if args.feed_href:
        extra_head.append(htmlgenerator.LINK(rel="alternate", type="application/rss+xml", title=args.feed_title, href=args.feed_href))

    input_ = sys.stdin.read()
    gemtext = parser.parse(input_)
    gemtext = list(gemtext)
    html = to_html(gemtext, extra_head=extra_head)
    rendered = htmlgenerator.render(html, {})
    rendered = pretty(rendered)
    print(rendered)
