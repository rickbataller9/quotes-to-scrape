import csv, hashlib, time, requests
from pathlib import Path

CACHE = Path("cache"); CACHE.mkdir(exist_ok=True)
HEADERS = {"User-Agent": "Mozilla/5.0 (learning project)"}
FIELDS = ["text", "author", "tags"]


def get(url, delay=1.0, ext="html"):
    key = CACHE / f"{hashlib.md5(url.encode()).hexdigest()}.{ext}"
    if key.exists():
        return key.read_text(encoding="utf-8")
    r = requests.get(url, headers=HEADERS, timeout=10)
    r.raise_for_status()
    r.encoding = "utf-8"
    key.write_text(r.text, encoding="utf-8")
    time.sleep(delay)
    return r.text


def write_csv(rows, path):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        for row in rows:
            row = dict(row)
            row["tags"] = "|".join(row.get("tags", []))
            w.writerow(row)
    print(f"{path}: {len(rows)} rows")