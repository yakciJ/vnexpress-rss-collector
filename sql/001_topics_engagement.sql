-- Thêm chủ đề + số tương tác cho bảng articles.
-- Chạy trong Supabase > SQL Editor. Chạy lại nhiều lần vẫn an toàn.
--
-- KIỂM TRA TRƯỚC (chạy riêng, xem kết quả rồi mới chạy phần dưới):
--   select count(*) as tong, count(distinct link) as link_khac_nhau from articles;
--   -- hai số phải bằng nhau (script cũ upsert theo link nên link phải unique)
--   select substring(link from '-(\d{6,8})\.html') as vne_id, count(*)
--   from articles group by 1 having count(*) > 1;
--   -- phải trả về 0 dòng, nếu không thì index unique vne_id bên dưới sẽ lỗi

alter table articles
  add column if not exists vne_id bigint,
  add column if not exists sapo text,
  add column if not exists thumbnail text,
  add column if not exists source_feed text,
  -- nhãn
  add column if not exists topics text[],
  add column if not exists topic_score real,
  add column if not exists topic_scores jsonb,
  add column if not exists kind text,
  add column if not exists publishable boolean,
  add column if not exists needs_review boolean,
  add column if not exists label_version text,
  add column if not exists labeled_at timestamptz,
  -- tương tác (giá trị mới nhất, lịch sử ở article_metrics)
  add column if not exists comment_count int,
  add column if not exists top_comment_likes int,
  add column if not exists metrics_updated_at timestamptz,
  add column if not exists most_read_rank int,
  add column if not exists most_read_at timestamptz;

update articles
set vne_id = substring(link from '-(\d{6,8})\.html')::bigint
where vne_id is null;

create unique index if not exists articles_vne_id_key on articles (vne_id);
create index if not exists articles_published_at_idx on articles (published_at desc);
create index if not exists articles_topics_idx on articles using gin (topics);

-- Lịch sử số tương tác, chỉ ghi khi số thay đổi
create table if not exists article_metrics (
  vne_id bigint not null,
  captured_at timestamptz not null default now(),
  comment_count int not null,
  top_comment_likes int not null,
  primary key (vne_id, captured_at)
);

-- Tên hiển thị của chủ đề, script tự đồng bộ từ topics.py
create table if not exists topics (
  key text primary key,
  name text not null,
  publish boolean not null,
  sort int not null
);

-- Chỉ service role (GitHub Actions) đọc/ghi. Muốn app đọc bằng anon key thì thêm policy select.
alter table article_metrics enable row level security;
alter table topics enable row level security;

-- Điểm tương tác: log để vài bài nghìn bình luận không lấn át hết.
-- percent_rank so với bài đăng trong 30 ngày gần nhất.
create or replace view article_ranking with (security_invoker = on) as
with scored as (
  select
    a.vne_id, a.title, a.link, a.sapo, a.thumbnail, a.published_at,
    a.topics, a.kind, a.publishable, a.needs_review, a.topic_score,
    coalesce(a.comment_count, 0) as comment_count,
    coalesce(a.top_comment_likes, 0) as top_comment_likes,
    a.most_read_rank,
    round(extract(epoch from now() - a.published_at) / 3600) as age_hours,
    ln(1 + coalesce(a.comment_count, 0))
      + 0.3 * ln(1 + coalesce(a.top_comment_likes, 0))
      + case when a.most_read_rank is not null then 1.5 else 0 end as engagement_score
  from articles a
  where a.published_at > now() - interval '30 days'
)
select
  *,
  round(percent_rank() over (order by engagement_score)::numeric, 3) as engagement_pct,
  -- bình luận VnExpress dồn vào 1-2 ngày đầu; bài trẻ hơn thì điểm còn tăng
  age_hours >= 48 as is_mature
from scored;

-- Bài tương tác cao, đăng được lên app. Lọc theo chủ đề:
--   select * from hot_articles where 'huyet_ap' = any(topics);
create or replace view hot_articles with (security_invoker = on) as
select *
from article_ranking
where publishable
  and engagement_pct >= 0.8
order by engagement_score desc;

-- KIỂM TRA SAU:
--   select count(*) filter (where vne_id is null) as thieu_vne_id from articles;  -- nên là 0
--   select * from article_ranking order by engagement_score desc limit 10;
