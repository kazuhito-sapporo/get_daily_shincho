import streamlit as st
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime
import time
import os

# --- 保存ディレクトリ ---
SAVE_DIR = "./saved_articles"
os.makedirs(SAVE_DIR, exist_ok=True)

# --- Seleniumドライバ設定 ---
def get_driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920x1080")
    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=options)

# --- デイリー新潮 記事一覧取得 ---
def get_daily_shincho_articles():
    driver = get_driver()
    driver.get("https://www.dailyshincho.jp/")
    time.sleep(5)

    articles = []
    elements = driver.find_elements(By.CSS_SELECTOR, "a:has(p.c-list-article__caption)")

    for elem in elements:
        try:
            title_elem = elem.find_element(By.CSS_SELECTOR, "p.c-list-article__caption")
            title = title_elem.text.strip()
            link = elem.get_attribute("href")
            if title and link:
                articles.append({"title": title, "url": link})
        except:
            continue

    driver.quit()
    return articles

# --- 本文取得（Selenium）---
def get_article_body_selenium(url):
    driver = get_driver()
    driver.get(url)

    try:
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR, "article")))
        time.sleep(2)
        elems = driver.find_elements(By.CSS_SELECTOR, "article p")
        body = "\n".join([e.text for e in elems if e.text.strip()])
    except Exception as e:
        body = f"（本文取得中にエラーが発生しました: {e}）"

    driver.quit()
    return body or "（本文が空です）"

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
st.set_page_config(page_title="デイリー新潮ビューア", layout="centered")
st.title("📰 デイリー新潮 - 記事取得アプリ")

# 本文取得方法の切替
method = st.radio("📖 本文取得方法", ["Selenium", "BeautifulSoup"], horizontal=True)

# 記事取得ボタン
if st.button("🗞️ 記事一覧を取得"):
    with st.spinner("記事一覧を取得中..."):
        st.session_state.articles = get_daily_shincho_articles()
        st.session_state.body = ""
        st.session_state.selected_title = ""

# 記事選択と本文表示
if "articles" in st.session_state and st.session_state.articles:
    titles = [a["title"] for a in st.session_state.articles]
    selected_title = st.selectbox("📰 記事を選択", titles)
    selected_article = next((a for a in st.session_state.articles if a["title"] == selected_title), None)

    if selected_article:
        st.markdown(f"🔗 [記事リンクを開く]({selected_article['url']})")

        if st.button("📖 本文を表示"):
            with st.spinner("本文を取得中..."):
                if method == "Selenium":
                    st.session_state.body = get_article_body_selenium(selected_article["url"])
                else:
                    st.session_state.body = get_article_body_bs4(selected_article["url"])
            st.success("✅ 本文を取得しました。")

# 本文表示＆保存
if "body" in st.session_state and st.session_state.body:
    st.subheader("📄 記事本文")
    st.write(st.session_state.body)

    if st.button("💾 テキスト保存"):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_title = selected_title[:30].replace(" ", "_").replace("/", "_").replace(":", "_")
        filename = os.path.join(SAVE_DIR, f"{safe_title}_{timestamp}.txt")
        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"{selected_title}\n{selected_article['url']}\n\n{st.session_state.body}")
        st.success(f"✅ 保存しました: {filename}")
