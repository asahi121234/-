# 楽天アフィリエイト × Threads 自動投稿の仕組み

楽天の売れ筋から商品を選び、ルールを守った投稿文を作って下書きにします。週に1回、結果を振り返って精度を上げていきます。

## 体制

```
司令塔スキル（rakuten-threads）
  ├─ ① rt-researcher  候補集め（楽天ランキングAPI ＋ 機械的な絞り込み）
  ├─ ② rt-selector    売れそうかの判断
  ├─ ③ rt-writer      投稿文を2パターン書く
  ├─ ④ rt-reviewer    厳しく審査（不合格ならライターに差し戻す。最大2回）
  └─ ⑤ 司令塔だけが下書き保存・Typefullyへ下書き登録

週次スキル（rakuten-threads-review）
  └─ ⑥ rt-analyst     売れた/売れない投稿を比べて learnings.md を更新
```

## ファイル

| パス | 内容 |
|---|---|
| `config.json` | ジャンル、絞り込み条件、1回に作る投稿数 |
| `rules/posting_rules.md` | 投稿ルール（PR表記・禁止事項） |
| `rules/ng_words.txt` | NGワード一覧（追加して育てる） |
| `data/posts_log.csv` | 投稿ログ（特徴と結果） |
| `data/learnings.md` | 振り返りで分かったこと。ライターが毎回読む |
| `data/results/` | 楽天の成果レポートCSVの置き場所（コミットされない） |
| `drafts/` | 投稿文の下書き（Typefullyが使えないとき） |
| `scripts/` | 取得・絞り込み・チェック・記録・集計のスクリプト（標準ライブラリのみ） |

## 使い方

Claude Codeに次のように話しかけます。
- 「Threadsの投稿を作って」→ 司令塔スキルが動きます
- 「今週の振り返りをして」→ 週次スキルが動きます
- 「〇〇（post_id）を投稿した」→ 投稿ログを更新します

APIキーがなくても、サンプルデータで流れを試せます。

## セットアップ（あなたがすること）

1. **楽天アフィリエイト**に登録し、アフィリエイトIDを取得する
2. **楽天ウェブサービス**でアプリを登録し、アプリIDを取得する
3. Claude Codeのクラウド環境の設定に、環境変数として登録する（チャットに貼らないこと）
   - `RAKUTEN_APP_ID`
   - `RAKUTEN_AFFILIATE_ID`
   - 楽天側でアクセスキーも必要な場合は `RAKUTEN_ACCESS_KEY`
4. 同じ環境設定の **Network access** で、`app.rakuten.co.jp` へのアクセスを許可する
5. **Threads**のアカウントを作る。（任意）claude.aiのConnectorsで**Typefully**をつなぐと、下書き登録まで自動になります

> 楽天APIのエンドポイントやパラメータは変わることがあります。最初に動かすときに公式ドキュメントと照らし合わせ、違っていれば `RAKUTEN_RANKING_URL` で差し替えられます。`config.json` のジャンルIDも確認してください。

## 注意
- **このリポジトリは公開（public）になっています。** 投稿ログには売上の数字も入るため、非公開にするか、別の非公開リポジトリに移すことをおすすめします。
- ステマ規制により、アフィリエイト投稿には `#PR` などの表記が必要です。審査担当と `check_post.py` が必ず確認します。
- 最初のうちは、公開前に必ず自分の目で確認してください。

## テスト
```
python3 -m unittest discover affiliate/tests
```
