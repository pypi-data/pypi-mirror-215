Universal RSS Parser.

extra features:

- work with any rss and atom feed format.
- smart cache
- multiple rss support
- parallel parser
- parse rss podcast.

## Installation

```
pip install kolak
```

## Usage Example

```python
from kolak import Parser

url = ""
rss = Parser(url)
items = rss.parse()
print("title:", rss.title)
print("description:", rss.description)
print("permalink:", rss.permalink)
print("updated:", rss.updated)
print("author:", rss.author)
print("-"*10)
for item in items:
	print("title:", item["title"])
	print("date:", item["date"])
	print("description:",item["description"])
	print("link:",item["link"])
	print("link_image", item["link_image"])
	print("link_podcast:",item["link_podcast"])
	print("-"*10) # line
```

multiple rss processing

```
url1 = ""
url2 = ""
rss1 = Parser(url1)
items1 = rss1.parse()
rss2 = Parser(url2)
items2 = rss2.parse()
items = items1+items2
```
also you can pass raw xml feed as url input in `Parser()`.

### parse option

```python
rss.parse(limit=0, debug=False, parallel=False)

"""
limit: limitable items parse, 0 = nolimited

debug: activate debug mode. when no model is match, you will see what happened on kolak.log

parallel: use multiprocessing to parse items (experimental)
"""
```
