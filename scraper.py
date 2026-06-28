import requests
from bs4 import BeautifulSoup
import pandas as pd

base_url = "http://books.toscrape.com/catalogue/page-{}.html"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

all_data = []

for page in range(1, 6):
    url = base_url.format(page)
    print(f"Scraping page {page}...")

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(f"Failed on page {page}")
        continue

    soup = BeautifulSoup(response.text, "html.parser")
    books = soup.find_all("article", class_="product_pod")

    for book in books:
        name = book.h3.a["title"]
        price = book.find("p", class_="price_color").text

        # Clean price (remove £)
        price = price.replace("£", "").strip()

        all_data.append({
            "Product Name": name,
            "Price (£)": price,
            "Page": page
        })

# Save to CSV
df = pd.DataFrame(all_data)
df.to_csv("clean_products.csv", index=False)

print("✅ Clean data saved successfully!")