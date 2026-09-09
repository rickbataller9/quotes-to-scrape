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
    getNext = None

    # Put in the list the raw data and remove the first element and store the last --
    for i in soup.select("table tr"):
        raw.append(i)
    raw.pop(0)
    for i in raw[-1].select("a"):
        if 'Next' in i.text:
            getNext = i["href"]
        else:
            getNext = None
    raw.pop(-1)
    # --

    for i in raw[::2]:
        clean.append(i.select_one("td").text.split(" Author: "))

    for i in clean:
        i.append(raw[1::2][index])
        index += 1

    for i in clean:
        rows.append({
            "text": i[0],
            "author": i[1],
            "tags": [tag.text for tag in i[2].select("a")]
            })
    return rows, getNext

def next_url(getNext, current_url):
    if getNext != None:
        return urljoin(BASE, getNext)
    else:
        return None

def crawl():
    all_rows = []
    current_url = BASE

    while current_url != None:
        rows, getNext = parse_page(get(current_url))
        all_rows.extend(rows)
        current_url = next_url(getNext ,current_url)
    
    return all_rows

if __name__ == "__main__":
    write_csv(crawl(), "quotes_tableful.csv")

all_rows = crawl()
print(len(all_rows))
