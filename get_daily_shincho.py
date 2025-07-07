from selenium import webdriver
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time

# --- Seleniumの設定 ---
options = Options()
options.add_argument("--headless")  # ヘッドレスモード（ブラウザ非表示）
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

# --- デイリー新潮 トップページ ---
url = "https://www.dailyshincho.jp/"
driver.get(url)
time.sleep(5)  # JavaScriptでの描画を待つ

# --- 見出しとリンクの取得 ---
articles = []
elements = driver.find_elements(By.CSS_SELECTOR, "a:has(p.c-list-article__caption)")

for elem in elements:
    try:
        title_elem = elem.find_element(By.CSS_SELECTOR, "p.c-list-article__caption")
        title = title_elem.text.strip()
        link = elem.get_attribute("href")
        if title and link:
            articles.append((title, link))
    except:
        continue

print(f"🔍 {len(articles)} 件の見出しを取得しました。")

# --- 本文の取得と保存 ---
with open("dailyshincho_articles.txt", "w", encoding="utf-8") as f:
    for i, (title, link) in enumerate(articles, 1):
        print(f"\n📰 [{i}] {title}")
        f.write(f"### {title}\n{link}\n")

        try:
            driver.get(link)
            time.sleep(3)

            paragraphs = driver.find_elements(By.CSS_SELECTOR, "div.article-body p")
            body = "\n".join(p.text for p in paragraphs if p.text.strip())

            if not body:
                body = "（本文が取得できませんでした）"

            f.write(f"\n{body}\n\n---\n\n")

        except Exception as e:
            print(f"⚠️ 本文取得エラー: {e}")
            f.write("（記事取得時にエラーが発生しました）\n\n---\n\n")

driver.quit()
print("\n✅ 完了しました。→ dailyshincho_articles.txt に保存されました。")
