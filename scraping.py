import requests
from bs4 import BeautifulSoup

# URL der IMDb-Suche
url = "https://www.imdb.com/search/title/?title_type=feature&release_date=2025-01-01,2025-12-31&user_rating=7,"

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

    # Metadaten
    metadata = m.find_all("span", class_="sc-432a38ea-7 jTRrxk dli-title-metadata-item")
    metadatastring = ""
    for data in metadata:
        metadatastring = metadatastring + " " + data.get_text(strip=True) if metadata else "--"
    metadatastring=metadatastring[1:]
    

    # Bewertung
    rating_tag = m.find("span", class_="ipc-rating-star--rating")
    rating = rating_tag.get_text(strip=True) if rating_tag else "--"

    rating_count_tag = m.find("span", class_="ipc-rating-star--voteCount")
    rating_count = rating_count_tag.get_text(strip=True) if rating_count_tag else "--"

    print(f"Titel: {title}")
    print(f"Metadaten: {metadatastring}")
    print(f"Rating: {rating} {rating_count}")
    print("-" * 40)
print(f"Gefundene Einträge: {len(movies)}\n")