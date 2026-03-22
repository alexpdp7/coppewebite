import sys

for line in sys.stdin.read().splitlines():
    date, url, title, = line.split(maxsplit=2)
    print(f"=> {url} {date} {title}")
