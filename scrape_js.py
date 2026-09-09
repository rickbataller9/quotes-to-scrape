from urllib.parse import urljoin
from fetch import get, write_csv
from bs4 import BeautifulSoup
import json

BASE = "http://quotes.toscrape.com/js/"

def parse_page(html):
    soup = BeautifulSoup(html, "lxml")
    raw = soup.select("script")[1].get_text()

    start = raw.find("[")
    loop_start = raw.find("for (var i in data)")
    end = raw.rfind("]", start, loop_start)

    data = raw[start: end + 1]
    quotes = json.loads(data)

    rows = []
    for i in quotes:
        rows.append({
            "text": i["text"],
            "author": i["author"]["name"],
            "tags": [tag for tag in i["tags"]]
        })

    return rows

def next_url(html, BASE):
    soup = BeautifulSoup(get(BASE), "lxml")
    next_page = None

    for i in soup.select("nav li"):
        if 'Next' in i.select_one("a").text:
            next_page = i.select_one("a")["href"]
        else:
            next_page = None

    if next_page != None:
        return urljoin(BASE, next_page)
    else:
        return None

def crawl():
    all_rows = []
    current_url = BASE

    while current_url != None:
        all_rows.extend(parse_page(get(current_url)))
        current_url = next_url(get(current_url), current_url)
    return all_rows

if __name__ == "__main__":
    write_csv(crawl(), "quotes_js.csv")

all_rows = crawl()
print(len(all_rows))