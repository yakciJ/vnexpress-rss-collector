-- Hoàn tác 001_topics_engagement.sql. Bảng articles và dữ liệu cũ (title, link, published_at) giữ nguyên.

drop view if exists hot_articles;
drop view if exists article_ranking;
drop table if exists article_metrics;
drop table if exists topics;

drop index if exists articles_vne_id_key;
drop index if exists articles_published_at_idx;
drop index if exists articles_topics_idx;

alter table articles
  drop column if exists vne_id,
  drop column if exists sapo,
  drop column if exists thumbnail,
  drop column if exists source_feed,
  drop column if exists topics,
  drop column if exists topic_score,
  drop column if exists topic_scores,
  drop column if exists kind,
  drop column if exists publishable,
  drop column if exists needs_review,
  drop column if exists label_version,
  drop column if exists labeled_at,
  drop column if exists comment_count,
  drop column if exists top_comment_likes,
  drop column if exists metrics_updated_at,
  drop column if exists most_read_rank,
  drop column if exists most_read_at;
