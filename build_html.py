#!/usr/bin/env python3
import json

LINKS = [
    {"name": "厚生労働省 職場の安全サイト", "url": "https://anzeninfo.mhlw.go.jp/", "desc": "労働安全衛生に関する情報ポータル"},
    {"name": "安全衛生情報センター (JAISH)", "url": "https://www.jaish.gr.jp/", "desc": "法令・通達・ガイドラインのデータベース"},
    {"name": "こころの耳", "url": "https://kokoro.mhlw.go.jp/", "desc": "職場のメンタルヘルス対策"},
    {"name": "産業保健総合支援センター", "url": "https://www.johas.go.jp/sangyouhoken/", "desc": "地域の産業保健活動支援"},
    {"name": "e-Gov法令検索", "url": "https://elaws.e-gov.go.jp/", "desc": "法令の原文検索"},
    {"name": "届出・申請等帳票", "url": "https://www.mhlw.go.jp/stf/seisakunitsuite/bunya/koyou_roudou/roudoukijun/anzen/anzeneisei36/index.html", "desc": "各種届出様式のダウンロード"},
]

COMMON_HEAD = '''<meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Noto+Sans+JP:wght@400;500;600;700&display=swap" rel="stylesheet">'''

COMMON_STYLE = '''
    * { margin: 0; padding: 0; box-sizing: border-box; }
    :root {
      --blue: #3b82f6; --blue-dark: #1d4ed8;
      --orange: #f59e0b; --orange-dark: #ea580c;
      --green: #10b981; --green-dark: #059669;
      --gray-50: #f9fafb; --gray-100: #f3f4f6; --gray-200: #e5e7eb;
      --gray-400: #9ca3af; --gray-500: #6b7280; --gray-600: #4b5563;
      --gray-800: #1f2937; --gray-900: #111827;
    }
    body { 
      font-family: "Inter", "Noto Sans JP", sans-serif;
      background: linear-gradient(180deg, #f8fafc 0%, #f1f5f9 100%);
      color: var(--gray-800); line-height: 1.6; min-height: 100vh;
    }
    header {
      background: rgba(255,255,255,0.8); backdrop-filter: blur(12px);
      border-bottom: 1px solid var(--gray-200);
      position: sticky; top: 0; z-index: 100;
    }
    .header-inner {
      max-width: 1200px; margin: 0 auto; padding: 16px 32px;
      display: flex; justify-content: space-between; align-items: center;
    }
    .logo { font-size: 1.25rem; font-weight: 700; color: var(--gray-900); text-decoration: none; }
    .logo span { color: var(--blue); }
    nav { display: flex; gap: 32px; }
    nav a { font-size: 0.9rem; font-weight: 500; color: var(--gray-500); text-decoration: none; transition: color 0.2s; }
    nav a:hover, nav a.active { color: var(--blue); }
    main { max-width: 1000px; margin: 0 auto; padding: 48px 32px 80px; }
    @media (max-width: 768px) {
      .header-inner { padding: 12px 20px; }
      nav { gap: 16px; }
      nav a { font-size: 0.8rem; }
      main { padding: 32px 20px 60px; }
    }
'''

HEADER_HTML = '''<header>
    <div class="header-inner">
      <a href="index.html" class="logo">産業保健<span>ポータル</span></a>
      <nav>
        <a href="seido.html"{seido_active}>制度改正</a>
        <a href="articles.html"{articles_active}>最新記事</a>
        <a href="journals.html"{journals_active}>雑誌一覧</a>
      </nav>
    </div>
  </header>'''

def generate_index(data):
    # 最新記事を収集
    all_articles = []
    for j in data["journals"]:
        for a in j.get("articles", [])[:2]:
            all_articles.append({**a, "journal": j["name"]})
    all_articles.sort(key=lambda x: (x.get("year", ""), x.get("volume", "")), reverse=True)
    
    quick_links = ""
    for a in all_articles[:5]:
        issue = f'{a["year"]}年 {a["volume"]}巻' if a.get("year") and a.get("volume") else ""
        quick_links += f'''
      <a href="{a.get('link', 'articles.html')}" target="_blank" class="quick-link">
        <span class="tag jstage">J-STAGE</span>
        <span class="text">{a["title"]}</span>
        <span class="meta">{issue}</span>
        <svg class="arrow" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 12h14M12 5l7 7-7 7"/></svg>
      </a>'''
    
    if not quick_links:
        quick_links = '<div class="loading-item">データ取得中...</div>'
    
    return f'''<!DOCTYPE html>
<html lang="ja">
<head>
  {COMMON_HEAD}
  <title>産業保健ポータル</title>
  <style>{COMMON_STYLE}
    .hero-cards {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 24px; margin-bottom: 64px; }}
    .hero-card {{
      position: relative; overflow: hidden; padding: 32px; border-radius: 20px;
      color: white; text-decoration: none; min-height: 180px;
      display: flex; flex-direction: column; justify-content: flex-end;
      transition: transform 0.3s ease, box-shadow 0.3s ease;
    }}
    .hero-card:hover {{ transform: translateY(-6px); }}
    .hero-card.blue {{ background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%); box-shadow: 0 10px 40px -10px rgba(59,130,246,0.5); }}
    .hero-card.orange {{ background: linear-gradient(135deg, #f59e0b 0%, #ea580c 100%); box-shadow: 0 10px 40px -10px rgba(245,158,11,0.5); }}
    .hero-card.green {{ background: linear-gradient(135deg, #10b981 0%, #059669 100%); box-shadow: 0 10px 40px -10px rgba(16,185,129,0.5); }}
    .hero-card h2 {{ font-size: 1.5rem; font-weight: 700; margin-bottom: 8px; }}
    .hero-card p {{ font-size: 0.9rem; opacity: 0.9; }}
    .section-header {{ display: flex; align-items: center; gap: 12px; margin-bottom: 20px; }}
    .section-header h3 {{ font-size: 0.8rem; font-weight: 600; letter-spacing: 0.1em; text-transform: uppercase; color: var(--gray-400); }}
    .section-header::after {{ content: ''; flex: 1; height: 1px; background: var(--gray-200); }}
    .quick-links {{ background: white; border-radius: 16px; box-shadow: 0 1px 3px rgba(0,0,0,0.04), 0 4px 12px rgba(0,0,0,0.03); overflow: hidden; }}
    .quick-link {{ display: flex; align-items: center; gap: 16px; padding: 20px 24px; text-decoration: none; color: inherit; border-bottom: 1px solid var(--gray-100); transition: background 0.2s; }}
    .quick-link:last-child {{ border-bottom: none; }}
    .quick-link:hover {{ background: var(--gray-50); }}
    .quick-link .tag {{ font-size: 0.7rem; font-weight: 600; padding: 4px 10px; border-radius: 6px; white-space: nowrap; }}
    .tag.jstage {{ background: #dbeafe; color: #1d4ed8; }}
    .quick-link .text {{ flex: 1; font-size: 0.95rem; font-weight: 500; color: var(--gray-800); overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }}
    .quick-link .meta {{ font-size: 0.8rem; color: var(--gray-400); white-space: nowrap; }}
    .quick-link .arrow {{ color: var(--gray-300); transition: transform 0.2s, color 0.2s; }}
    .quick-link:hover .arrow {{ transform: translateX(4px); color: var(--blue); }}
    .loading-item {{ padding: 24px; text-align: center; color: var(--gray-400); }}
    footer {{ background: var(--gray-900); color: white; padding: 48px 32px; text-align: center; }}
    footer p {{ font-size: 0.85rem; opacity: 0.7; margin-bottom: 8px; }}
    footer small {{ font-size: 0.75rem; opacity: 0.4; }}
    @media (max-width: 768px) {{
      .hero-cards {{ grid-template-columns: 1fr; gap: 16px; margin-bottom: 48px; }}
      .hero-card {{ min-height: 120px; padding: 24px; }}
    }}
  </style>
</head>
<body>
  {HEADER_HTML.format(seido_active="", articles_active="", journals_active="")}
  <main>
    <div class="hero-cards">
      <a href="seido.html" class="hero-card blue">
        <h2>制度改正</h2>
        <p>法令・ガイドラインの最新改正情報</p>
      </a>
      <a href="articles.html" class="hero-card orange">
        <h2>最新記事</h2>
        <p>各学術誌の最新論文</p>
      </a>
      <a href="journals.html" class="hero-card green">
        <h2>雑誌一覧</h2>
        <p>J-STAGE無料閲覧可能な学術誌</p>
      </a>
    </div>
    <div class="section-header"><h3>Quick Links</h3></div>
    <div class="quick-links">{quick_links}
    </div>
  </main>
  <footer>
    <p>産業保健に関する法令・ガイドライン・学術情報の収集を目的としたポータルサイトです</p>
    <small>最終更新: {data["updated"]}</small>
  </footer>
</body>
</html>'''

def generate_seido():
    links_html = ""
    for link in LINKS:
        links_html += f'''
      <a href="{link['url']}" target="_blank" class="link-card">
        <div class="content">
          <h3>{link['name']}</h3>
          <p>{link['desc']}</p>
        </div>
        <svg class="arrow" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 12h14M12 5l7 7-7 7"/></svg>
      </a>'''
    
    return f'''<!DOCTYPE html>
<html lang="ja">
<head>
  {COMMON_HEAD}
  <title>制度改正 - 産業保健ポータル</title>
  <style>{COMMON_STYLE}
    nav a.active {{ color: var(--blue); }}
    .page-header {{ margin-bottom: 48px; }}
    .page-header h1 {{ font-size: 2rem; font-weight: 700; color: var(--gray-900); margin-bottom: 12px; }}
    .page-header p {{ font-size: 1rem; color: var(--gray-500); }}
    .link-grid {{ display: grid; gap: 16px; }}
    .link-card {{
      display: flex; align-items: center; gap: 20px; padding: 24px 28px;
      background: white; border-radius: 16px; text-decoration: none; color: inherit;
      box-shadow: 0 1px 3px rgba(0,0,0,0.04), 0 4px 12px rgba(0,0,0,0.03);
      transition: all 0.3s ease;
    }}
    .link-card:hover {{ transform: translateY(-2px); box-shadow: 0 8px 30px rgba(59,130,246,0.12); }}
    .link-card .content {{ flex: 1; }}
    .link-card .content h3 {{ font-size: 1rem; font-weight: 600; color: var(--gray-800); margin-bottom: 4px; }}
    .link-card .content p {{ font-size: 0.85rem; color: var(--gray-500); }}
    .link-card .arrow {{ color: var(--gray-300); transition: transform 0.2s, color 0.2s; }}
    .link-card:hover .arrow {{ transform: translateX(4px); color: var(--blue); }}
  </style>
</head>
<body>
  {HEADER_HTML.format(seido_active=' class="active"', articles_active="", journals_active="")}
  <main>
    <div class="page-header">
      <h1>制度改正・法令情報</h1>
      <p>産業保健に関する主要な情報源へのリンク集</p>
    </div>
    <div class="link-grid">{links_html}
    </div>
  </main>
</body>
</html>'''

def generate_articles(data):
    journals_html = ""
    for j in data["journals"]:
        articles_html = ""
        if j.get("articles"):
            for a in j["articles"]:
                authors = ", ".join(a.get("authors", [])[:3])
                if len(a.get("authors", [])) > 3:
                    authors += " 他"
                issue = f'{a["year"]}年 {a["volume"]}巻{a.get("number", "")}号' if a.get("year") else ""
                meta = " / ".join(filter(None, [authors, issue]))
                link = a.get("link", "#")
                articles_html += f'''
          <a href="{link}" target="_blank" class="article-item">
            <div class="article-title">{a["title"]}</div>
            <div class="article-meta">{meta}</div>
          </a>'''
        else:
            articles_html = '<div class="article-item"><div class="article-meta">データなし</div></div>'
        
        journals_html += f'''
    <div class="journal-section">
      <div class="journal-header">
        <div class="journal-info">
          <h2><a href="{j['url']}" target="_blank">{j['name']}</a></h2>
          <p>{j['publisher']}</p>
        </div>
      </div>
      <div class="article-list">{articles_html}
      </div>
    </div>'''
    
    return f'''<!DOCTYPE html>
<html lang="ja">
<head>
  {COMMON_HEAD}
  <title>最新記事 - 産業保健ポータル</title>
  <style>{COMMON_STYLE}
    nav a.active {{ color: var(--orange); }}
    .page-header {{ margin-bottom: 12px; }}
    .page-header h1 {{ font-size: 2rem; font-weight: 700; color: var(--gray-900); margin-bottom: 12px; }}
    .page-header p {{ font-size: 1rem; color: var(--gray-500); }}
    .updated {{ font-size: 0.8rem; color: var(--gray-400); margin-bottom: 40px; }}
    .journal-section {{
      background: white; border-radius: 20px; padding: 28px; margin-bottom: 24px;
      box-shadow: 0 1px 3px rgba(0,0,0,0.04), 0 4px 12px rgba(0,0,0,0.03);
    }}
    .journal-header {{ margin-bottom: 20px; padding-bottom: 16px; border-bottom: 1px solid var(--gray-100); }}
    .journal-info h2 {{ font-size: 1.1rem; font-weight: 600; color: var(--gray-800); }}
    .journal-info h2 a {{ color: inherit; text-decoration: none; }}
    .journal-info h2 a:hover {{ color: var(--orange); }}
    .journal-info p {{ font-size: 0.8rem; color: var(--gray-400); }}
    .article-list {{ display: grid; gap: 1px; background: var(--gray-100); border-radius: 12px; overflow: hidden; }}
    .article-item {{
      display: block; padding: 16px 20px; background: var(--gray-50);
      text-decoration: none; color: inherit; transition: background 0.2s;
    }}
    .article-item:hover {{ background: white; }}
    .article-title {{ font-size: 0.95rem; font-weight: 500; color: var(--gray-800); margin-bottom: 6px; }}
    .article-item:hover .article-title {{ color: var(--orange); }}
    .article-meta {{ font-size: 0.8rem; color: var(--gray-400); }}
  </style>
</head>
<body>
  {HEADER_HTML.format(seido_active="", articles_active=' class="active"', journals_active="")}
  <main>
    <div class="page-header">
      <h1>最新記事</h1>
      <p>各学術誌の最新論文</p>
    </div>
    <div class="updated">最終更新: {data["updated"]}</div>
    {journals_html}
  </main>
</body>
</html>'''

def generate_journals(data):
    journals_html = ""
    for j in data["journals"]:
        journals_html += f'''
    <div class="journal-card">
      <div class="journal-card-header">
        <div class="info">
          <h2><a href="{j['url']}" target="_blank">{j['name']}</a></h2>
          <p class="publisher">{j['publisher']}</p>
        </div>
      </div>
      <p class="description">{j.get('desc', '')}</p>
      <a href="{j['url']}" target="_blank" class="link-btn">
        J-STAGEで開く
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M18 13v6a2 2 0 01-2 2H5a2 2 0 01-2-2V8a2 2 0 012-2h6M15 3h6v6M10 14L21 3"/></svg>
      </a>
    </div>'''
    
    return f'''<!DOCTYPE html>
<html lang="ja">
<head>
  {COMMON_HEAD}
  <title>雑誌一覧 - 産業保健ポータル</title>
  <style>{COMMON_STYLE}
    nav a.active {{ color: var(--green); }}
    .page-header {{ margin-bottom: 48px; }}
    .page-header h1 {{ font-size: 2rem; font-weight: 700; color: var(--gray-900); margin-bottom: 12px; }}
    .page-header p {{ font-size: 1rem; color: var(--gray-500); }}
    .journal-list {{ display: flex; flex-direction: column; gap: 20px; }}
    .journal-card {{
      background: white; border-radius: 20px; padding: 28px;
      box-shadow: 0 1px 3px rgba(0,0,0,0.04), 0 4px 12px rgba(0,0,0,0.03);
      transition: all 0.3s ease;
    }}
    .journal-card:hover {{ transform: translateY(-2px); box-shadow: 0 8px 30px rgba(16,185,129,0.12); }}
    .journal-card-header {{ display: flex; align-items: flex-start; gap: 16px; margin-bottom: 16px; }}
    .journal-card-header .info {{ flex: 1; }}
    .journal-card-header h2 {{ font-size: 1.15rem; font-weight: 600; color: var(--gray-900); margin-bottom: 4px; }}
    .journal-card-header h2 a {{ color: inherit; text-decoration: none; }}
    .journal-card-header h2 a:hover {{ color: var(--green); }}
    .journal-card-header .publisher {{ font-size: 0.8rem; color: var(--gray-400); }}
    .journal-card .description {{ font-size: 0.9rem; color: var(--gray-600); line-height: 1.7; margin-bottom: 20px; }}
    .journal-card .link-btn {{
      display: inline-flex; align-items: center; gap: 8px;
      padding: 10px 18px; background: var(--gray-50); border-radius: 10px;
      font-size: 0.85rem; font-weight: 500; color: var(--gray-600);
      text-decoration: none; transition: all 0.2s;
    }}
    .journal-card .link-btn:hover {{ background: var(--green); color: white; }}
    .journal-card .link-btn svg {{ width: 16px; height: 16px; }}
  </style>
</head>
<body>
  {HEADER_HTML.format(seido_active="", articles_active="", journals_active=' class="active"')}
  <main>
    <div class="page-header">
      <h1>雑誌一覧</h1>
      <p>J-STAGEで無料閲覧可能な産業保健関連学術誌</p>
    </div>
    <div class="journal-list">{journals_html}
    </div>
  </main>
</body>
</html>'''

def main():
    with open("data.json", encoding="utf-8") as f:
        data = json.load(f)
    
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(generate_index(data))
    
    with open("seido.html", "w", encoding="utf-8") as f:
        f.write(generate_seido())
    
    with open("articles.html", "w", encoding="utf-8") as f:
        f.write(generate_articles(data))
    
    with open("journals.html", "w", encoding="utf-8") as f:
        f.write(generate_journals(data))
    
    print("Generated: index.html, seido.html, articles.html, journals.html")

if __name__ == "__main__":
    main()
