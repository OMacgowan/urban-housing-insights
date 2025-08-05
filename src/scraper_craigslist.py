import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

BASE_URL = "https://toronto.craigslist.org/search/apa"
HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}

def fetch_listings(max_pages=30):
    listings = []
    page = 0
    while True:
        params = {'s': page * 120}
        response = requests.get(BASE_URL, params=params, headers=HEADERS)
        if response.status_code != 200:
            print(f"Failed to fetch page {page}")
            break

        soup = BeautifulSoup(response.text, 'html.parser')
        results = soup.find_all('li', class_='cl-static-search-result')
        print(f"Found {len(results)} listings on page {page}")

        if not results:
            print("No more listings found. Stopping pagination.")
            break

        for result in results:
            title_elem = result.find('div', class_='title')
            title = title_elem.text.strip() if title_elem else None

            price_elem = result.find('div', class_='price')
            price = price_elem.text.strip() if price_elem else None

            location_elem = result.find('div', class_='location')
            neighborhood = location_elem.text.strip() if location_elem else None

            link_elem = result.find('a')
            url = link_elem['href'] if link_elem else None

            listings.append({
                'title': title,
                'price': price,
                'neighborhood': neighborhood,
                'url': url
            })

        page += 1
        if page >= max_pages:
            print(f"Reached max page limit ({max_pages}). Stopping.")
            break

        time.sleep(2)  # Polite scraping delay

    return listings

if __name__ == "__main__":
    print("Fetching listings...")
    data = fetch_listings(max_pages=2)
    df = pd.DataFrame(data)
    df = df.drop_duplicates(subset='url')
    df.to_csv('craigslist_listings.csv', index=False)
    print(f"Saved {len(df)} listings to craigslist_listings.csv")
