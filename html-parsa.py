import streamlit as st
import requests
from bs4 import BeautifulSoup

st.set_page_config(page_title="記事ソース解析アプリ", layout="centered")
st.title("🔍 Web記事ソース解析アプリ")

url = st.text_input("🌐 記事URLを入力", placeholder="https://www.example.com/article/123")

if st.button("🔎 解析開始") and url:
    try:
        st.info("HTMLソースを取得中...")
        res = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        soup = BeautifulSoup(res.content, "html.parser")
        
        # よく使われる本文の親要素候補
        candidates = [
            "article",
            "section.article-body",
            "div.article-body",
            "div.c-article-body",
            "main",
            "div#main",
            "div.entry-content",
            "div#content"
        ]
        
        found = False
        for selector in candidates:
            body_el = soup.select_one(selector)
            if body_el:
                paragraphs = [p.text.strip() for p in body_el.find_all("p") if p.text.strip()]
                if paragraphs:
                    st.success(f"✅ 本文らしき部分を `{selector}` セレクタで抽出しました。")
                    st.subheader("📄 抽出結果（段落）")
                    for para in paragraphs:
                        st.write(para)
                    found = True
                    break
        
        if not found:
            st.warning("⚠️ 既知のセレクタから本文を抽出できませんでした。HTML構造が特殊かもしれません。")
            st.text("HTMLの一部抜粋:")
            st.code(soup.prettify()[:3000], language="html")

    except Exception as e:
        st.error(f"❌ エラーが発生しました: {e}")
