// Cloudflare Worker: J-STAGE API Proxy v2
// XMLパース改善版

const JSTAGE_API = "https://api.jstage.jst.go.jp/searchapi/do";

const JOURNALS = [
  "sangyoeisei",
  "indhealth", 
  "ohpfrev",
  "jjomh",
  "jaohn",
  "jaohl"
];

export default {
  async fetch(request) {
    if (request.method === "OPTIONS") {
      return new Response(null, {
        headers: {
          "Access-Control-Allow-Origin": "*",
          "Access-Control-Allow-Methods": "GET, OPTIONS",
          "Access-Control-Allow-Headers": "Content-Type",
        },
      });
    }

    const url = new URL(request.url);
    const journal = url.searchParams.get("journal");

    if (journal && JOURNALS.includes(journal)) {
      const data = await fetchJournal(journal);
      return jsonResponse(data);
    }

    if (url.pathname === "/all" || url.pathname === "/") {
      const results = await Promise.all(
        JOURNALS.map(async (id) => ({
          id,
          articles: await fetchJournal(id),
        }))
      );
      return jsonResponse({
        updated: new Date().toISOString(),
        journals: results,
      });
    }

    return jsonResponse({ error: "Invalid request" }, 400);
  },
};

async function fetchJournal(journalId) {
  const apiUrl = `${JSTAGE_API}?service=3&cdjournal=${journalId}&count=5&sortflg=2`;
  
  try {
    const response = await fetch(apiUrl, {
      headers: { "User-Agent": "SanpoPortal/1.0" },
    });
    const xml = await response.text();
    return parseXml(xml);
  } catch (e) {
    console.error(`Error fetching ${journalId}:`, e);
    return [];
  }
}

function extractCDATA(str) {
  // CDATA内のテキストを抽出
  const match = str.match(/<!\[CDATA\[([\s\S]*?)\]\]>/);
  if (match) return match[1].trim();
  // CDATAがない場合はタグ内のテキストを返す
  return str.replace(/<[^>]+>/g, '').trim();
}

function parseXml(xml) {
  const articles = [];
  
  // entry単位で分割
  const entryMatches = xml.match(/<entry>([\s\S]*?)<\/entry>/g);
  if (!entryMatches) return [];
  
  for (const entryBlock of entryMatches) {
    const entry = entryBlock;
    
    // タイトル取得
    let title = "";
    
    // 1. article_title/ja を試す
    const articleTitleMatch = entry.match(/<article_title>([\s\S]*?)<\/article_title>/);
    if (articleTitleMatch) {
      const articleTitle = articleTitleMatch[1];
      const jaMatch = articleTitle.match(/<ja>([\s\S]*?)<\/ja>/);
      if (jaMatch) {
        title = extractCDATA(jaMatch[1]);
      }
      // 日本語がなければ英語
      if (!title) {
        const enMatch = articleTitle.match(/<en>([\s\S]*?)<\/en>/);
        if (enMatch) {
          title = extractCDATA(enMatch[1]);
        }
      }
    }
    
    // 2. フォールバック: titleタグ
    if (!title) {
      const titleMatch = entry.match(/<title>([\s\S]*?)<\/title>/);
      if (titleMatch) {
        const t = extractCDATA(titleMatch[1]);
        if (t && !t.startsWith("http")) {
          title = t;
        }
      }
    }
    
    if (!title) continue;

    // 著者取得
    const authors = [];
    const authorMatch = entry.match(/<author>([\s\S]*?)<\/author>/);
    if (authorMatch) {
      const authorBlock = authorMatch[1];
      // 日本語著者を優先
      let nameBlock = "";
      const jaAuthor = authorBlock.match(/<ja>([\s\S]*?)<\/ja>/);
      if (jaAuthor) {
        nameBlock = jaAuthor[1];
      } else {
        const enAuthor = authorBlock.match(/<en>([\s\S]*?)<\/en>/);
        if (enAuthor) {
          nameBlock = enAuthor[1];
        }
      }
      // <n>タグから名前を抽出
      const nameMatches = nameBlock.match(/<n>([\s\S]*?)<\/n>/g);
      if (nameMatches) {
        for (const nm of nameMatches) {
          const name = extractCDATA(nm.replace(/<\/?n>/g, ''));
          if (name) authors.push(name);
        }
      }
    }

    // 巻号・年
    const volume = entry.match(/<(?:prism:)?volume>(\d+)<\/(?:prism:)?volume>/)?.[1] || "";
    const number = entry.match(/<(?:prism:)?number>([^<]+)<\/(?:prism:)?number>/)?.[1] || "";
    const year = entry.match(/<pubyear>(\d+)<\/pubyear>/)?.[1] || "";

    // リンク
    const link = entry.match(/<link[^>]*href="([^"]+)"/)?.[1] || "";

    articles.push({ title, authors, volume, number, year, link });
  }

  return articles.slice(0, 5);
}

function jsonResponse(data, status = 200) {
  return new Response(JSON.stringify(data), {
    status,
    headers: {
      "Content-Type": "application/json",
      "Access-Control-Allow-Origin": "*",
      "Cache-Control": "public, max-age=3600",
    },
  });
}
