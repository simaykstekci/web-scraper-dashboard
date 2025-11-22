import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

st.title("Yazılım Blog Arama Dashboard")

search_term = st.text_input("Aramak istediğin yazılım dili:", "")


sites = [
    {
        "name": "Python Blog",
        "url": "https://www.python.org/blogs/",
        "selector": "ul.list-recent-posts li a"
    },
    {
        "name": "Dev.to Python",
        "url": "https://dev.to/t/python",
        "selector": "h2 a"
    },
    {
        "name": "Dev.to Java",
        "url": "https://dev.to/t/java",
        "selector": "h2 a"
    }
]

all_posts = []


for site in sites:
    try:
        response = requests.get(site["url"])
        soup = BeautifulSoup(response.text, "lxml")
        for post in soup.select(site["selector"]):
            title = post.get_text(strip=True)
            link = post.get("href")
            if link.startswith("/"):
                link = site["url"].rstrip("/") + link
            all_posts.append({
                "site": site["name"],
                "title": title,
                "link": link,
                "scraped_at": datetime.utcnow().isoformat()
            })
    except Exception as e:
        st.write(f"{site['name']} veri çekilemedi: {e}")

df = pd.DataFrame(all_posts)


if search_term and not df.empty:
    df = df[df["title"].str.contains(search_term, case=False, na=False)]


if not df.empty:
    st.subheader(f"{len(df)} başlık bulundu")
    st.dataframe(df)
    df["title_length"] = df["title"].str.len()
    st.subheader("Başlık Uzunluğu Grafiği")
    st.bar_chart(df["title_length"])
else:
    st.write("Hiç başlık bulunamadı.")


