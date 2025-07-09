from weasyprint import HTML
from jinja2 import Template

# --- PDF用テンプレート ---
def render_html(title, url, body):
    html_template = """
    <html>
    <head>
        <meta charset="utf-8">
        <style>
            body { font-family: sans-serif; margin: 2em; }
            h1 { color: #333; }
            a { font-size: 0.9em; color: #555; }
            pre { white-space: pre-wrap; }
        </style>
    </head>
    <body>
        <h1>{{ title }}</h1>
        <a href="{{ url }}">{{ url }}</a>
        <hr>
        <pre>{{ body }}</pre>
    </body>
    </html>
    """
    return Template(html_template).render(title=title, url=url, body=body)

# --- PDF保存 ---
if st.button("📄 PDFで保存"):
    html_content = render_html(selected_title, selected_article["url"], body)
    filename_pdf = f"{selected_title[:30].replace(' ', '_').replace('/', '_')}_{timestamp}.pdf"
    filepath_pdf = os.path.join(SAVE_DIR, filename_pdf)
    HTML(string=html_content).write_pdf(filepath_pdf)
    st.success(f"✅ PDF保存しました: {filepath_pdf}")
