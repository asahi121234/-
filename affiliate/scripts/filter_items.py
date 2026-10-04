"""機械的に判断できる条件で候補を絞り込む（AIに判断させない部分）。

使い方:
  python3 affiliate/scripts/filter_items.py /tmp/ranking.json > /tmp/filtered.json

落とす条件（config.json の filter）:
  レビュー平均・件数が基準未満 / 価格が範囲外 / 除外キーワードを含む /
  在庫なし / affiliateUrl がない / 直近N日に投稿済み
"""

import json
import sys
from datetime import datetime, timedelta, timezone

from common import load_config, read_log, to_float


def recently_posted_codes(days):
    cutoff = datetime.now(timezone.utc) - timedelta(days=days)
    codes = set()
    for row in read_log():
        if row.get("status") == "skipped":
            continue
        try:
            created = datetime.fromisoformat(row.get("created_at", ""))
        except ValueError:
            continue
        if created.tzinfo is None:
            created = created.replace(tzinfo=timezone.utc)
        if created >= cutoff:
            codes.add(row.get("item_code"))
    return codes


def reject_reason(item, rules, recent):
    text = item["item_name"] + " " + item.get("catchcopy", "")
    if not item.get("affiliate_url"):
        return "affiliateUrlなし"
    if str(item.get("availability", 1)) == "0":
        return "在庫なし"
    if to_float(item["review_average"]) < rules["min_review_average"]:
        return "レビュー平均が基準未満"
    if to_float(item["review_count"]) < rules["min_review_count"]:
        return "レビュー件数が基準未満"
    price = to_float(item["price"])
    if price < rules["min_price"] or price > rules["max_price"]:
        return "価格が範囲外"
    for word in rules["exclude_keywords"]:
        if word in text:
            return f"除外キーワード「{word}」"
    if item["item_code"] in recent:
        return "直近に投稿済み"
    return None


def main():
    if len(sys.argv) != 2:
        sys.exit("使い方: filter_items.py <fetch_ranking.py の出力JSON>")
    with open(sys.argv[1], encoding="utf-8") as f:
        data = json.load(f)

    rules = load_config()["filter"]
    recent = recently_posted_codes(rules["skip_recently_posted_days"])

    passed, rejected = [], []
    for item in data["items"]:
        reason = reject_reason(item, rules, recent)
        if reason:
            rejected.append({"item_code": item["item_code"], "item_name": item["item_name"][:40], "reason": reason})
        else:
            passed.append(item)

    json.dump(
        {"fetched_at": data.get("fetched_at"), "passed": passed, "rejected": rejected},
        sys.stdout,
        ensure_ascii=False,
        indent=2,
    )
    print()


if __name__ == "__main__":
    main()
