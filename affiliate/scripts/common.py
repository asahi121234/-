"""各スクリプトで共有するパス・設定・投稿ログの定義。"""

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONFIG_PATH = ROOT / "config.json"
NG_WORDS_PATH = ROOT / "rules" / "ng_words.txt"
POSTS_LOG_PATH = ROOT / "data" / "posts_log.csv"

LOG_COLUMNS = [
    "post_id",
    "created_at",
    "posted_at",
    "status",  # draft / posted / skipped
    "item_code",
    "item_name",
    "genre_id",
    "genre_name",
    "rank",
    "price",
    "review_average",
    "review_count",
    "hook_type",  # 悩み提起 / 数字 / 質問 など
    "style",  # 文体の種類
    "char_count",
    "has_image",
    "post_hour",
    "affiliate_url",
    "text",
    "views",
    "likes",
    "replies",
    "clicks",
    "sales",
    "revenue",
    "notes",
]


def load_config():
    with CONFIG_PATH.open(encoding="utf-8") as f:
        return json.load(f)


def load_ng_words():
    words = []
    for line in NG_WORDS_PATH.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#"):
            words.append(line)
    return words


def read_log():
    if not POSTS_LOG_PATH.exists():
        return []
    with POSTS_LOG_PATH.open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def write_log(rows):
    POSTS_LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with POSTS_LOG_PATH.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=LOG_COLUMNS, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({col: row.get(col, "") for col in LOG_COLUMNS})


def to_float(value, default=0.0):
    try:
        return float(value)
    except (TypeError, ValueError):
        return default
