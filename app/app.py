import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Market Intelligence Scraper",
    layout="wide"
)

# ---------------- HEADER ----------------
st.title("📊 Market Intelligence & Web Scraper")
st.markdown("Extract product names and prices from an e-commerce site with ease.")

# ---------------- SIDEBAR ----------------
st.sidebar.header("⚙️ Controls")

keyword = st.sidebar.text_input("🔍 Enter Keyword")
pages = st.sidebar.slider("📄 Number of Pages", 1, 10, 5)

# ---------------- MAIN ACTION ----------------
if st.button("🚀 Start Scraping"):

    if not keyword:
        st.warning("⚠️ Please enter a keyword")
    else:
        with st.spinner("🔍 Scraping data... Please wait..."):

            base_url = "http://books.toscrape.com/catalogue/page-{}.html"
            headers = {
                "User-Agent": "Mozilla/5.0"
            }

            all_data = []

            # -------- MULTI-PAGE LOOP --------
            for page in range(1, pages + 1):
                url = base_url.format(page)

                try:
                    response = requests.get(url, headers=headers)
                    response.raise_for_status()
                except:
                    st.error(f"❌ Failed to load page {page}")
                    continue

                soup = BeautifulSoup(response.text, "html.parser")
                books = soup.find_all("article", class_="product_pod")

                for book in books:
                    name = book.h3.a["title"]
                    price = book.find("p", class_="price_color").text
                    price = price.replace("£", "").strip()

                    if keyword.lower() in name.lower():
                        all_data.append({
                            "Product Name": name,
                            "Price (£)": float(price),
                            "Page": page
                        })

        # ---------------- RESULTS ----------------
        if all_data:
            df = pd.DataFrame(all_data)

            st.success(f"✅ Found {len(df)} matching products!")

            # -------- METRICS --------
            col1, col2 = st.columns(2)
            col1.metric("📦 Total Products", len(df))
            col2.metric("💰 Avg Price", round(df["Price (£)"].mean(), 2))

            # -------- TABLE --------
            st.subheader("📋 Scraped Data")
            st.dataframe(df, use_container_width=True)

            # -------- CHART --------
            st.subheader("📈 Price Distribution")
            st.bar_chart(df["Price (£)"])

            # -------- DOWNLOAD --------
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Download CSV",
                data=csv,
                file_name="filtered_products.csv",
                mime="text/csv"
            )

        else:
            st.warning("⚠️ No matching products found!")

# ---------------- FOOTER ----------------
st.markdown("---")
st.caption("Built using Streamlit | Market Intelligence Project 🚀")
