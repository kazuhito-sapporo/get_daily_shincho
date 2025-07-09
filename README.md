# 📰 Daily Shincho Scraper

これは、デイリー新潮のトップページから記事一覧を取得し、本文を抽出・保存する Streamlit アプリです。

## ✅ 機能

- 記事一覧を自動取得（Selenium使用）
- 記事タイトルを選択し、本文を取得・表示（Selenium / BeautifulSoup 選択可）
- 本文を `.txt` 形式で保存

## 🚀 使用方法

```bash
git clone https://github.com/あなたのユーザー名/daily_shincho_scraper.git
cd daily_shincho_scraper
python -m venv venv
source venv/bin/activate  # Windowsなら venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py

