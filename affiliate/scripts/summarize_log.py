"""投稿ログを特徴ごとに集計し、振り返り担当が比較しやすい形で出力する。

使い方:
  python3 affiliate/scripts/summarize_log.py

投稿済み（status=posted）のみ対象。件数が min_samples_for_trend 未満の項目は
"enough_data": false になるので、傾向として断定しないこと。
"""

import json
import sys
from collections import defaultdict

from common import load_config, read_log, to_float


def price_band(price):
    p = to_float(price)
    if p < 2000:
        return "〜2千円"
    if p < 5000:
        return "2千〜5千円"
    if p < 10000:
        return "5千〜1万円"
    return "1万円〜"


def time_band(hour):
    try:
        h = int(hour)
    except (TypeError, ValueError):
        return "不明"
    if 5 <= h < 11:
        return "朝"
    if 11 <= h < 17:
        return "昼"
    if 17 <= h < 24:
        return "夜"
    return "深夜"


FEATURES = {
    "post_type": lambda r: r.get("post_type") or "affiliate",
    "genre_name": lambda r: r.get("genre_name") or "不明",
    "price_band": lambda r: price_band(r.get("price")),
    "hook_type": lambda r: r.get("hook_type") or "不明",
    "style": lambda r: r.get("style") or "不明",
    "has_image": lambda r: r.get("has_image") or "不明",
    "time_band": lambda r: time_band(r.get("post_hour")),
}


def summarize(rows, min_samples):
    def stats(group):
        n = len(group)
        views = sum(to_float(r.get("views")) for r in group)
        clicks = sum(to_float(r.get("clicks")) for r in group)
        sales = sum(to_float(r.get("sales")) for r in group)
        return {
            "posts": n,
            "enough_data": n >= min_samples,
            "views": views,
            "clicks": clicks,
            "sales": sales,
            "revenue": sum(to_float(r.get("revenue")) for r in group),
            "click_rate": round(clicks / views, 4) if views else None,
            "posts_with_sale": sum(1 for r in group if to_float(r.get("sales")) > 0),
        }

    by_feature = {}
    for name, key_fn in FEATURES.items():
        groups = defaultdict(list)
        for r in rows:
            groups[key_fn(r)].append(r)
        by_feature[name] = {k: stats(v) for k, v in sorted(groups.items())}

    def brief(r):
        return {
            "post_id": r["post_id"],
            "item_name": r["item_name"][:30],
            "hook_type": r.get("hook_type"),
            "style": r.get("style"),
            "views": r.get("views"),
            "clicks": r.get("clicks"),
            "sales": r.get("sales"),
            "text": r.get("text"),
        }

    with_sale = [r for r in rows if to_float(r.get("sales")) > 0]
    without_sale = sorted(
        (r for r in rows if to_float(r.get("sales")) <= 0),
        key=lambda r: to_float(r.get("clicks")),
        reverse=True,
    )
    return {
        "total": stats(rows),
        "by_feature": by_feature,
        "sold_posts": [brief(r) for r in with_sale],
        "unsold_posts": [brief(r) for r in without_sale[:20]],
    }


def main():
    config = load_config()
    rows = [r for r in read_log() if r.get("status") == "posted"]
    result = summarize(rows, config["analysis"]["min_samples_for_trend"])
    # 売れた/売れないの比較はアフィリエイト投稿だけで行う
    affiliate = [r for r in rows if (r.get("post_type") or "affiliate") == "affiliate"]
    compared = summarize(affiliate, config["analysis"]["min_samples_for_trend"])
    result["sold_posts"] = compared["sold_posts"]
    result["unsold_posts"] = compared["unsold_posts"]
    json.dump(result, sys.stdout, ensure_ascii=False, indent=2)
    print()


if __name__ == "__main__":
    main()
