import fileinput
import re
import sys

import urllib.parse
urllib.parse.uses_relative += ["gemini"]
urllib.parse.uses_netloc += ["gemini"]


base_url = sys.argv[1]

page_title = sys.argv[2]

for line in sys.stdin.read().splitlines():
    if not line.startswith("=> "):
        continue
    _, url, text = line.split(maxsplit=2)

    url = urllib.parse.urljoin(base_url, url)

    match = re.match(r"(\d{4}-\d{2}-\d{2})\s+(.*)", text)
    if not match:
        continue
    date, title = match.groups()
    print(date, url, f"{page_title} - {title}")
