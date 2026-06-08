import requests
from bs4 import BeautifulSoup
import os
import time

os.makedirs("documents", exist_ok=True)

sources = [
    ("01_dining_locations", "https://housing.ucla.edu/dining-locations", "official"),
    ("02_discover_dining", "https://housing.ucla.edu/discover-dining-2025", "official"),
    ("03_asucla_guide", "https://asucla.ucla.edu/ucla/ucla-dining-hall", "student_guide"),
    ("04_best_nation_2023", "https://adminvc.ucla.edu/news-views/fall-2023/ucla-dining-named-best-nation-seventh-time", "news"),
    ("05_best_nation_2025", "https://adminvc.ucla.edu/news-views/summer-2025/ucla-dining-remains-no-1-nation", "news"),
    ("08_niche_reviews", "https://www.niche.com/colleges/university-of-california-los-angeles/reviews/?topic=food", "reviews"),
    ("09_yelp_bruin_plate", "https://www.yelp.com/biz/bruin-plate-los-angeles", "reviews"),
    ("10_yelp_de_neve", "https://www.yelp.com/biz/de-neve-dining-los-angeles", "reviews"),
    ("11_yelp_epicuria", "https://www.yelp.com/biz/epicuria-at-covel-los-angeles", "reviews"),
    ("12_dining_portal", "https://dining.ucla.edu", "official"),
]

headers = {"User-Agent": "Mozilla/5.0"}

def clean(soup):
    for tag in soup(["nav", "header", "footer", "script", "style", "aside"]):
        tag.decompose()
    text = soup.get_text(separator="\n")
    lines = [l.strip() for l in text.splitlines() if len(l.strip()) > 40]
    return "\n".join(lines)

for filename, url, source_type in sources:
    try:
        resp = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(resp.text, "html.parser")
        text = clean(soup)
        with open(f"documents/{filename}.txt", "w") as f:
            f.write(f"source_url: {url}\nsource_type: {source_type}\n\n{text}")
        print(f"saved {filename}")
        time.sleep(1)
    except Exception as e:
        print(f"failed {filename}: {e}")

print("done - check documents/ folder, some sites may need manual saving")
