# 産業保健情報ポータル

産業保健に関する法令・ガイドライン・学術情報を集約したポータルサイトです。

## 機能

- **制度改正**: 産業保健関連の法令・ガイドライン改正情報
- **最新記事**: J-STAGEから自動取得した各学術誌の最新論文
- **雑誌一覧**: 無料で閲覧可能な産業保健関連学術誌の紹介

## 対象学術誌（J-STAGE）

| 雑誌名 | 発行元 |
|--------|--------|
| 産業衛生学雑誌 | 日本産業衛生学会 |
| Industrial Health | 労働安全衛生総合研究所 |
| 産業医学レビュー | 産業医学振興財団 |
| 産業精神保健 | 日本産業精神保健学会 |
| 日本産業看護学会誌 | 日本産業看護学会 |
| 産業保健法学会誌 | 日本産業保健法学会 |

## 自動更新

GitHub Actionsにより、毎日日本時間の朝6時にJ-STAGEから最新の論文情報を取得し、`data/articles.json`を更新します。

### 手動更新

Actions タブから「Update Articles from J-STAGE」ワークフローを手動実行することもできます。

## デプロイ

GitHub PagesまたはNetlifyで静的サイトとしてホスティングできます。

### GitHub Pages

1. Settings → Pages
2. Source: Deploy from a branch
3. Branch: main, / (root)
4. Save

### Netlify

1. New site from Git
2. リポジトリを選択
3. Build command: (空欄)
4. Publish directory: ./
5. Deploy

## ファイル構成

```
├── index.html                 # メインHTML
├── data/
│   └── articles.json          # 論文データ（自動更新）
├── scripts/
│   └── fetch_articles.py      # J-STAGEスクレイピング
└── .github/
    └── workflows/
        └── update-articles.yml # 自動更新ワークフロー
```

## ライセンス

MIT License
