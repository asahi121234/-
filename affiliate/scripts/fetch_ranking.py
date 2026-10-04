"""楽天商品ランキングAPIから候補商品を取得し、扱いやすいJSONにして標準出力へ出す。

使い方:
  python3 affiliate/scripts/fetch_ranking.py --genre 215783 > /tmp/ranking.json
  python3 affiliate/scripts/fetch_ranking.py --all-genres > /tmp/ranking.json
  python3 affiliate/scripts/fetch_ranking.py --sample          # APIキーなしで動作確認

必要な環境変数:
  RAKUTEN_APP_ID        楽天ウェブサービスのアプリID
  RAKUTEN_AFFILIATE_ID  楽天アフィリエイトID（これがないと affiliateUrl が返らない）
任意:
  RAKUTEN_ACCESS_KEY    楽天側でアクセスキーが必要な場合に送る
  RAKUTEN_RANKING_URL   エンドポイントを変える場合（楽天の仕様変更に備えて）
"""

import argparse
import json
import os
import sys
import urllib.parse
import urllib.request
from datetime import datetime, timezone

from common import ROOT, load_config

DEFAULT_URL = "https://app.rakuten.co.jp/services/api/IchibaItem/Ranking/20220601"
SAMPLE_PATH = ROOT / "tests" / "sample_ranking.json"


def call_api(genre_id):
    app_id = os.environ.get("RAKUTEN_APP_ID")
    affiliate_id = os.environ.get("RAKUTEN_AFFILIATE_ID")
    if not app_id or not affiliate_id:
        sys.exit("RAKUTEN_APP_ID と RAKUTEN_AFFILIATE_ID を環境変数に設定してください。")

    params = {
        "applicationId": app_id,
        "affiliateId": affiliate_id,
        "genreId": genre_id,
        "format": "json",
        "formatVersion": "2",
    }
    access_key = os.environ.get("RAKUTEN_ACCESS_KEY")
    if access_key:
        params["accessKey"] = access_key

    url = os.environ.get("RAKUTEN_RANKING_URL", DEFAULT_URL) + "?" + urllib.parse.urlencode(params)
    with urllib.request.urlopen(url, timeout=20) as res:
        return json.load(res)


def normalize(raw, genre):
    """formatVersion 1/2 のどちらの形でも、必要な項目だけの一覧にする。"""
    items = []
    for entry in raw.get("Items", []):
        item = entry.get("Item", entry)
        images = item.get("mediumImageUrls") or []
        image = images[0] if images else ""
        if isinstance(image, dict):
            image = image.get("imageUrl", "")
        items.append(
            {
                "item_code": item.get("itemCode", ""),
                "item_name": item.get("itemName", ""),
                "catchcopy": item.get("catchcopy", ""),
                "price": item.get("itemPrice", 0),
                "review_average": item.get("reviewAverage", 0),
                "review_count": item.get("reviewCount", 0),
                "rank": item.get("rank", 0),
                "shop_name": item.get("shopName", ""),
                "item_url": item.get("itemUrl", ""),
                "affiliate_url": item.get("affiliateUrl", ""),
                "image_url": image,
                "availability": item.get("availability", 1),
                "genre_id": genre["id"],
                "genre_name": genre["name"],
            }
        )
    return items


def main():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--genre", help="ジャンルID")
    group.add_argument("--all-genres", action="store_true", help="config.json の全ジャンル")
    group.add_argument("--sample", action="store_true", help="サンプルデータで動作確認")
    args = parser.parse_args()

    config = load_config()
    limit = config.get("candidates_per_genre", 30)

    if args.sample:
        raw = json.loads(SAMPLE_PATH.read_text(encoding="utf-8"))
        genre = config["genres"][0]
        items = normalize(raw, genre)
    else:
        if args.all_genres:
            genres = config["genres"]
        else:
            genres = [g for g in config["genres"] if g["id"] == args.genre] or [
                {"id": args.genre, "name": ""}
            ]
        items = []
        for genre in genres:
            items.extend(normalize(call_api(genre["id"]), genre)[:limit])

    output = {
        "fetched_at": datetime.now(timezone.utc).isoformat(),
        "source": "sample" if args.sample else "rakuten_ranking_api",
        "items": items,
    }
    json.dump(output, sys.stdout, ensure_ascii=False, indent=2)
    print()


if __name__ == "__main__":
    main()
