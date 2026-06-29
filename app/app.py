import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd

st.set_page_config(page_title="Market Intelligence Scraper", layout="wide")

st.title("📊 Market Intelligence & Web Scraper")
st.markdown("Extract real product data like laptops, mobiles, etc.")

st.sidebar.header("⚙️ Controls")

category = st.sidebar.selectbox(
    "Select Category",
    ["laptops", "phones"]
)

pages = st.sidebar.slider("Number of Pages", 1, 5, 1)

if st.button("🚀 Start Scraping"):

    with st.spinner("Scraping real product data..."):

        base_url = f"https://webscraper.io/test-sites/e-commerce/static/{category}?page={{}}"

        all_data = []

        for page in range(1, pages + 1):
            url = base_url.format(page)

            response = requests.get(url)
            soup = BeautifulSoup(response.text, "html.parser")

            products = soup.find_all("div", class_="thumbnail")

            for product in products:
                name = product.find("a", class_="title").text.strip()
                price = product.find("h4", class_="price").text.strip()
                price = price.replace("$", "")

                all_data.append({
                    "Product Name": name,
                    "Price ($)": float(price),
                    "Page": page
                })

        if all_data:
            df = pd.DataFrame(all_data)

            st.success(f"Found {len(df)} products")

            col1, col2 = st.columns(2)
            col1.metric("Total Products", len(df))
            col2.metric("Average Price", round(df["Price ($)"].mean(), 2))

            st.dataframe(df, use_container_width=True)

            st.subheader("📈 Price Analysis")
            st.bar_chart(df["Price ($)"])

            csv = df.to_csv(index=False).encode("utf-8")
            st.download_button(
                "Download CSV",
                csv,
                "products.csv",
                "text/csv"
            )

        else:
            st.warning("No products found")
