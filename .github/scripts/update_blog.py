"""Write the latest Korean blog posts into README.md between the BLOG-POST-LIST markers."""
import re
import urllib.request
import xml.etree.ElementTree as ET

FEED = "https://jin3402.github.io/feed.xml"
MAX_POSTS = 5
NS = {"a": "http://www.w3.org/2005/Atom"}

with urllib.request.urlopen(FEED, timeout=30) as res:
    root = ET.fromstring(res.read())

lines = []
for entry in root.findall("a:entry", NS):
    url = entry.find("a:link", NS).get("href")
    if "/en/" in url:  # 영어판은 건너뛴다
        continue
    title = entry.find("a:title", NS).text.strip()
    date = entry.find("a:published", NS).text[:10]
    lines.append(f"- [{title}]({url}) `{date}`")
    if len(lines) == MAX_POSTS:
        break

with open("README.md", encoding="utf-8") as f:
    readme = f.read()

block = "<!-- BLOG-POST-LIST:START -->\n" + "\n".join(lines) + "\n<!-- BLOG-POST-LIST:END -->"
updated = re.sub(r"<!-- BLOG-POST-LIST:START -->.*?<!-- BLOG-POST-LIST:END -->", block, readme, flags=re.S)

with open("README.md", "w", encoding="utf-8") as f:
    f.write(updated)
print("\n".join(lines))
