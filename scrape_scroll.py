from fetch import get, write_csv
from urllib.parse import urljoin
import json

BASE = "http://quotes.toscrape.com/api/quotes?page=1"

def parse_page(html):
    rows = []
    data = json.loads(html)

    quotes = data["quotes"]

    for quote in quotes:
        rows.append({
            "text": quote["text"],
            "author": quote["author"]["name"],
            "tags": [tag for tag in quote["tags"]]
        })
    
    return rows

def next_url(html):
    data = json.loads(html)
    next_page = str(data["page"] + 1)
    file_name = "quotes?page="

    if data["has_next"] == True:
        next_url = urljoin(BASE, file_name + next_page)
    else:
        next_url = None
    
    return next_url

def crawl():
    all_rows = []
    current_url = BASE

    while current_url != None:
        all_rows.extend(parse_page(get(current_url, ext="json")))
        current_url = next_url(get(current_url, ext="json"))

    return all_rows

if __name__ == "__main__":
    write_csv(crawl(), "quotes_scroll.csv")

all_rows = crawl()
print(len(all_rows))
