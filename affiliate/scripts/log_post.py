"""投稿ログ（data/posts_log.csv）への追加と更新。

使い方:
  # 下書きを追加（JSONは1件のオブジェクトか配列）
  python3 affiliate/scripts/log_post.py add drafts.json

  # 状態や結果を更新
  python3 affiliate/scripts/log_post.py update <post_id> status=posted posted_at=2026-10-05T08:00:00+09:00
  python3 affiliate/scripts/log_post.py update <post_id> views=1200 likes=15 clicks=8 sales=1 revenue=120
"""

import json
import sys
import uuid
from datetime import datetime, timezone

from common import LOG_COLUMNS, read_log, write_log


def add(path):
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    entries = data if isinstance(data, list) else [data]

    rows = read_log()
    now = datetime.now(timezone.utc).isoformat()
    added = []
    for entry in entries:
        row = {col: entry.get(col, "") for col in LOG_COLUMNS}
        row["post_id"] = row["post_id"] or uuid.uuid4().hex[:10]
        row["created_at"] = row["created_at"] or now
        row["status"] = row["status"] or "draft"
        row["char_count"] = row["char_count"] or len(entry.get("text", ""))
        rows.append(row)
        added.append(row["post_id"])
    write_log(rows)
    print(json.dumps({"added": added}, ensure_ascii=False))


def update(post_id, pairs):
    rows = read_log()
    target = next((r for r in rows if r["post_id"] == post_id), None)
    if target is None:
        sys.exit(f"post_id {post_id} が見つかりません。")
    for pair in pairs:
        key, _, value = pair.partition("=")
        if key not in LOG_COLUMNS:
            sys.exit(f"不明な項目: {key}")
        target[key] = value
    write_log(rows)
    print(json.dumps({"updated": post_id}, ensure_ascii=False))


def main():
    if len(sys.argv) >= 3 and sys.argv[1] == "add":
        add(sys.argv[2])
    elif len(sys.argv) >= 4 and sys.argv[1] == "update":
        update(sys.argv[2], sys.argv[3:])
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    main()
