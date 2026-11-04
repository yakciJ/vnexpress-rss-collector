# vnexpress-rss-collector

Lấy bài mục Sức khỏe của VnExpress, đo mức tương tác, gán chủ đề y tế để chọn bài đăng lên app. Chạy miễn phí: GitHub Actions + Supabase, model embedding chạy trên runner, không gọi API AI.

## Mỗi lần chạy (30 phút một lần)

1. **collect**: đọc RSS `suc-khoe`, lưu bài mới (tiêu đề, sapo, ảnh, ngày đăng). Đọc 3 trang Xem nhiều (ngày, tuần, 30 ngày), bài nào của mình có tên trong đó thì ghi hạng.
2. **metrics**: với bài đăng trong 3 ngày gần nhất, lấy số bình luận và lượt thích bình luận. Số đổi thì ghi một dòng vào `article_metrics`.
3. **label**: bài chưa có nhãn được gán 1–3 chủ đề (`topics`) và dạng bài (`kind`). Chỉ nạp model khi có bài mới.

VnExpress không công bố lượt xem, nên tương tác = số bình luận + lượt thích bình luận + có mặt trong Xem nhiều.

## Cài đặt lần đầu

1. Supabase > SQL Editor: chạy phần **KIỂM TRA TRƯỚC** ở đầu `sql/001_topics_engagement.sql`, rồi chạy cả file. Hoàn tác: `sql/001_rollback.sql`.
2. Secrets `SUPABASE_URL`, `SUPABASE_SERVICE_ROLE_KEY` đã có từ bản cũ, không cần thêm.
3. Actions > VNExpress RSS Collector > Run workflow để chạy thử. Lần đầu mất thêm khoảng 30 giây để tải model, các lần sau lấy từ cache.

## Lấy bài

```sql
-- bài tương tác cao (top 20% trong 30 ngày), đăng được lên app
select title, link, topics, kind, comment_count, most_read_rank from hot_articles;

-- theo chủ đề
select * from hot_articles where 'huyet_ap' = any(topics);

-- chỉ bài kiến thức / hướng dẫn, đã đủ 2 ngày để số bình luận ổn định
select * from hot_articles where kind = 'huong_dan' and is_mature;

-- bài máy không chắc, cần người xem lại nhãn
select title, topics, topic_scores from article_ranking where needs_review;
```

Mã chủ đề và tên hiển thị nằm ở bảng `topics` (đồng bộ từ `topics.py`).

## Chủ đề

Huyết áp · Đường huyết & tiểu đường · Tim mạch & đột quỵ · Thận & tiết niệu · Tiêu hóa & gan · Xương khớp · Hô hấp & bệnh truyền nhiễm · Ung thư & tầm soát · Dinh dưỡng · Cân nặng & giảm cân · Vận động & bài tập · Giấc ngủ & tinh thần · Mang thai, mẹ & bé · Sức khỏe sinh sản & giới tính · Mắt, tai mũi họng & răng miệng · Da, tóc & làm đẹp.

Hai chủ đề không đăng (`publish: False`): Tin ngành y & chính sách, Ngoài chủ đề sức khỏe.

Dạng bài: `huong_dan` (kiến thức, hỏi đáp, mẹo), `cau_chuyen` (ca bệnh, nhân vật), `khac`.

## Chỉnh khi gán sai

- Thêm câu mẫu (`examples`) hoặc từ khoá (`keywords`) cho chủ đề trong `topics.py`, rồi tăng `LABEL_VERSION` để gán lại toàn bộ.
- Ngưỡng ở đầu `labeler.py`: `LOW_CONFIDENCE` (dưới mức này thì `needs_review`), `SECONDARY_MARGIN` (độ gần để thêm chủ đề phụ).
- Công thức điểm tương tác và ngưỡng top 20% nằm trong view ở file SQL.

Thử trên 60 bài ngày 03/11/2026: khoảng 55 bài đúng chủ đề chính. Bài sai đa số có điểm thấp và đã bị đánh dấu `needs_review`.

## Giới hạn

- RSS chỉ giữ khoảng 60 bài (2–3 ngày), nên workflow phải chạy đều. Repo public thì phút Actions không giới hạn.
- `tin-xem-nhieu.rss` của VnExpress bị đóng băng ở tin năm 2021, nên script đọc trang HTML thay vào.
- API bình luận (`usi-saas.vnexpress.net`) là API nội bộ của trang, có thể đổi bất cứ lúc nào.
- Nội dung bài thuộc bản quyền VnExpress. Dùng danh sách này để biên tập viên chọn đề tài, viết lại hoặc dẫn link, đừng chép nguyên bài vào app.

## Bước sau (chưa làm)

- Thêm nguồn khác (báo khác, YouTube): thêm vào `RSS_FEEDS` hoặc viết hàm lấy riêng trong `vne.py`.
- Bài `needs_review` gửi cho LLM rẻ phân loại lại (bậc 2), tốn rất ít vì chỉ là phần nhỏ.
