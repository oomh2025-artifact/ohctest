const https = require('https');

// 対象の6誌のみに絞る
const TARGET_JOURNALS = ['sangyoeisei', 'indhealth', 'ohpfrev', 'jjomh', 'jaohn', 'jaohl'];

function searchJstage(keyword) {
  return new Promise((resolve, reject) => {
    // 6誌に絞って検索
    const journalParam = TARGET_JOURNALS.map(j => `cdjournal=${j}`).join('&');
    const url = `https://api.jstage.jst.go.jp/searchapi/do?service=3&keyword=${encodeURIComponent(keyword)}&count=50&${journalParam}`;
    
    https.get(url, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => resolve(data));
    }).on('error', reject);
  });
}

function parseResults(xml) {
  const results = [];
  const entries = xml.split('<entry>').slice(1);
  
  for (const entry of entries) {
    // タイトル
    let title = '';
    let m = entry.match(/article_title[\s\S]*?<ja>[\s\S]*?CDATA\[([\s\S]*?)\]\]/);
    if (m) title = m[1].trim();
    if (!title) {
      m = entry.match(/article_title[\s\S]*?<en>[\s\S]*?CDATA\[([\s\S]*?)\]\]/);
      if (m) title = m[1].trim();
    }
    if (!title) {
      m = entry.match(/<title>[\s\S]*?CDATA\[([\s\S]*?)\]\]/);
      if (m && !m[1].startsWith('http')) title = m[1].trim();
    }
    
    if (!title || title.length < 3) continue;
    
    // 著者
    const authors = [];
    const authorMatch = entry.match(/<author>([\s\S]*?)<\/author>/);
    if (authorMatch) {
      const block = authorMatch[1];
      const jaBlock = block.match(/<ja>([\s\S]*?)<\/ja>/);
      const names = (jaBlock ? jaBlock[1] : block).match(/CDATA\[([\s\S]*?)\]\]/g) || [];
      for (const n of names) {
        const name = n.replace(/CDATA\[|\]\]/g, '').trim();
        if (name) authors.push(name);
      }
    }
    
    // 抄録（abstract）
    let abstract = '';
    const absMatch = entry.match(/<abstract>([\s\S]*?)<\/abstract>/);
    if (absMatch) {
      const absBlock = absMatch[1];
      // 日本語優先
      let absJa = absBlock.match(/<ja>[\s\S]*?CDATA\[([\s\S]*?)\]\]/);
      if (absJa) {
        abstract = absJa[1].trim();
      } else {
        // 英語フォールバック
        let absEn = absBlock.match(/<en>[\s\S]*?CDATA\[([\s\S]*?)\]\]/);
        if (absEn) abstract = absEn[1].trim();
      }
    }
    // 150文字で切る
    if (abstract.length > 150) {
      abstract = abstract.substring(0, 150) + '...';
    }
    
    // 雑誌名
    let journal = '';
    const cdj = entry.match(/cdjournal>([^<]+)</);
    if (cdj) {
      const journalNames = {
        'sangyoeisei': '産業衛生学雑誌',
        'indhealth': 'Industrial Health',
        'ohpfrev': '産業医学レビュー',
        'jjomh': '産業精神保健',
        'jaohn': '日本産業看護学会誌',
        'jaohl': '産業保健法学会誌'
      };
      journal = journalNames[cdj[1]] || cdj[1];
    }
    
    // 巻号年
    const vol = entry.match(/volume>(\d+)</);
    const num = entry.match(/number>([^<]+)</);
    const year = entry.match(/pubyear>(\d+)</);
    const link = entry.match(/link[^>]*href="([^"]+)"/);
    
    results.push({
      title,
      authors: authors.slice(0, 5),
      abstract,
      journal,
      volume: vol ? vol[1] : '',
      number: num ? num[1] : '',
      year: year ? year[1] : '',
      link: link ? link[1] : ''
    });
  }
  
  return results;
}

exports.handler = async function(event) {
  const headers = {
    'Access-Control-Allow-Origin': '*',
    'Content-Type': 'application/json; charset=utf-8'
  };
  
  // クエリパラメータからキーワード取得
  const keyword = event.queryStringParameters?.q;
  
  if (!keyword) {
    return {
      statusCode: 400,
      headers,
      body: JSON.stringify({ error: 'キーワードを指定してください' })
    };
  }
  
  try {
    const xml = await searchJstage(keyword);
    const results = parseResults(xml);
    
    return {
      statusCode: 200,
      headers,
      body: JSON.stringify({ results, count: results.length })
    };
  } catch (e) {
    return {
      statusCode: 500,
      headers,
      body: JSON.stringify({ error: e.message })
    };
  }
};
