from urllib.parse import urljoin
from fetch import get, write_csv
from bs4 import BeautifulSoup

BASE = "http://quotes.toscrape.com/tableful/"

def parse_page(html):
    soup = BeautifulSoup(html, "lxml")
    index = 0
    raw = []
    clean = []
    rows = []

    # Put in the list the raw data and remove the first element and store the last --
    for i in soup.select("table tr"):
        raw.append(i)
    raw.pop(0)
    getNext = raw[-1].select_one("a")["href"]
    raw.pop(-1)
    # --

    for i in raw[::2]:
        clean.append(i.select_one("td").text.split(" Author: "))

    for i in clean:
        i.append(raw[1::2][index])
        index += 1

    for i in clean:
        rows.append({
            "quote": i[0],
            "author": i[1],
            "tags": [tag.text for tag in i[2].select("a")]
            })
    return rows, getNext
    