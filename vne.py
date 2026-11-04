"""Lấy dữ liệu từ VnExpress: RSS, danh sách Xem nhiều, số bình luận."""

import html
import re
import time
from datetime import timezone
from email.utils import parsedate_to_datetime

import feedparser
import requests

HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; RSSCollector/1.0)"}

RSS_FEEDS = {
    "suc-khoe": "https://vnexpress.net/rss/suc-khoe.rss",
}

# tin-xem-nhieu.rss bị đóng băng (toàn tin 2021) nên đọc trang HTML
MOST_READ_PAGES = {
    "ngay": "https://vnexpress.net/tin-xem-nhieu",
    "tuan": "https://vnexpress.net/tin-xem-nhieu/trong-tuan",
    "30-ngay": "https://vnexpress.net/tin-xem-nhieu/30-ngay",
}

COMMENT_API = "https://usi-saas.vnexpress.net/index/get"

_ARTICLE_LINK = re.compile(r'href="(https://vnexpress\.net/[^"#?]+-(\d{6,8})\.html)"')
_VNE_ID = re.compile(r"-(\d{6,8})\.html")


def vne_id_from_link(link):
    match = _VNE_ID.search(link or "")
    return int(match.group(1)) if match else None


def _published_at(entry):
    value = entry.get("published") or entry.get("updated")
    if not value:
        return None
    try:
        return parsedate_to_datetime(value).astimezone(timezone.utc).isoformat()
    except (TypeError, ValueError):
        return None


def _parse_description(description):
    """Mô tả RSS có dạng <a><img src></a></br>sapo."""
    description = description or ""
    image = re.search(r'<img[^>]+src="([^"]+)"', description)
    sapo = re.split(r"</br>|<br\s*/?>", description)[-1]
    sapo = html.unescape(re.sub(r"<[^>]+>", "", sapo)).strip()
    return sapo, (html.unescape(image.group(1)) if image else None)


def fetch_feed(name, url):
    response = requests.get(url, timeout=30, headers=HEADERS)
    response.raise_for_status()
    feed = feedparser.parse(response.content)
    if feed.bozo and not feed.entries:
        raise RuntimeError(f"RSS parsing failed: {url}")

    articles = []
    for entry in feed.entries:
        title = entry.get("title", "").strip()
        link = entry.get("link", "").strip()
        if not title or not link:
            continue
        sapo, thumbnail = _parse_description(entry.get("description"))
        articles.append({
            "title": title,
            "link": link,
            "published_at": _published_at(entry),
            "vne_id": vne_id_from_link(link),
            "sapo": sapo,
            "thumbnail": thumbnail,
            "source_feed": name,
        })
    return articles


def fetch_most_read():
    """Trả về {vne_id: hạng tốt nhất} trên các trang Xem nhiều (hạng 1 là cao nhất)."""
    ranks = {}
    for url in MOST_READ_PAGES.values():
        response = requests.get(url, timeout=30, headers=HEADERS)
        response.raise_for_status()
        seen = []
        for _, vne_id in _ARTICLE_LINK.findall(response.text):
            vne_id = int(vne_id)
            if vne_id not in seen:
                seen.append(vne_id)
        for rank, vne_id in enumerate(seen, start=1):
            ranks[vne_id] = min(rank, ranks.get(vne_id, rank))
    return ranks


def fetch_comment_stats(vne_id):
    """Số bình luận (gồm trả lời) và tổng lượt thích của 10 bình luận nhiều thích nhất.

    Trả về None khi bài tắt bình luận.
    """
    response = requests.get(
        COMMENT_API,
        timeout=15,
        headers=HEADERS,
        params={
            "offset": 0,
            "limit": 10,
            "frommobile": 0,
            "sort": "like",
            "is_onload": 1,
            "objectid": vne_id,
            "objecttype": 1,
            "siteid": 1000000,
        },
    )
    response.raise_for_status()
    payload = response.json()
    if payload.get("error") or not payload.get("iscomment"):
        return None
    data = payload.get("data") or {}
    items = data.get("items") or []
    return {
        "comment_count": int(data.get("totalitem") or 0),
        "top_comment_likes": sum(int(item.get("userlike") or 0) for item in items),
    }


def polite_sleep():
    time.sleep(0.3)
