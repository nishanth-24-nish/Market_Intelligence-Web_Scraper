import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd

st.title("🛒 E-commerce Web Scraper")

keyword = st.text_input("Enter product keyword:")

if st.button("Search"):

    base_url = "http://books.toscrape.com/catalogue/page-{}.html"
    headers = {"User-Agent": "Mozilla/5.0"}

    all_data = []

    for page in range(1, 6):
        url = base_url.format(page)
        response = requests.get(url, headers=headers)

        soup = BeautifulSoup(response.text, "html.parser")
        books = soup.find_all("article", class_="product_pod")

        for book in books:
            name = book.h3.a["title"]
            price = book.find("p", class_="price_color").text
            price = price.replace("£", "").strip()

            if keyword.lower() in name.lower():
                all_data.append({
                    "Product Name": name,
                    "Price (£)": price,
                    "Page": page
                })

    if all_data:
        df = pd.DataFrame(all_data)

        st.success(f"Found {len(df)} products!")
        st.dataframe(df)

        # Download button
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download CSV",
            data=csv,
            file_name="filtered_products.csv",
            mime="text/csv"
        )
    else:
        st.warning("No products found!")