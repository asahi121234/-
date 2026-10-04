"""スクリプトの最低限のテスト。実行: python3 -m unittest discover affiliate/tests"""

import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

import common  # noqa: E402
from check_post import check  # noqa: E402
from fetch_ranking import SAMPLE_PATH, normalize  # noqa: E402
from filter_items import reject_reason  # noqa: E402
from summarize_log import summarize  # noqa: E402

URL = "https://hb.afl.rakuten.co.jp/ichiba/SAMPLE/1"


class CheckPostTest(unittest.TestCase):
    def setUp(self):
        self.config = common.load_config()
        self.ng = common.load_ng_words()

    def test_ok(self):
        text = f"#PR\n洗面所の床がいつも濡れている人向け。\n価格2,480円（投稿時点）\n{URL}"
        self.assertTrue(check(text, URL, self.config, self.ng)["ok"])

    def test_missing_pr(self):
        result = check(f"おすすめです\n{URL}", URL, self.config, self.ng)
        self.assertIn("PR表記がない（#PR など）", result["errors"])

    def test_ng_word(self):
        result = check(f"#PR これで絶対痩せる\n{URL}", URL, self.config, self.ng)
        self.assertFalse(result["ok"])
        self.assertTrue(any("痩せる" in e for e in result["errors"]))

    def test_non_affiliate_url(self):
        result = check("#PR テスト", "https://example.com/", self.config, self.ng)
        self.assertIn("楽天のアフィリエイトURLではない", result["errors"])

    def test_too_long(self):
        result = check("#PR " + "あ" * 600, URL, self.config, self.ng)
        self.assertFalse(result["ok"])


class FilterTest(unittest.TestCase):
    def test_sample_filtering(self):
        raw = json.loads(SAMPLE_PATH.read_text(encoding="utf-8"))
        items = normalize(raw, {"id": "0", "name": "テスト"})
        rules = common.load_config()["filter"]
        reasons = {i["item_code"]: reject_reason(i, rules, set()) for i in items}
        self.assertIsNone(reasons["sample-shop:10000001"])
        self.assertIn("除外キーワード", reasons["sample-shop:10000002"])
        self.assertEqual(reasons["sample-shop:10000003"], "レビュー平均が基準未満")
        self.assertIsNone(reasons["sample-shop:10000004"])
        self.assertEqual(items[3]["image_url"], "https://thumbnail.image.rakuten.co.jp/sample4.jpg")

    def test_recently_posted(self):
        raw = json.loads(SAMPLE_PATH.read_text(encoding="utf-8"))
        item = normalize(raw, {"id": "0", "name": ""})[0]
        rules = common.load_config()["filter"]
        self.assertEqual(reject_reason(item, rules, {item["item_code"]}), "直近に投稿済み")


class LogAndSummaryTest(unittest.TestCase):
    def test_roundtrip_and_summary(self):
        with tempfile.TemporaryDirectory() as tmp:
            original = common.POSTS_LOG_PATH
            common.POSTS_LOG_PATH = Path(tmp) / "posts_log.csv"
            try:
                rows = [
                    {"post_id": "a", "status": "posted", "hook_type": "悩み提起", "price": "2480",
                     "views": "1000", "clicks": "20", "sales": "1", "item_name": "A"},
                    {"post_id": "b", "status": "posted", "hook_type": "数字", "price": "12000",
                     "views": "500", "clicks": "2", "sales": "0", "item_name": "B"},
                ]
                common.write_log(rows)
                read = common.read_log()
                self.assertEqual([r["post_id"] for r in read], ["a", "b"])
                result = summarize(read, min_samples=10)
                self.assertEqual(result["total"]["posts"], 2)
                self.assertFalse(result["total"]["enough_data"])
                self.assertEqual(result["by_feature"]["hook_type"]["悩み提起"]["click_rate"], 0.02)
                self.assertEqual(len(result["sold_posts"]), 1)
            finally:
                common.POSTS_LOG_PATH = original


if __name__ == "__main__":
    unittest.main()
