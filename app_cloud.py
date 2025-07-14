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
        res = requests.get(url,
