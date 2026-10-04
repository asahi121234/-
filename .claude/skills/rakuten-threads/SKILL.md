---
name: rakuten-threads
description: 楽天アフィリエイトのThreads投稿を作る司令塔。リサーチ→選定→執筆→審査のサブエージェントを順に回し、合格した投稿を下書きとして保存（またはTypefullyに下書き登録）する。「Threadsの投稿作って」「楽天アフィの投稿」「今週分の投稿」「アフィリエイト投稿を作成」などで使う。
---

# 楽天×Threads 投稿作成（司令塔）

あなたは司令塔です。各担当（サブエージェント）に仕事を渡して結果をつなぎます。**投稿の操作をするのは司令塔だけ**です（二重投稿を防ぐため）。

## 0. 準備
- 作業用ディレクトリを作る：`WORK=$(mktemp -d)`。各担当には、このパスを `$WORK` として依頼文に書いて渡す
- `affiliate/config.json` を読み、`posts_per_run` と `review.max_revisions` を確認する
- 環境変数 `RAKUTEN_APP_ID` と `RAKUTEN_AFFILIATE_ID` があるかを、値は表示せずに確認する：`[ -n "$RAKUTEN_APP_ID" ] && echo set`
  - ない場合は**サンプルモード**で動かし、最後に「サンプルデータなので投稿しないこと」と明記する
- ユーザーが件数やジャンルを指定していれば、それを優先する

## 1. リサーチ（rt-researcher）
Agentツールで `rt-researcher` を呼ぶ。依頼文には `$WORK` のパスと、サンプルモードかどうかを書く。
返ってきた `notes` にAPIエラーがあれば、そこで止めてユーザーに報告する。

## 2. 選定（rt-selector）
`rt-selector` に、候補一覧のJSONと件数（`posts_per_run`）を渡す。
`selected` が0件なら、理由を添えて終了する。

## 3. 執筆（rt-writer）
`rt-writer` に、選ばれた商品の**商品データ全体**と、選定担当の `target`・`angle` を渡す。

## 4. 審査（rt-reviewer）とやり直し
- `rt-reviewer` に、下書きと元の商品データを渡す。依頼文には `$WORK` のパスも書く
- 商品ごとに、合格した下書きが1つもなければ、`fix_instructions` を付けて `rt-writer` に差し戻し、もう一度審査する
- やり直しは**最大 `max_revisions` 回**まで。それでも合格しなければ、その商品は見送る
- 審査担当が合格にした下書きを、司令塔が勝手に書き換えない

## 5. 保存と記録
商品ごとに `best: true` の下書きを1件選ぶ。

1. **投稿ログに追加**：下書きを `$WORK/log.json` に書き出してから、`python3 affiliate/scripts/log_post.py add $WORK/log.json` を実行する
   - 下書きのJSONに入れる項目は `item_code, item_name, genre_id, genre_name, rank, price, review_average, review_count, hook_type, style, has_image, affiliate_url, text` で、`status` は `draft` にする
   - サンプルモードのときは記録しない
2. **投稿先**
   - Typefullyなど**SNS予約投稿のMCPツールが使える場合**：**下書きとして**登録する（予約公開や即時公開はしない）。ユーザーが明示的に頼んだときだけ予約する
   - **使えない場合**：`affiliate/drafts/YYYY-MM-DD.md` に、コピーしやすい形で書き出す
3. ユーザーに報告する（下書きの本文、見送った商品と理由、次にユーザーがすること）

## 6. 投稿後（ユーザーから報告があったとき）
- 投稿した：`python3 affiliate/scripts/log_post.py update <post_id> status=posted posted_at=<ISO日時> post_hour=<時>`
- 見送った：`python3 affiliate/scripts/log_post.py update <post_id> status=skipped`

## 7. 変更を保存する
クラウド環境は作業が終わると消えるので、`affiliate/data/` と `affiliate/drafts/` の変更をコミットしてプッシュする。

## 守ること
- APIキーやトークンを、表示・記録・コミットしない
- 商品データにない情報を足さない
- 最初の運用期間は、ユーザーの承認なしに公開しない
