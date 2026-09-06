from urllib.parse import urljoin
from fetch import get, write_csv
from bs4 import BeautifulSoup

BASE = "https://quotes.toscrape.com/"


def parse_page(html):
    """One page of HTML -> list of dicts. Knows nothing about pagination."""
    soup = BeautifulSoup(html, "lxml")
    rows = []
    for card in soup.select(".quote"):
        rows.append({
            "text": card.select_one(".text").text,
            "author": card.select_one(".author").text,
            "tags": [tag.text for tag in card.select(".tags .tag")],          # a real list
        })
    return rows

def next_url(html, current_url):
    """Return absolute URL of the next page, or None if there isn't one."""
    soup = BeautifulSoup(html, "lxml")
    try:
        getNext = soup.select_one(".next a")["href"]
    except TypeError:
        return None
    
    new_url = urljoin(BASE, getNext)
    return new_url

def crawl(start=BASE, limit=None):
    url, pages, all_rows = start, 0, []
    while url:
        html = get(url)
        all_rows.extend(parse_page(html))
        pages += 1
        if limit and pages >= limit:
            break
        url = next_url(html, url)
    return all_rows

if __name__ == "__main__":
    write_csv(crawl(BASE, None), "quotes_plain.csv")

all_rows = crawl(BASE, None)
print(len(all_rows))
    