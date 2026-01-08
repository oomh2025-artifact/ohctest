const JOURNALS = [
  { id: "sangyoeisei", name: "産業衛生学雑誌", publisher: "日本産業衛生学会", color: "#0066cc", cdjournal: "sangyoeisei" },
  { id: "indhealth", name: "Industrial Health", publisher: "労働安全衛生総合研究所", color: "#006644", cdjournal: "indhealth" },
  { id: "ohpfrev", name: "産業医学レビュー", publisher: "産業医学振興財団", color: "#cc3300", cdjournal: "ohpfrev" },
  { id: "jjomh", name: "産業精神保健", publisher: "日本産業精神保健学会", color: "#9933cc", cdjournal: "jjomh" },
  { id: "jaohn", name: "日本産業看護学会誌", publisher: "日本産業看護学会", color: "#e91e63", cdjournal: "jaohn" },
  { id: "jaohl", name: "産業保健法学会誌", publisher: "日本産業保健法学会", color: "#336699", cdjournal: "jaohl" },
];

async function fetchJournal(j) {
  try {
    const url = "https://api.jstage.jst.go.jp/searchapi/do?service=3&cdjournal=" + j.cdjournal + "&count=5";
    const controller = new AbortController();
    const tid = setTimeout(() => controller.abort(), 8000);
    const res = await fetch(url, { signal: controller.signal });
    clearTimeout(tid);
    if (!res.ok) throw new Error("HTTP " + res.status);
    const xml = await res.text();
    
    const articles = [];
    const entries = xml.split("<entry>");
    
    for (let i = 1; i < entries.length && articles.length < 3; i++) {
      const entry = entries[i];
      let title = "";
      
      // タイトル取得（複数パターン対応）
      let m = entry.match(/<article_title>[\s\S]*?<ja>([^<]+)<\/ja>/);
      if (m) title = m[1];
      if (!title) { m = entry.match(/<article_title>([^<]+)<\/article_title>/); if (m) title = m[1]; }
      if (!title) { m = entry.match(/<title[^>]*>([^<]+)<\/title>/); if (m) title = m[1]; }
      
      title = (title || "").replace(/<[^>]+>/g, "").replace(/\s+/g, " ").trim();
      
      // 著者取得（nameタグ対応）
      let authors = "";
      const authorMatch = entry.match(/<author>([\s\S]*?)<\/author>/);
      if (authorMatch) {
        const names = [];
        const re = /<n>([^<]+)<\/n>/g;
        let nm;
        while ((nm = re.exec(authorMatch[1])) !== null) names.push(nm[1].trim());
        if (names.length > 2) authors = names[0] + " 他";
        else if (names.length > 0) authors = names.join(", ");
      }
      
      if (title && title.length > 3) articles.push({ title: title.slice(0, 100), authors });
    }
    
    // 巻号取得
    let issue = "";
    if (entries[1]) {
      const e = entries[1];
      const vol = e.match(/<prism:volume>(\d+)<\/prism:volume>/);
      const no = e.match(/<prism:number>(\d+)<\/prism:number>/);
      const year = e.match(/<pubyear>(\d+)<\/pubyear>/);
      if (vol) {
        if (year) issue += year[1] + "年 ";
        issue += vol[1] + "巻";
        if (no) issue += no[1] + "号";
      }
    }
    
    return { id: j.id, name: j.name, publisher: j.publisher, color: j.color, url: "https://www.jstage.jst.go.jp/browse/" + j.cdjournal + "/-char/ja", latest_issue: issue, articles };
  } catch (e) {
    console.error(j.name + ": " + e.message);
    return { id: j.id, name: j.name, publisher: j.publisher, color: j.color, url: "https://www.jstage.jst.go.jp/browse/" + j.cdjournal + "/-char/ja", latest_issue: "", articles: [] };
  }
}

export async function handler(event) {
  const headers = { "Access-Control-Allow-Origin": "*", "Content-Type": "application/json; charset=utf-8", "Cache-Control": "public, max-age=3600" };
  if (event.httpMethod === "OPTIONS") return { statusCode: 200, headers, body: "" };
  try {
    const results = await Promise.all(JOURNALS.map(fetchJournal));
    return { statusCode: 200, headers, body: JSON.stringify({ updated_at: new Date().toISOString().split("T")[0], journals: results }) };
  } catch (e) {
    return { statusCode: 500, headers, body: JSON.stringify({ error: e.message }) };
  }
}
