import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd

# -------- PAGE CONFIG --------
st.set_page_config(
    page_title="Market Intelligence Scraper",
    layout="wide"
)

# -------- HEADER --------
st.title("📊 Market Intelligence & Web Scraper")
st.markdown("Search and extract product data like laptops, mobiles, etc.")

# -------- SIDEBAR --------
st.sidebar.header("⚙️ Controls")

search_query = st.sidebar.text_input("🔍 Search Product (e.g. laptop, phone)")

# -------- SCRAPING --------
if st.button("🚀 Start Scraping"):

    if not search_query:
        st.warning("⚠️ Please enter a search keyword")
    else:
        with st.spinner("🔍 Scraping data..."):

            base_url = "https://webscraper.io/test-sites/e-commerce/static"

            all_data = []

            try:
                response = requests.get(base_url)
                response.raise_for_status()
            except:
                st.error("❌ Failed to load website")
                st.stop()

            soup = BeautifulSoup(response.text, "html.parser")

            products = soup.find_all("div", class_="thumbnail")

            for product in products:
                name = product.find("a", class_="title").text.strip()
                price = product.find("h4", class_="price").text.strip()
                price = price.replace("$", "")

                if search_query.lower() in name.lower():
                    all_data.append({
                        "Product Name": name,
                        "Price ($)": float(price)
                    })

        # -------- RESULTS --------
        if all_data:
            df = pd.DataFrame(all_data)

            st.success(f"✅ Found {len(df)} products")

            col1, col2 = st.columns(2)
            col1.metric("📦 Total Products", len(df))
            col2.metric("💰 Avg Price", round(df["Price ($)"].mean(), 2))

            st.subheader("📋 Scraped Data")
            st.dataframe(df, use_container_width=True)

            st.subheader("📈 Price Analysis")
            st.bar_chart(df["Price ($)"])

            csv = df.to_csv(index=False).encode("utf-8")
            st.download_button(
                "📥 Download CSV",
                csv,
                "products.csv",
                "text/csv"
            )

        else:
            st.warning("⚠️ No matching products found")

# -------- FOOTER --------
st.markdown("---")
st.caption("Built using Streamlit 🚀")
