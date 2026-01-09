// netlify/functions/expand-query.js
// Claude APIを使って検索キーワードの類義語・関連語を動的に生成

export async function handler(event) {
  // CORSヘッダー
  const headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Allow-Methods': 'POST, OPTIONS',
    'Content-Type': 'application/json'
  };

  // OPTIONSリクエスト（プリフライト）への対応
  if (event.httpMethod === 'OPTIONS') {
    return { statusCode: 200, headers, body: '' };
  }

  // POSTのみ受付
  if (event.httpMethod !== 'POST') {
    return {
      statusCode: 405,
      headers,
      body: JSON.stringify({ error: 'Method not allowed' })
    };
  }

  try {
    const { query } = JSON.parse(event.body);

    if (!query || query.trim() === '') {
      return {
        statusCode: 400,
        headers,
        body: JSON.stringify({ error: 'Query is required' })
      };
    }

    // Claude API呼び出し
    const response = await fetch('https://api.anthropic.com/v1/messages', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'x-api-key': process.env.CLAUDE_API_KEY,
        'anthropic-version': '2023-06-01'
      },
      body: JSON.stringify({
        model: 'claude-3-haiku-20240307',
        max_tokens: 300,
        messages: [{
          role: 'user',
          content: `あなたは産業保健・労働衛生分野の専門家です。
検索キーワード「${query}」に対して、産業保健分野で関連性の高い類義語・関連語を生成してください。

ルール：
- 日本語と英語の両方を含める
- 略語があれば含める（例：EAP、THP）
- 専門用語と一般用語の両方
- 最大15個まで
- JSON配列形式のみで出力（説明不要）

出力例：
["メンタルヘルス","精神保健","心の健康","mental health","ストレス","うつ","EAP"]`
        }]
      })
    });

    if (!response.ok) {
      const errorData = await response.text();
      console.error('Claude API Error:', errorData);
      return {
        statusCode: 500,
        headers,
        body: JSON.stringify({ error: 'Claude API error', details: errorData })
      };
    }

    const data = await response.json();
    const content = data.content[0].text;

    // JSONをパース（余計な文字があれば除去）
    let synonyms;
    try {
      // JSON配列部分を抽出
      const jsonMatch = content.match(/\[[\s\S]*\]/);
      if (jsonMatch) {
        synonyms = JSON.parse(jsonMatch[0]);
      } else {
        synonyms = JSON.parse(content);
      }
    } catch (parseError) {
      console.error('Parse error:', content);
      // パース失敗時は元のクエリのみ返す
      synonyms = [query];
    }

    // 元のクエリを先頭に追加（重複排除）
    const allTerms = [query, ...synonyms.filter(s => s.toLowerCase() !== query.toLowerCase())];

    return {
      statusCode: 200,
      headers,
      body: JSON.stringify({
        original: query,
        synonyms: allTerms,
        count: allTerms.length
      })
    };

  } catch (error) {
    console.error('Function error:', error);
    return {
      statusCode: 500,
      headers,
      body: JSON.stringify({ error: 'Internal server error', message: error.message })
    };
  }
}
