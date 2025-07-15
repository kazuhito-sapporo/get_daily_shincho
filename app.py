import streamlit as st
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import os

# --- 保存ディレクトリ ---
SAVE_DIR = "./saved_articles"
os.makedirs(SAVE_DIR, exist_ok=True)

# --- デイリー新潮：記事一覧取得（BeautifulSoup） ---
def get_daily_shincho_articles():
    url = "https://www.dailyshincho.jp/"
    res = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(res.content, "html.parser")
    elements = soup.select("a:has(p.c-list-article__caption)")
    articles = []
    for el in elements:
        title_el = el.select_one("p.c-list-article__caption")
        title = title_el.text.strip() if title_el else ""
        link = el.get("href")
        if title and link and link.startswith("https"):
            articles.append({"title": title, "url": link})
    return articles

# --- 本文取得（BeautifulSoup）---
def get_article_body_bs4(url):
    try:
        res = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        soup = BeautifulSoup(res.content, "html.parser")
        body_el = soup.select_one("article")
        if not body_el:
            return "（本文が見つかりません）"
        paragraphs = [p.text.strip() for p in body_el.find_all("p") if p.text.strip()]
        return "\n".join(paragraphs)
    except Exception as e:
        return f"（本文取得に失敗しました: {e}）"

# --- Streamlit UI ---
st.set_page_config(page_title="複数メディア記事ビューア", layout="centered")
st.title("🗞️ 複数メディア対応記事ビューア（Cloud対応）")

media = st.radio("📰 メディアを選択", ["デイリー新潮", "文春オンライン"], horizontal=True)

if media == "デイリー新潮":
    if st.button("🗞️ 新潮記事一覧を取得"):
        with st.spinner("記事一覧を取得中..."):
            st.session_state.articles = get_daily_shincho_articles()
            st.session_state.body = ""
            st.session_state.selected_title = ""

    if "articles" in st.session_state and st.session_state.articles:
        titles = [a["title"] for a in st.session_state.articles]
        selected_title = st.selectbox("📰 記事を選択", titles)
        selected_article = next((a for a in st.session_state.articles if a["title"] == selected_title), None)

        if selected_article:
            st.markdown(f"🔗 [記事リンクを開く]({selected_article['url']})")
            if st.button("📖 本文を表示"):
                with st.spinner("本文を取得中..."):
                    st.session_state.body = get_article_body_bs4(selected_article["url"])
                st.session_state.selected_title = selected_title

elif media == "文春オンライン":
    url = st.text_input("🔗 記事URLを入力してください（例: https://bunshun.jp/articles/-/XXXXX）")
    if url:
        if st.button("📖 本文を表示"):
            with st.spinner("本文を取得中..."):
                st.session_state.body = get_article_body_bs4(url)
            st.session_state.selected_title = "文春オンライン記事"

# --- 本文表示＆保存 ---
if "body" in st.session_state and st.session_state.body:
    st.subheader("📄 記事本文")
    st.write(st.session_state.body)

    if st.button("💾 テキスト保存"):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_title = st.session_state.selected_title[:30].replace(" ", "_").replace("/", "_").replace(":", "_")
        filename = os.path.join(SAVE_DIR, f"{safe_title}_{timestamp}.txt")
        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"{st.session_state.selected_title}\n{url if media == '文春オンライン' else selected_article['url']}\n\n{st.session_state.body}")
        st.success(f"✅ 保存しました: {filename}")
