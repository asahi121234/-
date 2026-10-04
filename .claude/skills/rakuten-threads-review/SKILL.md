---
name: rakuten-threads-review
description: 楽天×Threadsアフィリエイトの週次振り返り。投稿の反応と成果を投稿ログに反映し、売れた投稿と売れなかった投稿を比較して learnings.md を更新する。「振り返り」「今週の結果」「なぜ売れないか分析」「成果を反映」などで使う。
---

# 楽天×Threads 週次振り返り

## 1. 結果を投稿ログに入れる
`status=posted` の投稿について、次の数値を集める。
- **Threadsの反応**（閲覧数・いいね・返信）
  - SNS分析用のMCPツール（Typefullyなど）が使えれば、そこから取得する
  - 使えなければ、ユーザーにThreadsのインサイトの数値を聞く
- **クリック数・売上**：楽天アフィリエイトの成果レポートから取る
  - ユーザーが `affiliate/data/results/` にレポートのCSVを置いていれば、それを読む。読み方は列名を見て判断し、自信がなければユーザーに確認する
  - 楽天の成果は、確定までに時間がかかる。対象期間を明記すること
  - 投稿と成果が1対1で結びつかない場合（別の商品が買われた場合など）は、無理に割り当てず、`notes` に書く

更新は `python3 affiliate/scripts/log_post.py update <post_id> views=.. likes=.. replies=.. clicks=.. sales=.. revenue=..` で行う。

## 2. 分析（rt-analyst）
Agentツールで `rt-analyst` を呼ぶ。`learnings.md` の更新までを任せる。

## 3. 報告
ユーザーには次の内容を短く伝える。
- 今週の数字（投稿数、閲覧数、クリック数、売上）
- 分かったこと（件数を添え、仮説かどうかも明記）
- 来週試すこと

## 4. 変更を保存する
`affiliate/data/` の変更をコミットしてプッシュする。
