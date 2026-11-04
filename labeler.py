"""Gán chủ đề cho bài viết bằng embedding chạy trên máy (không gọi API).

Điểm của một chủ đề = cosine cao nhất giữa bài và các câu mẫu của chủ đề
+ KEYWORD_BONUS cho mỗi từ khoá khớp (tối đa MAX_KEYWORD_HITS từ).
"""

import os
import re
import unicodedata

import numpy as np
from fastembed import TextEmbedding
from fastembed.common.model_description import ModelSource, PoolingType

from topics import DEFAULT_KIND, KIND_PATTERNS, TOPICS

MODEL_NAME = "intfloat/multilingual-e5-small"

KEYWORD_BONUS = 0.03
MAX_KEYWORD_HITS = 2
# Chủ đề phụ phải có từ khoá khớp và điểm cách chủ đề chính không quá SECONDARY_MARGIN
SECONDARY_MARGIN = 0.03
MAX_TOPICS = 3
# Điểm chủ đề chính dưới mức này thì đánh dấu cần người xem
LOW_CONFIDENCE = 0.87

_model = None
_topic_vectors = None


def _normalize(text):
    return unicodedata.normalize("NFC", text or "").lower()


def _get_model():
    global _model
    if _model is None:
        # fastembed không có sẵn e5-small nên khai báo bản ONNX trên Hugging Face
        TextEmbedding.add_custom_model(
            model=MODEL_NAME,
            pooling=PoolingType.MEAN,
            normalization=True,
            sources=ModelSource(hf=MODEL_NAME),
            dim=384,
            model_file="onnx/model.onnx",
        )
        # FASTEMBED_CACHE_PATH do workflow đặt để actions/cache giữ model giữa các lần chạy
        _model = TextEmbedding(MODEL_NAME, cache_dir=os.environ.get("FASTEMBED_CACHE_PATH"))
    return _model


def _embed(texts):
    # e5 dùng tiền tố "query: " cho cả hai phía khi phân loại (không phải truy vấn tài liệu)
    vectors = _get_model().embed(["query: " + t for t in texts])
    return np.array(list(vectors))


def _get_topic_vectors():
    global _topic_vectors
    if _topic_vectors is None:
        _topic_vectors = [_embed(topic["examples"]) for topic in TOPICS]
    return _topic_vectors


_keyword_patterns = [
    [re.compile(rf"(?<!\w){re.escape(_normalize(k))}(?!\w)") for k in topic["keywords"]]
    for topic in TOPICS
]
_kind_patterns = [(kind, re.compile(pattern)) for kind, pattern in KIND_PATTERNS]


def guess_kind(title):
    title = _normalize(title).strip()
    for kind, pattern in _kind_patterns:
        if pattern.search(title):
            return kind
    return DEFAULT_KIND


def label(items):
    """items: list of dict có title, sapo. Trả về list dict nhãn cùng thứ tự."""
    if not items:
        return []

    texts = [f"{item['title']}. {item.get('sapo') or ''}".strip() for item in items]
    article_vectors = _embed(texts)
    topic_vectors = _get_topic_vectors()

    results = []
    for text, item, vector in zip(texts, items, article_vectors):
        normalized = _normalize(text)
        scores, hits = {}, {}
        for topic, examples, patterns in zip(TOPICS, topic_vectors, _keyword_patterns):
            cosine = float(np.max(examples @ vector))
            hits[topic["key"]] = sum(1 for p in patterns if p.search(normalized))
            scores[topic["key"]] = cosine + KEYWORD_BONUS * min(hits[topic["key"]], MAX_KEYWORD_HITS)

        ranked = sorted(scores.items(), key=lambda kv: kv[1], reverse=True)
        top_key, top_score = ranked[0]
        chosen = [top_key] + [
            k for k, s in ranked[1:MAX_TOPICS]
            if s >= top_score - SECONDARY_MARGIN and hits[k] > 0
        ]
        # Chủ đề không đăng chỉ giữ khi nó đứng đầu, không làm chủ đề phụ
        publishable = {t["key"] for t in TOPICS if t["publish"]}
        if top_key in publishable:
            chosen = [k for k in chosen if k in publishable]
        else:
            chosen = [top_key]

        results.append({
            "topics": chosen,
            "topic_score": round(top_score, 4),
            "topic_scores": {k: round(s, 4) for k, s in ranked[:5]},
            "kind": guess_kind(item["title"]),
            "needs_review": top_score < LOW_CONFIDENCE,
            "publishable": top_key in publishable,
        })
    return results
