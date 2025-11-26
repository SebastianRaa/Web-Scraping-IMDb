import requests
from bs4 import BeautifulSoup
from datetime import datetime

REQ_VOTES = 1000
def build_imdb_url(year_from, year_to, min_rating, genres, runtime):
    base = f"https://www.imdb.com/search/title/?title_type=feature&num_votes={REQ_VOTES},"
    base += f"&release_date={year_from}-01-01,{year_to}-12-31"
    
    if min_rating:
        base += f"&user_rating={min_rating},"

    if genres:
        base += f"&genres={genres}"

    if runtime:
        base += f"&runtime=,{runtime}"

    return base


# ---- Nutzer-Eingaben ----
print(f"IMDb Film-Suche\nEs werden nur Filme angezeigt, die mindestens {REQ_VOTES} Bewertungen haben\nSortiert nach Beliebtheit\nAlle Filter sind optional\n")

year_from = input("Startjahr (z.B. 2023): ")
if year_from == "":
    year_from = "1700"
year_to   = input("Endjahr (z.B. 2025): ")
if year_to == "":
    year_to = str(datetime.now().year)
    
min_rating = input("Mindestbewertung (0-10): ")

genres = input("Genre (z.B. action,comedy): ")
genres = genres.strip() if genres else None

runtime = input("Maximale Laufzeit (z.B. 210): ")
runtime = runtime.strip() if runtime else None

# URL bauen
url = build_imdb_url(year_from, year_to, min_rating, genres, runtime)

print("\nVerwende URL:")
print(url)
print("\n--- Starte Scraping ---\n")

# ---- Scraping ----
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    "Accept-Language": "de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7"
}

response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

movies = soup.find_all("li", class_="ipc-metadata-list-summary-item")

print(f"Gefundene Einträge: {len(movies)}\n")

for m in movies:
    # Titel
    header = m.find("h3", class_="ipc-title__text ipc-title__text--reduced")
    title = header.get_text(strip=True).split(". ", 1)[1] if header else "—"

    # Metadaten (Jahr, Dauer, Altersfreigabe)
    metadata = m.find_all("span", class_="sc-432a38ea-7 jTRrxk dli-title-metadata-item")
    meta_values = [md.get_text(strip=True) for md in metadata]
    metadatastring = ", ".join(meta_values)

    # Bewertung
    rating_tag = m.find("span", class_="ipc-rating-star--rating")
    rating = rating_tag.get_text(strip=True) if rating_tag else "--"

    rating_count_tag = m.find("span", class_="ipc-rating-star--voteCount")
    rating_count = rating_count_tag.get_text(strip=True) if rating_count_tag else "--"

    description = m.find("div", class_="ipc-html-content-inner-div")
    desc = description.get_text(strip=True) if description else "--"

    print(f"Titel: {title}")
    print(f"Metadaten: {metadatastring}")
    print(f"Rating: {rating} {rating_count}")
    print(f"Beschreibung: {desc}")
    print("-" * 40)

print(f"Gefundene Einträge: {len(movies)}\n")