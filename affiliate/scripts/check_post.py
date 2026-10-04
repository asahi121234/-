"""投稿文を機械的にチェックする（審査担当が最初に必ず実行する）。

使い方:
  python3 affiliate/scripts/check_post.py --text "投稿文" --url "https://hb.afl.rakuten.co.jp/..."
  python3 affiliate/scripts/check_post.py --file draft.json   # {"text": ..., "affiliate_url": ..., "post_type": ...}
  python3 affiliate/scripts/check_post.py --type normal --text "普通の投稿文"

post_type は affiliate（既定）か normal。normal はリンクなし・PR表記不要で、
URLや楽天のリンクが入っていないことを確認する。

結果はJSONで出力し、不合格なら終了コード1を返す。
"""

import argparse
import json
import sys

from common import load_config, load_ng_words


def check(text, url, config, ng_words, post_type="affiliate"):
    rules = config["post"]
    errors, warnings = [], []

    full = text if url in text else f"{text}\n{url}"
    if len(full) > rules["max_chars"]:
        errors.append(f"文字数オーバー：{len(full)}文字（上限{rules['max_chars']}）")

    if post_type == "normal":
        if url or "http://" in text or "https://" in text:
            errors.append("普通の投稿にリンクが入っている")
        if any(marker in text for marker in rules["pr_markers"]):
            warnings.append("普通の投稿にPR表記がある（商品紹介ならアフィリエイト投稿として扱う）")
    elif not any(marker in text for marker in rules["pr_markers"]):
        errors.append("PR表記がない（#PR など）")

    if post_type == "normal":
        pass
    elif not url:
        errors.append("アフィリエイトURLがない")
    elif not any(url.startswith(p) for p in rules["affiliate_url_prefixes"]):
        errors.append("楽天のアフィリエイトURLではない")

    lowered = text.lower()
    for word in ng_words:
        if word.lower() in lowered:
            errors.append(f"NGワード「{word}」")

    hashtags = [w for w in text.split() if w.startswith("#")]
    if len(hashtags) > 2:
        warnings.append(f"ハッシュタグが{len(hashtags)}個（推奨2個まで）")
    if ("円" in text or "¥" in text) and "時点" not in text:
        warnings.append("価格に「投稿時点」の注記がない")

    return {"ok": not errors, "char_count": len(full), "errors": errors, "warnings": warnings}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--text")
    parser.add_argument("--url", default="")
    parser.add_argument("--file")
    parser.add_argument("--type", choices=["affiliate", "normal"])
    args = parser.parse_args()

    if args.file:
        with open(args.file, encoding="utf-8") as f:
            draft = json.load(f)
        text, url = draft["text"], draft.get("affiliate_url", "")
        post_type = args.type or draft.get("post_type") or "affiliate"
    elif args.text is not None:
        text, url = args.text, args.url
        post_type = args.type or "affiliate"
    else:
        sys.exit("--text か --file を指定してください。")

    result = check(text, url, load_config(), load_ng_words(), post_type)
    json.dump(result, sys.stdout, ensure_ascii=False, indent=2)
    print()
    sys.exit(0 if result["ok"] else 1)


if __name__ == "__main__":
    main()
