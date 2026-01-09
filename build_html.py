#!/usr/bin/env python3
import json

LINKS = [
    {"name": "厚生労働省 職場の安全サイト", "url": "https://anzeninfo.mhlw.go.jp/", "desc": "労働安全衛生に関する情報ポータル", "icon": "building"},
    {"name": "安全衛生情報センター (JAISH)", "url": "https://www.jaish.gr.jp/", "desc": "法令・通達・ガイドラインのデータベース", "icon": "database"},
    {"name": "こころの耳", "url": "https://kokoro.mhlw.go.jp/", "desc": "職場のメンタルヘルス対策", "icon": "heart"},
    {"name": "産業保健総合支援センター", "url": "https://www.johas.go.jp/sangyouhoken/", "desc": "地域の産業保健活動支援", "icon": "users"},
    {"name": "e-Gov法令検索", "url": "https://elaws.e-gov.go.jp/", "desc": "法令の原文検索", "icon": "search"},
    {"name": "届出・申請等帳票", "url": "https://www.mhlw.go.jp/stf/seisakunitsuite/bunya/koyou_roudou/roudoukijun/anzen/anzeneisei36/index.html", "desc": "各種届出様式のダウンロード", "icon": "download"},
]

ICONS = {
    "building": '<path d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"/>',
    "database": '<path d="M4 7v10c0 2 1 3 3 3h10c2 0 3-1 3-3V7c0-2-1-3-3-3H7C5 4 4 5 4 7zm0 5h16M9 4v16"/>',
    "heart": '<path d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"/>',
    "users": '<path d="M17 21v-2a4 4 0 00-4-4H5a4 4 0 00-4 4v2M9 11a4 4 0 100-8 4 4 0 000 8zM23 21v-2a4 4 0 00-3-3.87M16 3.13a4 4 0 010 7.75"/>',
    "search": '<path d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/>',
    "download": '<path d="M21 15v4a2 2 0 01-2 2H5a2 2 0 01-2-2v-4M7 10l5 5 5-5M12 15V3"/>',
    "file": '<path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z"/><path d="M14 2v6h6M16 13H8M16 17H8M10 9H8"/>',
    "book": '<path d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"/>',
    "arrow": '<path d="M5 12h14M12 5l7 7-7 7"/>',
    "external": '<path d="M18 13v6a2 2 0 01-2 2H5a2 2 0 01-2-2V8a2 2 0 012-2h6M15 3h6v6M10 14L21 3"/>',
}

COMMON_HEAD = '''<meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Noto+Sans+JP:wght@300;400;500;600;700&display=swap" rel="stylesheet">'''

COMMON_STYLE = '''
    * { margin: 0; padding: 0; box-sizing: border-box; }
    :root {
      --bg: #ffffff;
      --bg-secondary: #fafafa;
      --text: #18181b;
      --text-muted: #71717a;
      --text-light: #a1a1aa;
      --border: #e4e4e7;
      --border-light: #f4f4f5;
      --accent-1: #6366f1;
      --accent-2: #8b5cf6;
      --accent-3: #ec4899;
    }
    body { 
      font-family: "Inter", "Noto Sans JP", -apple-system, sans-serif;
      background: var(--bg);
      color: var(--text);
      line-height: 1.6;
      min-height: 100vh;
      -webkit-font-smoothing: antialiased;
    }
    header {
      position: fixed; top: 0; left: 0; right: 0;
      background: rgba(255,255,255,0.85);
      backdrop-filter: blur(20px);
      border-bottom: 1px solid var(--border-light);
      z-index: 100;
    }
    .header-inner {
      max-width: 1200px; margin: 0 auto;
      padding: 18px 40px;
      display: flex; justify-content: space-between; align-items: center;
    }
    .logo {
      font-size: 1rem; font-weight: 600; letter-spacing: 0.02em;
      color: var(--text); text-decoration: none;
      display: flex; align-items: center; gap: 10px;
    }
    .logo-icon {
      width: 32px; height: 32px;
      background: linear-gradient(135deg, var(--accent-1) 0%, var(--accent-2) 100%);
      border-radius: 8px;
      display: flex; align-items: center; justify-content: center;
    }
    .logo-icon svg { width: 18px; height: 18px; color: white; }
    nav { display: flex; gap: 36px; }
    nav a {
      font-size: 0.875rem; font-weight: 450; color: var(--text-muted);
      text-decoration: none; transition: color 0.2s;
    }
    nav a:hover, nav a.active { color: var(--text); }
    main { max-width: 1200px; margin: 0 auto; padding: 120px 40px 80px; }
    @media (max-width: 768px) {
      .header-inner { padding: 14px 20px; }
      nav { gap: 20px; }
      nav a { font-size: 0.8rem; }
      main { padding: 100px 20px 60px; }
    }
'''

HEADER_HTML = '''<header>
    <div class="header-inner">
      <a href="index.html" class="logo">
        <div class="logo-icon">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"/>
          </svg>
        </div>
        SANPO PORTAL
      </a>
      <nav>
        <a href="seido.html"{seido_active}>制度改正</a>
        <a href="articles.html"{articles_active}>最新記事</a>
        <a href="journals.html"{journals_active}>雑誌一覧</a>
        <a href="search.html"{search_active}>検索</a>
      </nav>
    </div>
  </header>'''

def generate_index(data):
    all_articles = []
    for j in data["journals"]:
        for a in j.get("articles", [])[:2]:
            all_articles.append({**a, "journal": j["name"]})
    all_articles.sort(key=lambda x: (x.get("year", ""), x.get("volume", "")), reverse=True)
    
    quick_links = ""
    for i, a in enumerate(all_articles[:5]):
        issue = f'{a["year"]}年 {a["volume"]}巻' if a.get("year") and a.get("volume") else ""
        quick_links += f'''
        <a href="{a.get('link', 'articles.html')}" target="_blank" class="article-row">
          <span class="article-num">{str(i+1).zfill(2)}</span>
          <span class="article-title">{a["title"]}</span>
          <span class="article-meta">{issue}</span>
          <svg class="article-arrow" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">{ICONS["arrow"]}</svg>
        </a>'''
    
    if not quick_links:
        quick_links = '<div class="empty">データ取得中...</div>'
    
    return f'''<!DOCTYPE html>
<html lang="ja">
<head>
  {COMMON_HEAD}
  <title>SANPO PORTAL - 産業保健情報ポータル</title>
  <style>{COMMON_STYLE}
    .hero {{
      padding: 60px 0 80px;
      text-align: center;
    }}
    .hero-badge {{
      display: inline-flex;
      align-items: center;
      gap: 6px;
      padding: 6px 14px;
      background: var(--bg-secondary);
      border: 1px solid var(--border);
      border-radius: 100px;
      font-size: 0.75rem;
      font-weight: 500;
      color: var(--text-muted);
      margin-bottom: 24px;
    }}
    .hero-badge::before {{
      content: '';
      width: 6px; height: 6px;
      background: var(--accent-1);
      border-radius: 50%;
    }}
    .hero h1 {{
      font-size: clamp(2rem, 4vw, 3.25rem);
      font-weight: 700;
      letter-spacing: -0.03em;
      line-height: 1.2;
      margin-bottom: 16px;
    }}
    .hero p {{
      font-size: 1.125rem;
      color: var(--text-muted);
      font-weight: 400;
    }}
    
    .cards {{
      display: grid;
      grid-template-columns: repeat(2, 1fr);
      gap: 16px;
      margin-bottom: 80px;
    }}
    .card {{
      position: relative;
      padding: 32px 28px;
      background: var(--bg);
      border: 1px solid var(--border);
      border-radius: 20px;
      text-decoration: none;
      color: inherit;
      transition: all 0.3s ease;
    }}
    .card:hover {{
      border-color: var(--accent-1);
      box-shadow: 0 8px 30px rgba(99, 102, 241, 0.08);
      transform: translateY(-2px);
    }}
    .card-icon {{
      width: 48px; height: 48px;
      border-radius: 14px;
      display: flex; align-items: center; justify-content: center;
      margin-bottom: 20px;
    }}
    .card-icon svg {{ width: 24px; height: 24px; }}
    .card:nth-child(1) .card-icon {{ background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%); color: white; }}
    .card:nth-child(2) .card-icon {{ background: linear-gradient(135deg, #f59e0b 0%, #f97316 100%); color: white; }}
    .card:nth-child(3) .card-icon {{ background: linear-gradient(135deg, #10b981 0%, #14b8a6 100%); color: white; }}
    .card:nth-child(4) .card-icon {{ background: linear-gradient(135deg, #ec4899 0%, #f43f5e 100%); color: white; }}
    .card h2 {{
      font-size: 1.125rem;
      font-weight: 600;
      margin-bottom: 8px;
    }}
    .card p {{
      font-size: 0.875rem;
      color: var(--text-muted);
      line-height: 1.5;
    }}
    .card-arrow {{
      position: absolute;
      top: 28px; right: 28px;
      width: 32px; height: 32px;
      border-radius: 50%;
      background: var(--bg-secondary);
      display: flex; align-items: center; justify-content: center;
      transition: all 0.3s;
    }}
    .card-arrow svg {{ width: 14px; height: 14px; color: var(--text-light); transition: all 0.3s; }}
    .card:hover .card-arrow {{ background: var(--accent-1); }}
    .card:hover .card-arrow svg {{ color: white; transform: translateX(2px); }}
    
    .section {{
      margin-bottom: 40px;
    }}
    .section-header {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      margin-bottom: 20px;
    }}
    .section-title {{
      font-size: 0.8rem;
      font-weight: 600;
      letter-spacing: 0.08em;
      text-transform: uppercase;
      color: var(--text-muted);
    }}
    .section-link {{
      font-size: 0.8rem;
      font-weight: 500;
      color: var(--accent-1);
      text-decoration: none;
    }}
    .section-link:hover {{ text-decoration: underline; }}
    
    .articles-list {{
      background: var(--bg-secondary);
      border-radius: 16px;
      overflow: hidden;
    }}
    .article-row {{
      display: grid;
      grid-template-columns: 40px 1fr auto auto;
      align-items: center;
      gap: 20px;
      padding: 18px 24px;
      text-decoration: none;
      color: inherit;
      border-bottom: 1px solid var(--border-light);
      transition: background 0.2s;
    }}
    .article-row:last-child {{ border-bottom: none; }}
    .article-row:hover {{ background: white; }}
    .article-num {{
      font-size: 0.75rem;
      font-weight: 600;
      color: var(--text-light);
      font-variant-numeric: tabular-nums;
    }}
    .article-title {{
      font-size: 0.9rem;
      font-weight: 450;
      color: var(--text);
      overflow: hidden;
      text-overflow: ellipsis;
      white-space: nowrap;
    }}
    .article-meta {{
      font-size: 0.8rem;
      color: var(--text-light);
      white-space: nowrap;
    }}
    .article-arrow {{
      color: var(--text-light);
      transition: all 0.2s;
    }}
    .article-row:hover .article-arrow {{
      color: var(--accent-1);
      transform: translateX(3px);
    }}
    .empty {{ padding: 40px; text-align: center; color: var(--text-muted); }}
    
    footer {{
      margin-top: 80px;
      padding: 32px 0;
      border-top: 1px solid var(--border-light);
      text-align: center;
    }}
    footer p {{ font-size: 0.8rem; color: var(--text-light); }}
    
    @media (max-width: 768px) {{
      .cards {{ grid-template-columns: 1fr; }}
      .article-row {{ grid-template-columns: 1fr; gap: 8px; }}
      .article-num {{ display: none; }}
      .article-meta {{ justify-self: start; }}
    }}
  </style>
</head>
<body>
  {HEADER_HTML.format(seido_active="", articles_active="", journals_active="", search_active="")}
  <main>
    <section class="hero">
      <div class="hero-badge">産業保健専門ポータル</div>
      <h1>産業保健情報を、<br>ひとつの場所に。</h1>
      <p>法令・ガイドライン・学術情報を一元的に収集</p>
    </section>
    
    <div class="cards">
      <a href="seido.html" class="card">
        <div class="card-icon">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">{ICONS["file"]}</svg>
        </div>
        <h2>制度改正</h2>
        <p>法令・ガイドラインの<br>最新改正情報</p>
        <div class="card-arrow">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">{ICONS["arrow"]}</svg>
        </div>
      </a>
      <a href="articles.html" class="card">
        <div class="card-icon">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">{ICONS["book"]}</svg>
        </div>
        <h2>最新記事</h2>
        <p>各学術誌の<br>最新論文</p>
        <div class="card-arrow">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">{ICONS["arrow"]}</svg>
        </div>
      </a>
      <a href="journals.html" class="card">
        <div class="card-icon">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">{ICONS["database"]}</svg>
        </div>
        <h2>雑誌一覧</h2>
        <p>J-STAGE無料閲覧<br>可能な学術誌</p>
        <div class="card-arrow">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">{ICONS["arrow"]}</svg>
        </div>
      </a>
      <a href="search.html" class="card">
        <div class="card-icon">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">{ICONS["search"]}</svg>
        </div>
        <h2>キーワード検索</h2>
        <p>類義語シソーラスで<br>論文を横断検索</p>
        <div class="card-arrow">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">{ICONS["arrow"]}</svg>
        </div>
      </a>
    </div>
    
    <section class="section">
      <div class="section-header">
        <span class="section-title">Latest Articles</span>
        <a href="articles.html" class="section-link">すべて見る →</a>
      </div>
      <div class="articles-list">{quick_links}
      </div>
    </section>
  </main>
  
  <footer>
    <p>© SANPO PORTAL · Last updated: {data["updated"]}</p>
  </footer>
</body>
</html>'''

def generate_seido(data):
    links_html = ""
    for link in LINKS:
        icon = ICONS.get(link.get("icon", "file"), ICONS["file"])
        links_html += f'''
      <a href="{link['url']}" target="_blank" class="link-card">
        <div class="link-icon">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">{icon}</svg>
        </div>
        <div class="link-content">
          <h3>{link['name']}</h3>
          <p>{link['desc']}</p>
        </div>
        <svg class="link-arrow" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">{ICONS["external"]}</svg>
      </a>'''
    
    # ニュースセクション
    news_html = ""
    news_items = data.get("news", [])
    if news_items:
        for item in news_items:
            news_html += f'''
        <a href="{item.get('link', '#')}" target="_blank" class="news-item">
          <span class="news-date">{item.get('date', '')}</span>
          <span class="news-title">{item.get('title', '')}</span>
          <svg class="news-arrow" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">{ICONS["arrow"]}</svg>
        </a>'''
    else:
        news_html = '<div class="news-empty">新着情報はありません</div>'
    
    return f'''<!DOCTYPE html>
<html lang="ja">
<head>
  {COMMON_HEAD}
  <title>制度改正 - SANPO PORTAL</title>
  <style>{COMMON_STYLE}
    .page-header {{
      padding: 40px 0 60px;
    }}
    .page-header h1 {{
      font-size: clamp(1.75rem, 3vw, 2.5rem);
      font-weight: 700;
      letter-spacing: -0.02em;
      margin-bottom: 12px;
    }}
    .page-header p {{
      font-size: 1rem;
      color: var(--text-muted);
    }}
    .section-title {{
      font-size: 0.8rem;
      font-weight: 600;
      letter-spacing: 0.08em;
      text-transform: uppercase;
      color: var(--text-muted);
      margin-bottom: 20px;
      display: flex;
      align-items: center;
      gap: 12px;
    }}
    .section-title::after {{
      content: '';
      flex: 1;
      height: 1px;
      background: var(--border);
    }}
    .news-section {{
      margin-bottom: 60px;
    }}
    .news-list {{
      background: var(--bg-secondary);
      border-radius: 16px;
      overflow: hidden;
    }}
    .news-item {{
      display: grid;
      grid-template-columns: 90px 1fr auto;
      align-items: center;
      gap: 16px;
      padding: 16px 24px;
      text-decoration: none;
      color: inherit;
      border-bottom: 1px solid var(--border-light);
      transition: background 0.2s;
    }}
    .news-item:last-child {{ border-bottom: none; }}
    .news-item:hover {{ background: white; }}
    .news-date {{
      font-size: 0.75rem;
      color: var(--text-light);
      font-variant-numeric: tabular-nums;
    }}
    .news-title {{
      font-size: 0.9rem;
      font-weight: 450;
      color: var(--text);
      overflow: hidden;
      text-overflow: ellipsis;
      white-space: nowrap;
    }}
    .news-item:hover .news-title {{ color: var(--accent-1); }}
    .news-arrow {{
      color: var(--text-light);
      transition: all 0.2s;
    }}
    .news-item:hover .news-arrow {{
      color: var(--accent-1);
      transform: translateX(3px);
    }}
    .news-empty {{
      padding: 32px;
      text-align: center;
      color: var(--text-light);
    }}
    .link-list {{
      display: grid;
      gap: 12px;
    }}
    .link-card {{
      display: grid;
      grid-template-columns: auto 1fr auto;
      align-items: center;
      gap: 20px;
      padding: 24px 28px;
      background: var(--bg-secondary);
      border-radius: 16px;
      text-decoration: none;
      color: inherit;
      transition: all 0.25s ease;
    }}
    .link-card:hover {{
      background: white;
      box-shadow: 0 4px 20px rgba(0,0,0,0.06);
      transform: translateX(4px);
    }}
    .link-icon {{
      width: 44px; height: 44px;
      background: white;
      border-radius: 12px;
      display: flex; align-items: center; justify-content: center;
      box-shadow: 0 2px 8px rgba(0,0,0,0.04);
    }}
    .link-icon svg {{ width: 20px; height: 20px; color: var(--accent-1); }}
    .link-content h3 {{ font-size: 0.95rem; font-weight: 600; margin-bottom: 4px; }}
    .link-content p {{ font-size: 0.8rem; color: var(--text-muted); }}
    .link-arrow {{ color: var(--text-light); transition: all 0.2s; }}
    .link-card:hover .link-arrow {{ color: var(--accent-1); }}
  </style>
</head>
<body>
  {HEADER_HTML.format(seido_active=' class="active"', articles_active="", journals_active="", search_active="")}
  <main>
    <div class="page-header">
      <h1>制度改正・法令情報</h1>
      <p>産業保健に関する最新ニュースと主要な情報源</p>
    </div>
    
    <section class="news-section">
      <div class="section-title">厚労省 新着情報（産業保健関連）</div>
      <div class="news-list">{news_html}
      </div>
    </section>
    
    <div class="section-title">関連リンク</div>
    <div class="link-list">{links_html}
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
            articles_html = '<div class="article-item empty">データなし</div>'
        
        journals_html += f'''
    <div class="journal-section">
      <div class="journal-header">
        <div class="journal-icon">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">{ICONS["book"]}</svg>
        </div>
        <div>
          <h2><a href="{j['url']}" target="_blank">{j['name']}</a></h2>
          <p class="publisher">{j['publisher']}</p>
        </div>
      </div>
      <div class="article-list">{articles_html}
      </div>
    </div>'''
    
    return f'''<!DOCTYPE html>
<html lang="ja">
<head>
  {COMMON_HEAD}
  <title>最新記事 - SANPO PORTAL</title>
  <style>{COMMON_STYLE}
    .page-header {{
      padding: 40px 0 20px;
    }}
    .page-header h1 {{
      font-size: clamp(1.75rem, 3vw, 2.5rem);
      font-weight: 700;
      letter-spacing: -0.02em;
      margin-bottom: 12px;
    }}
    .page-header p {{
      font-size: 1rem;
      color: var(--text-muted);
    }}
    .updated {{
      font-size: 0.75rem;
      color: var(--text-light);
      margin-bottom: 40px;
    }}
    .journal-section {{
      background: var(--bg-secondary);
      border-radius: 20px;
      padding: 28px;
      margin-bottom: 20px;
    }}
    .journal-header {{
      display: flex;
      align-items: center;
      gap: 16px;
      margin-bottom: 20px;
      padding-bottom: 20px;
      border-bottom: 1px solid var(--border-light);
    }}
    .journal-icon {{
      width: 44px; height: 44px;
      background: linear-gradient(135deg, #f59e0b 0%, #f97316 100%);
      border-radius: 12px;
      display: flex; align-items: center; justify-content: center;
      color: white;
    }}
    .journal-icon svg {{ width: 22px; height: 22px; }}
    .journal-header h2 {{ font-size: 1rem; font-weight: 600; margin-bottom: 2px; }}
    .journal-header h2 a {{ color: var(--text); text-decoration: none; }}
    .journal-header h2 a:hover {{ color: var(--accent-1); }}
    .journal-header .publisher {{ font-size: 0.8rem; color: var(--text-muted); }}
    .article-list {{ display: grid; gap: 2px; }}
    .article-item {{
      display: block;
      padding: 16px 20px;
      background: white;
      border-radius: 10px;
      text-decoration: none;
      color: inherit;
      transition: all 0.2s;
    }}
    .article-item:hover {{ box-shadow: 0 2px 12px rgba(0,0,0,0.04); transform: translateX(4px); }}
    .article-title {{ font-size: 0.9rem; font-weight: 450; margin-bottom: 6px; color: var(--text); }}
    .article-item:hover .article-title {{ color: var(--accent-1); }}
    .article-meta {{ font-size: 0.8rem; color: var(--text-muted); }}
    .empty {{ text-align: center; color: var(--text-light); padding: 20px; }}
  </style>
</head>
<body>
  {HEADER_HTML.format(seido_active="", articles_active=' class="active"', journals_active="", search_active="")}
  <main>
    <div class="page-header">
      <h1>最新記事</h1>
      <p>各学術誌の最新論文</p>
    </div>
    <div class="updated">Last updated: {data["updated"]}</div>
    {journals_html}
  </main>
</body>
</html>'''

def generate_journals(data):
    colors = [
        "linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%)",
        "linear-gradient(135deg, #f59e0b 0%, #f97316 100%)",
        "linear-gradient(135deg, #10b981 0%, #14b8a6 100%)",
        "linear-gradient(135deg, #ec4899 0%, #f43f5e 100%)",
        "linear-gradient(135deg, #3b82f6 0%, #0ea5e9 100%)",
        "linear-gradient(135deg, #8b5cf6 0%, #a855f7 100%)",
    ]
    
    journals_html = ""
    for i, j in enumerate(data["journals"]):
        color = colors[i % len(colors)]
        journals_html += f'''
    <div class="journal-card">
      <div class="journal-card-icon" style="background: {color}">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">{ICONS["book"]}</svg>
      </div>
      <div class="journal-card-content">
        <h2><a href="{j['url']}" target="_blank">{j['name']}</a></h2>
        <p class="publisher">{j['publisher']}</p>
        <p class="description">{j.get('desc', '')}</p>
      </div>
      <a href="{j['url']}" target="_blank" class="journal-link">
        J-STAGEで開く
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">{ICONS["external"]}</svg>
      </a>
    </div>'''
    
    return f'''<!DOCTYPE html>
<html lang="ja">
<head>
  {COMMON_HEAD}
  <title>雑誌一覧 - SANPO PORTAL</title>
  <style>{COMMON_STYLE}
    .page-header {{
      padding: 40px 0 60px;
    }}
    .page-header h1 {{
      font-size: clamp(1.75rem, 3vw, 2.5rem);
      font-weight: 700;
      letter-spacing: -0.02em;
      margin-bottom: 12px;
    }}
    .page-header p {{
      font-size: 1rem;
      color: var(--text-muted);
    }}
    .journal-list {{
      display: grid;
      gap: 16px;
    }}
    .journal-card {{
      display: grid;
      grid-template-columns: auto 1fr auto;
      align-items: start;
      gap: 24px;
      padding: 28px;
      background: var(--bg-secondary);
      border-radius: 20px;
      transition: all 0.25s ease;
    }}
    .journal-card:hover {{
      background: white;
      box-shadow: 0 4px 24px rgba(0,0,0,0.06);
    }}
    .journal-card-icon {{
      width: 56px; height: 56px;
      border-radius: 16px;
      display: flex; align-items: center; justify-content: center;
      color: white;
    }}
    .journal-card-icon svg {{ width: 28px; height: 28px; }}
    .journal-card-content h2 {{ font-size: 1.05rem; font-weight: 600; margin-bottom: 4px; }}
    .journal-card-content h2 a {{ color: var(--text); text-decoration: none; }}
    .journal-card-content h2 a:hover {{ color: var(--accent-1); }}
    .journal-card-content .publisher {{ font-size: 0.8rem; color: var(--text-muted); margin-bottom: 12px; }}
    .journal-card-content .description {{ font-size: 0.85rem; color: var(--text-muted); line-height: 1.6; }}
    .journal-link {{
      display: inline-flex;
      align-items: center;
      gap: 6px;
      padding: 10px 16px;
      background: white;
      border-radius: 10px;
      font-size: 0.8rem;
      font-weight: 500;
      color: var(--text-muted);
      text-decoration: none;
      white-space: nowrap;
      transition: all 0.2s;
      box-shadow: 0 1px 3px rgba(0,0,0,0.04);
    }}
    .journal-link:hover {{ color: var(--accent-1); box-shadow: 0 2px 8px rgba(99,102,241,0.15); }}
    .journal-link svg {{ width: 14px; height: 14px; }}
    @media (max-width: 768px) {{
      .journal-card {{ grid-template-columns: 1fr; gap: 16px; }}
      .journal-link {{ justify-self: start; }}
    }}
  </style>
</head>
<body>
  {HEADER_HTML.format(seido_active="", articles_active="", journals_active=' class="active"', search_active="")}
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

def generate_search(data):
    # thesaurus.jsonを読み込む
    try:
        with open("thesaurus.json", encoding="utf-8") as f:
            thesaurus = json.load(f)
    except:
        thesaurus = {}
    
    # JavaScriptに渡すデータ
    articles_js = []
    for j in data["journals"]:
        for a in j.get("articles", []):
            articles_js.append({
                "title": a.get("title", ""),
                "authors": a.get("authors", []),
                "journal": j["name"],
                "year": a.get("year", ""),
                "volume": a.get("volume", ""),
                "number": a.get("number", ""),
                "link": a.get("link", "")
            })
    
    return f'''<!DOCTYPE html>
<html lang="ja">
<head>
  {COMMON_HEAD}
  <title>キーワード検索 - SANPO PORTAL</title>
  <style>{COMMON_STYLE}
    .page-header {{
      padding: 40px 0 40px;
    }}
    .page-header h1 {{
      font-size: clamp(1.75rem, 3vw, 2.5rem);
      font-weight: 700;
      letter-spacing: -0.02em;
      margin-bottom: 12px;
    }}
    .page-header p {{
      font-size: 1rem;
      color: var(--text-muted);
    }}
    .search-box {{
      background: var(--bg-secondary);
      border-radius: 20px;
      padding: 32px;
      margin-bottom: 32px;
    }}
    .search-input-wrap {{
      display: flex;
      gap: 12px;
      margin-bottom: 16px;
    }}
    .search-input {{
      flex: 1;
      padding: 14px 20px;
      font-size: 1rem;
      border: 1px solid var(--border);
      border-radius: 12px;
      outline: none;
      transition: border-color 0.2s, box-shadow 0.2s;
      font-family: inherit;
    }}
    .search-input:focus {{
      border-color: var(--accent-1);
      box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
    }}
    .search-btn {{
      padding: 14px 28px;
      background: linear-gradient(135deg, var(--accent-1) 0%, var(--accent-2) 100%);
      color: white;
      border: none;
      border-radius: 12px;
      font-size: 0.95rem;
      font-weight: 600;
      cursor: pointer;
      transition: transform 0.2s, box-shadow 0.2s;
    }}
    .search-btn:hover {{
      transform: translateY(-1px);
      box-shadow: 0 4px 12px rgba(99, 102, 241, 0.3);
    }}
    .search-options {{
      display: flex;
      gap: 24px;
      align-items: center;
    }}
    .search-option {{
      display: flex;
      align-items: center;
      gap: 8px;
      cursor: pointer;
    }}
    .search-option input {{
      width: 18px;
      height: 18px;
      accent-color: var(--accent-1);
    }}
    .search-option label {{
      font-size: 0.9rem;
      color: var(--text);
      cursor: pointer;
    }}
    .synonyms-info {{
      margin-top: 16px;
      padding: 12px 16px;
      background: rgba(99, 102, 241, 0.05);
      border-radius: 8px;
      font-size: 0.85rem;
      color: var(--accent-1);
      display: none;
    }}
    .synonyms-info.show {{
      display: block;
    }}
    .results-header {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 20px;
    }}
    .results-count {{
      font-size: 0.9rem;
      color: var(--text-muted);
    }}
    .results-count strong {{
      color: var(--accent-1);
    }}
    .result-item {{
      display: block;
      padding: 20px 24px;
      background: var(--bg-secondary);
      border-radius: 12px;
      text-decoration: none;
      color: inherit;
      margin-bottom: 12px;
      transition: all 0.2s;
    }}
    .result-item:hover {{
      background: white;
      box-shadow: 0 4px 16px rgba(0,0,0,0.06);
      transform: translateX(4px);
    }}
    .result-title {{
      font-size: 1rem;
      font-weight: 500;
      color: var(--text);
      margin-bottom: 8px;
      line-height: 1.5;
    }}
    .result-item:hover .result-title {{
      color: var(--accent-1);
    }}
    .result-title mark {{
      background: rgba(245, 158, 11, 0.3);
      color: inherit;
      padding: 0 2px;
      border-radius: 2px;
    }}
    .result-meta {{
      font-size: 0.8rem;
      color: var(--text-muted);
    }}
    .result-journal {{
      display: inline-block;
      padding: 4px 10px;
      background: var(--border-light);
      border-radius: 6px;
      font-size: 0.75rem;
      font-weight: 500;
      color: var(--text-muted);
      margin-right: 12px;
    }}
    .no-results {{
      text-align: center;
      padding: 60px 20px;
      color: var(--text-muted);
    }}
    .no-results h3 {{
      font-size: 1.1rem;
      margin-bottom: 8px;
      color: var(--text);
    }}
    .initial-state {{
      text-align: center;
      padding: 60px 20px;
      color: var(--text-muted);
    }}
    .initial-state svg {{
      width: 48px;
      height: 48px;
      color: var(--border);
      margin-bottom: 16px;
    }}
  </style>
</head>
<body>
  {HEADER_HTML.format(seido_active="", articles_active="", journals_active="", search_active=' class="active"')}
  <main>
    <div class="page-header">
      <h1>キーワード検索</h1>
      <p>6つの学術誌からキーワードで論文を検索</p>
    </div>
    
    <div class="search-box">
      <div class="search-input-wrap">
        <input type="text" class="search-input" id="searchInput" placeholder="キーワードを入力（例: メンタルヘルス、ストレス）" />
        <button class="search-btn" onclick="doSearch()">検索</button>
      </div>
      <div class="search-options">
        <div class="search-option">
          <input type="radio" name="searchMode" id="exactMatch" value="exact" checked />
          <label for="exactMatch">完全一致</label>
        </div>
        <div class="search-option">
          <input type="radio" name="searchMode" id="synonymMatch" value="synonym" />
          <label for="synonymMatch">類義語も検索</label>
        </div>
      </div>
      <div class="synonyms-info" id="synonymsInfo"></div>
    </div>
    
    <div id="resultsArea">
      <div class="initial-state">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/>
        </svg>
        <p>キーワードを入力して検索してください</p>
      </div>
    </div>
  </main>
  
  <script>
    const articles = {json.dumps(articles_js, ensure_ascii=False)};
    const thesaurus = {json.dumps(thesaurus, ensure_ascii=False)};
    
    const searchInput = document.getElementById('searchInput');
    const synonymsInfo = document.getElementById('synonymsInfo');
    
    searchInput.addEventListener('keypress', (e) => {{
      if (e.key === 'Enter') doSearch();
    }});
    
    function getSynonyms(keyword) {{
      const kw = keyword.toLowerCase();
      let synonyms = [keyword];
      
      // 完全一致でシソーラスを検索
      for (const [key, values] of Object.entries(thesaurus)) {{
        if (key.toLowerCase() === kw || key.toLowerCase().includes(kw)) {{
          synonyms = synonyms.concat(values);
          synonyms.push(key);
        }}
        // 値にも含まれているかチェック
        for (const v of values) {{
          if (v.toLowerCase() === kw || v.toLowerCase().includes(kw)) {{
            synonyms = synonyms.concat(values);
            synonyms.push(key);
            break;
          }}
        }}
      }}
      
      return [...new Set(synonyms)];
    }}
    
    function highlightText(text, keywords) {{
      let result = text;
      for (const kw of keywords) {{
        const regex = new RegExp('(' + kw.replace(/[.*+?^${{}}()|[\\]\\\\]/g, '\\\\$&') + ')', 'gi');
        result = result.replace(regex, '<mark>$1</mark>');
      }}
      return result;
    }}
    
    function doSearch() {{
      const keyword = searchInput.value.trim();
      if (!keyword) return;
      
      const mode = document.querySelector('input[name="searchMode"]:checked').value;
      let searchTerms = [keyword];
      
      if (mode === 'synonym') {{
        searchTerms = getSynonyms(keyword);
        if (searchTerms.length > 1) {{
          synonymsInfo.innerHTML = '🔍 検索語: ' + searchTerms.join(', ');
          synonymsInfo.classList.add('show');
        }} else {{
          synonymsInfo.classList.remove('show');
        }}
      }} else {{
        synonymsInfo.classList.remove('show');
      }}
      
      const results = articles.filter(article => {{
        const text = (article.title + ' ' + article.authors.join(' ')).toLowerCase();
        return searchTerms.some(term => text.includes(term.toLowerCase()));
      }});
      
      renderResults(results, searchTerms);
    }}
    
    function renderResults(results, keywords) {{
      const area = document.getElementById('resultsArea');
      
      if (results.length === 0) {{
        area.innerHTML = `
          <div class="no-results">
            <h3>該当する論文が見つかりませんでした</h3>
            <p>別のキーワードをお試しください</p>
          </div>
        `;
        return;
      }}
      
      let html = `
        <div class="results-header">
          <span class="results-count"><strong>${{results.length}}</strong> 件の論文が見つかりました</span>
        </div>
      `;
      
      for (const r of results) {{
        const title = highlightText(r.title, keywords);
        const authors = r.authors.slice(0, 3).join(', ') + (r.authors.length > 3 ? ' 他' : '');
        const issue = r.year ? `${{r.year}}年 ${{r.volume}}巻${{r.number}}号` : '';
        
        html += `
          <a href="${{r.link}}" target="_blank" class="result-item">
            <div class="result-title">${{title}}</div>
            <div class="result-meta">
              <span class="result-journal">${{r.journal}}</span>
              ${{authors}}${{issue ? ' / ' + issue : ''}}
            </div>
          </a>
        `;
      }}
      
      area.innerHTML = html;
    }}
  </script>
</body>
</html>'''

def main():
    with open("data.json", encoding="utf-8") as f:
        data = json.load(f)
    
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(generate_index(data))
    
    with open("seido.html", "w", encoding="utf-8") as f:
        f.write(generate_seido(data))
    
    with open("articles.html", "w", encoding="utf-8") as f:
        f.write(generate_articles(data))
    
    with open("journals.html", "w", encoding="utf-8") as f:
        f.write(generate_journals(data))
    
    with open("search.html", "w", encoding="utf-8") as f:
        f.write(generate_search(data))
    
    print("Generated: index.html, seido.html, articles.html, journals.html, search.html")

if __name__ == "__main__":
    main()
