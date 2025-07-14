# 複数メディア対応 記事ビューア

## 概要
このアプリは、以下2つのメディア記事を取得・表示・保存できます：

- 📰 デイリー新潮（記事一覧から選択）
- 📰 文春オンライン（記事URLを手動で入力）

## 機能
- Selenium または BeautifulSoup による本文取得
- テキストファイルへの保存機能
- Streamlit UIで簡単操作

## セットアップ

1. 仮想環境作成（推奨）:

```
python -m venv venv
source venv/bin/activate  # Windowsは venv\Scripts\activate
```

2. 必要ライブラリのインストール:

```
pip install -r requirements.txt
```

3. 実行:

```
streamlit run app.py
```

## 保存先
保存した記事は `saved_articles/` ディレクトリに `.txt` 形式で保存されます。

## 注意
- 文春オンラインは一覧取得できないため、URLを直接貼り付けてください。