#!/usr/bin/env python3
"""
J-STAGEのページをスクレイピングして最新論文情報を取得し、JSONファイルに保存する
"""

import requests
from bs4 import BeautifulSoup
import json
import os
import re
from datetime import datetime

# 対象雑誌の設定
JOURNALS = [
    {
        "id": "sangyoeisei",
        "name": "産業衛生学雑誌",
        "publisher": "日本産業衛生学会",
        "color": "#0066cc",
        "url": "https://www.jstage.jst.go.jp/browse/sangyoeisei/-char/ja",
        "description": "日本産業衛生学会の機関誌。原著論文、総説、事例報告などを掲載。"
    },
    {
        "id": "indhealth",
        "name": "Industrial Health",
        "publisher": "労働安全衛生総合研究所",
        "color": "#006644",
        "url": "https://www.jstage.jst.go.jp/browse/indhealth/-char/ja",
        "description": "国際的査読付き英文誌。産業医学、人間工学、産業衛生など幅広い分野をカバー。"
    },
    {
        "id": "ohpfrev",
        "name": "産業医学レビュー",
        "publisher": "産業医学振興財団",
        "color": "#cc3300",
        "url": "https://www.jstage.jst.go.jp/browse/ohpfrev/-char/ja",
        "description": "産業医学領域の重要テーマについて専門家による総説論文を掲載。"
    },
    {
        "id": "jjomh",
        "name": "産業精神保健",
        "publisher": "日本産業精神保健学会",
        "color": "#9933cc",
        "url": "https://www.jstage.jst.go.jp/browse/jjomh/-char/ja",
        "description": "職場のメンタルヘルスに特化した専門誌。"
    },
    {
        "id": "jaohn",
        "name": "日本産業看護学会誌",
        "publisher": "日本産業看護学会",
        "color": "#e91e63",
        "url": "https://www.jstage.jst.go.jp/browse/jaohn/-char/ja",
        "description": "産業看護の実践、教育、両立支援における看護職の役割などを掲載。"
    },
    {
        "id": "jaohl",
        "name": "産業保健法学会誌",
        "publisher": "日本産業保健法学会",
        "color": "#336699",
        "url": "https://www.jstage.jst.go.jp/browse/jaohl/-char/ja",
        "description": "産業保健法学に関する専門誌。法の知見を基礎に現場課題の解決を探求。"
    },
]

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'ja,en-US;q=0.7,en;q=0.3',
}

def fetch_articles_from_jstage(url, max_articles=3):
    """J-STAGEのページから最新論文を取得"""
    try:
        response = requests.get(url, headers=HEADERS, timeout=30)
        response.raise_for_status()
        response.encoding = 'utf-8'
        
        soup = BeautifulSoup(response.text, 'html.parser')
        articles = []
        
        # 最新号の巻号情報を取得
        latest_issue = ""
        # パターン1: search-resultslabel
        issue_elem = soup.select_one('.search-resultslabel, .issue-header, h2.issue-title')
        if issue_elem:
            latest_issue = issue_elem.get_text(strip=True)
        
        # パターン2: 「年 巻 号」形式を探す
        if not latest_issue:
            year_vol_pattern = re.compile(r'\d{4}\s*年?\s*\d+\s*巻\s*\d+\s*号')
            for text in soup.stripped_strings:
                match = year_vol_pattern.search(text)
                if match:
                    latest_issue = match.group()
                    break
        
        # 論文リストを取得 - 複数のセレクタを試す
        selectors = [
            '.search-list-article',
            '.article-list-item', 
            '.c-toc__entry',
            'div[class*="article"]',
            '.resultlist li',
            'li.article',
        ]
        
        article_items = []
        for selector in selectors:
            article_items = soup.select(selector)
            if article_items:
                break
        
        # 記事が見つからない場合、リンクから探す
        if not article_items:
            # /article/ を含むリンクを探す
            all_links = soup.find_all('a', href=re.compile(r'/article/'))
            seen_titles = set()
            for link in all_links:
                title = link.get_text(strip=True)
                if title and len(title) > 10 and title not in seen_titles:
                    seen_titles.add(title)
                    href = link.get('href', '')
                    if href and not href.startswith('http'):
                        href = 'https://www.jstage.jst.go.jp' + href
                    
                    # 著者を探す（親要素から）
                    authors = ""
                    parent = link.find_parent(['div', 'li', 'article'])
                    if parent:
                        author_elem = parent.find(class_=re.compile(r'author'))
                        if author_elem:
                            authors = author_elem.get_text(strip=True)
                    
                    articles.append({
                        "title": title,
                        "authors": authors[:50] if authors else "",
                        "link": href
                    })
                    
                    if len(articles) >= max_articles:
                        break
        else:
            for item in article_items[:max_articles]:
                title = ""
                authors = ""
                link = ""
                
                # タイトルを取得
                title_elem = (
                    item.select_one('a.title, .article-title a, a[href*="/article/"]') or
                    item.find('a')
                )
                if title_elem:
                    title = title_elem.get_text(strip=True)
                    href = title_elem.get('href', '')
                    if href:
                        if not href.startswith('http'):
                            link = 'https://www.jstage.jst.go.jp' + href
                        else:
                            link = href
                
                # 著者を取得
                author_elem = item.select_one('.article-author, .author, [class*="author"]')
                if author_elem:
                    authors = author_elem.get_text(strip=True)
                    # 著者が長い場合は短縮
                    if len(authors) > 40:
                        author_list = re.split(r'[,、，]', authors)
                        if len(author_list) > 1:
                            authors = author_list[0].strip() + ' 他'
                
                if title and len(title) > 5:  # タイトルが有効な場合のみ追加
                    articles.append({
                        "title": title[:100],  # 長すぎるタイトルは切り詰め
                        "authors": authors,
                        "link": link
                    })
        
        return {
            "latest_issue": latest_issue,
            "articles": articles
        }
        
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return {
            "latest_issue": "",
            "articles": []
        }

def main():
    """メイン処理"""
    result = {
        "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "journals": []
    }
    
    for journal in JOURNALS:
        print(f"Fetching: {journal['name']}...")
        data = fetch_articles_from_jstage(journal['url'])
        
        journal_data = {
            "id": journal['id'],
            "name": journal['name'],
            "publisher": journal['publisher'],
            "color": journal['color'],
            "url": journal['url'],
            "description": journal['description'],
            "latest_issue": data['latest_issue'],
            "articles": data['articles']
        }
        
        result["journals"].append(journal_data)
        print(f"  -> Issue: {data['latest_issue']}")
        for i, art in enumerate(data['articles'], 1):
            print(f"     {i}. {art['title'][:40]}...")
    
    # JSONファイルに保存
    output_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'articles.json')
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    
    print(f"\n✓ Saved to {output_path}")
    print(f"✓ Updated at: {result['updated_at']}")

if __name__ == "__main__":
    main()
