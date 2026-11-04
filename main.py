"""Mỗi lần chạy: lấy bài mới → cập nhật số tương tác → gán chủ đề cho bài chưa có nhãn.

Chạy riêng một bước: python main.py collect | metrics | label
"""

import os
import sys
from datetime import datetime, timedelta, timezone

from supabase import create_client

import vne
from topics import LABEL_VERSION, TOPICS

# Bình luận VnExpress dồn vào 1-2 ngày đầu, theo dõi 3 ngày là đủ
METRICS_WINDOW_DAYS = 3
LABEL_BATCH = 500

# Kết nối Supabase
supabase = create_client(
    os.environ["SUPABASE_URL"],
    os.environ["SUPABASE_SERVICE_ROLE_KEY"]
)


def _now():
    return datetime.now(timezone.utc).isoformat()


def collect_articles():
    articles = []
    for name, url in vne.RSS_FEEDS.items():
        print(f"Fetching RSS {name}...")
        articles += vne.fetch_feed(name, url)

    if not articles:
        print("No articles found.")
        return

    # Không bỏ qua bài đã có: lần upsert này điền sapo/ảnh cho bài lưu từ bản script cũ.
    # Chỉ ghi các cột lấy từ RSS nên không đè nhãn và số tương tác.
    supabase.table("articles").upsert(articles, on_conflict="link").execute()
    print(f"Upserted {len(articles)} articles.")

    ranks = vne.fetch_most_read()
    if not ranks:
        return
    # Chỉ đánh dấu bài đã có trong bảng; trang Xem nhiều lẫn mọi chuyên mục
    rows = (
        supabase.table("articles")
        .select("vne_id, most_read_rank")
        .in_("vne_id", list(ranks))
        .execute()
        .data
    )
    for row in rows:
        rank = ranks[row["vne_id"]]
        best = min(rank, row["most_read_rank"] or rank)
        supabase.table("articles").update(
            {"most_read_rank": best, "most_read_at": _now()}
        ).eq("vne_id", row["vne_id"]).execute()
    print(f"Most-read: {len(rows)} of our articles are listed.")


def refresh_metrics():
    since = (datetime.now(timezone.utc) - timedelta(days=METRICS_WINDOW_DAYS)).isoformat()
    rows = (
        supabase.table("articles")
        .select("vne_id, comment_count, top_comment_likes")
        .gte("published_at", since)
        .not_.is_("vne_id", "null")
        .execute()
        .data
    )
    print(f"Refreshing metrics for {len(rows)} articles...")

    changed = 0
    for row in rows:
        try:
            stats = vne.fetch_comment_stats(row["vne_id"])
        except Exception as error:  # một bài lỗi không làm hỏng cả lượt
            print(f"  {row['vne_id']}: {error}")
            continue
        finally:
            vne.polite_sleep()

        # Bài tắt bình luận tính là 0
        stats = stats or {"comment_count": 0, "top_comment_likes": 0}
        supabase.table("articles").update(
            {**stats, "metrics_updated_at": _now()}
        ).eq("vne_id", row["vne_id"]).execute()

        if (stats["comment_count"], stats["top_comment_likes"]) != (
            row["comment_count"], row["top_comment_likes"]
        ):
            supabase.table("article_metrics").insert(
                {"vne_id": row["vne_id"], **stats}
            ).execute()
            changed += 1
    print(f"Metrics changed for {changed} articles.")


def sync_topics():
    supabase.table("topics").upsert([
        {"key": t["key"], "name": t["name"], "publish": t["publish"], "sort": i}
        for i, t in enumerate(TOPICS)
    ], on_conflict="key").execute()


def label_articles():
    rows = (
        supabase.table("articles")
        .select("link, title, sapo")
        .or_(f"label_version.is.null,label_version.neq.{LABEL_VERSION}")
        .limit(LABEL_BATCH)
        .execute()
        .data
    )
    if not rows:
        print("Nothing to label.")
        return

    # Nạp model chỉ khi có bài cần gán
    import labeler

    sync_topics()
    print(f"Labeling {len(rows)} articles...")
    for row, result in zip(rows, labeler.label(rows)):
        supabase.table("articles").update({
            **result,
            "label_version": LABEL_VERSION,
            "labeled_at": _now(),
        }).eq("link", row["link"]).execute()
    print("Labeled.")


STEPS = {
    "collect": collect_articles,
    "metrics": refresh_metrics,
    "label": label_articles,
}

if __name__ == "__main__":
    for step in sys.argv[1:] or STEPS:
        STEPS[step]()
