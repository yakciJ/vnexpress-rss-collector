
import os
import requests
import feedparser
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from supabase import create_client

# RSS nguồn tin
RSS_URL = "https://vnexpress.net/rss/suc-khoe.rss"

# Kết nối Supabase
supabase = create_client(
    os.environ["SUPABASE_URL"],
    os.environ["SUPABASE_SERVICE_ROLE_KEY"]
)


def get_published_date(entry):
    """Chuyển ngày xuất bản RSS thành ISO 8601."""
    date_string = entry.get("published") or entry.get("updated")

    if not date_string:
        return None

    try:
        return parsedate_to_datetime(date_string).astimezone(
            timezone.utc
        ).isoformat()
    except (TypeError, ValueError):
        return None


def collect_articles():
    print("Fetching RSS...")

    response = requests.get(
        RSS_URL,
        timeout=30,
        headers={"User-Agent": "RSSCollector/1.0"}
    )
    response.raise_for_status()

    feed = feedparser.parse(response.content)

    if feed.bozo and not feed.entries:
        raise RuntimeError("RSS parsing failed")

    articles = []

    for entry in feed.entries:
        title = entry.get("title", "").strip()
        link = entry.get("link", "").strip()

        if not title or not link:
            continue

        articles.append({
            "title": title,
            "link": link,
            "published_at": get_published_date(entry)
        })

    if not articles:
        print("No articles found.")
        return

    print(f"Found {len(articles)} articles.")

    # Lưu vào Supabase, bỏ qua link đã tồn tại
    result = (
        supabase.table("articles")
        .upsert(
            articles,
            on_conflict="link",
            ignore_duplicates=True
        )
        .execute()
    )

    print(f"Saved {len(result.data)} new articles.")


if __name__ == "__main__":
    collect_articles()
