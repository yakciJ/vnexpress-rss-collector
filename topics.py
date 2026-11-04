"""Bộ chủ đề để gán nhãn bài viết.

Mỗi chủ đề gồm:
- examples: câu mô tả + tiêu đề mẫu. Embedding của bài được so với từng câu,
  lấy điểm cao nhất. Muốn chủ đề bắt bài tốt hơn thì thêm câu mẫu vào đây.
- keywords: cụm từ gặp trong tiêu đề hoặc sapo thì cộng điểm. So khớp không
  phân biệt hoa thường, theo nguyên cụm từ.
- publish: False nghĩa là chủ đề này không đăng lên app (dùng để hút các bài
  tin ngành, tin ngoài lề ra khỏi các chủ đề chính).

Đổi nội dung file này thì tăng LABEL_VERSION để script gán nhãn lại toàn bộ.
"""

LABEL_VERSION = "v1"

TOPICS = [
    {
        "key": "huyet_ap",
        "name": "Huyết áp",
        "publish": True,
        "examples": [
            "Huyết áp cao là gì, cách đo huyết áp đúng tại nhà và kiểm soát tăng huyết áp",
            "Chỉ số huyết áp bao nhiêu là bình thường?",
            "Cách đo huyết áp bằng máy đo điện tử tại nhà",
            "Thực phẩm giúp hạ huyết áp tự nhiên",
            "Huyết áp thấp gây chóng mặt phải làm sao",
            "Biến chứng của tăng huyết áp không điều trị",
        ],
        "keywords": ["huyết áp", "tăng huyết áp", "cao huyết áp", "hạ áp", "tiền tăng huyết áp"],
    },
    {
        "key": "tieu_duong",
        "name": "Đường huyết & tiểu đường",
        "publish": True,
        "examples": [
            "Bệnh tiểu đường, đái tháo đường và cách kiểm soát đường huyết",
            "Chỉ số đường huyết lúc đói bao nhiêu là cao?",
            "Dấu hiệu sớm của bệnh tiểu đường type 2",
            "Người bị tiểu đường nên ăn gì",
            "Tiền tiểu đường có chữa được không",
        ],
        "keywords": ["tiểu đường", "đái tháo đường", "đường huyết", "insulin", "hba1c", "tiền tiểu đường"],
    },
    {
        "key": "tim_mach",
        "name": "Tim mạch & đột quỵ",
        "publish": True,
        "examples": [
            "Bệnh tim mạch, đột quỵ, mỡ máu và cách phòng ngừa",
            "Dấu hiệu cảnh báo đột quỵ cần đi cấp cứu ngay",
            "Cholesterol cao ảnh hưởng tim thế nào",
            "Nhồi máu cơ tim ở người trẻ",
            "Thói quen tốt cho tim mạch",
        ],
        "keywords": ["tim mạch", "đột quỵ", "nhồi máu", "suy tim", "mỡ máu", "cholesterol", "xơ vữa", "huyết khối", "rối loạn nhịp tim"],
    },
    {
        "key": "than_tiet_nieu",
        "name": "Thận & tiết niệu",
        "publish": True,
        "examples": [
            "Bệnh thận, suy thận, sỏi thận và sức khỏe đường tiết niệu",
            "Thói quen giúp bảo vệ thận",
            "Dấu hiệu suy thận sớm",
            "Uống nước thế nào tốt cho thận",
        ],
        "keywords": ["thận", "suy thận", "sỏi thận", "tiết niệu", "niệu quản", "bàng quang"],
    },
    {
        "key": "tieu_hoa_gan",
        "name": "Tiêu hóa & gan",
        "publish": True,
        "examples": [
            "Bệnh dạ dày, đường ruột, gan mật và hệ tiêu hóa",
            "Cách hạ men gan, phòng gan nhiễm mỡ",
            "Đồ uống tốt cho đường ruột",
            "Trào ngược dạ dày nên kiêng gì",
        ],
        "keywords": ["gan", "men gan", "gan nhiễm mỡ", "dạ dày", "đường ruột", "tiêu hóa", "táo bón", "trào ngược", "sỏi mật", "đại tràng"],
    },
    {
        "key": "xuong_khop",
        "name": "Xương khớp",
        "publish": True,
        "examples": [
            "Bệnh xương khớp, loãng xương, đau lưng, thoát vị đĩa đệm, gout",
            "Đau cổ vai gáy khi ngủ dậy",
            "Cách phòng loãng xương ở phụ nữ",
            "Thoái hóa khớp gối ở người lớn tuổi",
        ],
        "keywords": ["xương khớp", "loãng xương", "mật độ xương", "thoát vị", "đau lưng", "cổ vai gáy", "gout", "gút", "thoái hóa khớp", "viêm khớp"],
    },
    {
        "key": "ho_hap_truyen_nhiem",
        "name": "Hô hấp & bệnh truyền nhiễm",
        "publish": True,
        "examples": [
            "Cúm, cảm lạnh, viêm phổi, hen và bệnh truyền nhiễm",
            "Cách chăm sóc khi bị cúm tại nhà",
            "Vaccine phòng bệnh cho người lớn",
            "Sốt xuất huyết và dấu hiệu nguy hiểm",
        ],
        "keywords": ["cúm", "viêm phổi", "hen suyễn", "ho kéo dài", "truyền nhiễm", "vaccine", "vắc xin", "sốt xuất huyết", "sốt mò", "hpv"],
    },
    {
        "key": "ung_thu",
        "name": "Ung thư & tầm soát",
        "publish": True,
        "examples": [
            "Ung thư, dấu hiệu sớm và tầm soát ung thư định kỳ",
            "Ai nên tầm soát ung thư",
            "Thói quen làm tăng nguy cơ ung thư",
        ],
        "keywords": ["ung thư", "tầm soát", "khối u", "u ác"],
    },
    {
        "key": "dinh_duong",
        "name": "Dinh dưỡng",
        "publish": True,
        "examples": [
            "Dinh dưỡng, ăn uống lành mạnh, thực phẩm tốt cho sức khỏe",
            "Ăn trái cây thế nào cho đúng",
            "Uống gì buổi sáng tốt cho sức khỏe",
            "Thực phẩm giàu vitamin và khoáng chất",
            "Chế độ ăn Địa Trung Hải",
        ],
        "keywords": ["dinh dưỡng", "thực phẩm", "chế độ ăn", "trái cây", "rau", "vitamin", "uống nước", "món ăn", "ăn sáng"],
    },
    {
        "key": "giam_can",
        "name": "Cân nặng & giảm cân",
        "publish": True,
        "examples": [
            "Giảm cân an toàn, giảm mỡ bụng, kiểm soát cân nặng và béo phì",
            "Thực đơn giảm cân khoa học",
            "Cách giữ eo thon, giảm mỡ bụng",
            "Ăn gì để giảm cân mà không đói",
        ],
        "keywords": ["giảm cân", "tăng cân", "béo phì", "mỡ bụng", "cân nặng", "giảm mỡ", "eo thon", "bmi", "ăn kiêng", "trọng lượng"],
    },
    {
        "key": "van_dong",
        "name": "Vận động & bài tập",
        "publish": True,
        "examples": [
            "Tập thể dục, bài tập dẻo dai, giãn cơ, yoga, đi bộ, chạy bộ",
            "Bài tập kéo giãn cơ mỗi sáng",
            "Đi bộ bao nhiêu bước mỗi ngày là đủ",
            "Bài tập tăng sức bền cho người mới",
            "Tập luyện thế nào để không chấn thương",
        ],
        "keywords": ["tập luyện", "bài tập", "thể dục", "đi bộ", "chạy bộ", "yoga", "giãn cơ", "kéo giãn", "dẻo dai", "gym", "vận động", "marathon", "squat", "plank"],
    },
    {
        "key": "giac_ngu_tinh_than",
        "name": "Giấc ngủ & tinh thần",
        "publish": True,
        "examples": [
            "Giấc ngủ, mất ngủ, căng thẳng, stress và sức khỏe tinh thần",
            "Cách ngủ ngon hơn mỗi đêm",
            "Áp lực công việc gây trầm cảm, lo âu",
        ],
        "keywords": ["giấc ngủ", "mất ngủ", "ngủ ngon", "stress", "căng thẳng", "trầm cảm", "lo âu", "áp lực", "tâm lý"],
    },
    {
        "key": "me_be",
        "name": "Mang thai, mẹ & bé",
        "publish": True,
        "examples": [
            "Mang thai, thai kỳ, sinh con, chăm sóc trẻ sơ sinh và trẻ nhỏ",
            "Mẹ bầu nên ăn gì",
            "Đái tháo đường thai kỳ",
            "Chăm sóc trẻ sinh non",
        ],
        "keywords": ["mang thai", "thai kỳ", "mẹ bầu", "sinh non", "trẻ sơ sinh", "sinh con", "cho con bú", "dậy thì"],
    },
    {
        "key": "sinh_san_gioi_tinh",
        "name": "Sức khỏe sinh sản & giới tính",
        "publish": True,
        "examples": [
            "Sức khỏe sinh sản nam nữ, kinh nguyệt, buồng trứng, tuyến tiền liệt, chuyện chăn gối",
            "Rối loạn kinh nguyệt ở phụ nữ",
            "Khám tiền hôn nhân",
        ],
        "keywords": ["kinh nguyệt", "buồng trứng", "tử cung", "vòi trứng", "tiền liệt tuyến", "tuyến tiền liệt", "xuất tinh", "mãn kinh", "hiếm muộn", "tiền hôn nhân"],
    },
    {
        "key": "mat_tai_mui_hong",
        "name": "Mắt, tai mũi họng & răng miệng",
        "publish": True,
        "examples": [
            "Bệnh về mắt, tai, mũi, họng, răng miệng",
            "Đau mắt, mỏi mắt khi dùng điện thoại",
            "Viêm xoang, viêm amidan ở trẻ",
            "Chăm sóc răng miệng đúng cách",
        ],
        "keywords": ["mắt", "hốc mắt", "thị lực", "tai", "màng nhĩ", "mũi", "xoang", "họng", "amidan", "răng", "nướu"],
    },
    {
        "key": "da_toc",
        "name": "Da, tóc & làm đẹp",
        "publish": True,
        "examples": [
            "Chăm sóc da, tóc, nếp nhăn, rụng tóc, mụn",
            "Vì sao tóc bạc sớm",
            "Cách giảm nếp nhăn tự nhiên",
        ],
        "keywords": ["tóc", "rụng tóc", "nếp nhăn", "làn da", "mụn", "chăm sóc da", "bớt sắc tố", "ngứa"],
    },
    {
        "key": "tin_nganh_y",
        "name": "Tin ngành y & chính sách",
        "publish": False,
        "examples": [
            "Tin ngành y tế, Bộ Y tế, chính sách bảo hiểm y tế, bệnh viện, phòng khám",
            "Bộ Y tế ban hành quy định mới",
            "Bệnh viện đạt chứng nhận chất lượng",
            "Thu hồi sản phẩm không đạt chuẩn",
            "Thứ trưởng Y tế phát biểu về dân số",
        ],
        "keywords": ["bộ y tế", "bảo hiểm y tế", "bhyt", "thứ trưởng", "bộ trưởng", "thu hồi", "tổng đài", "du lịch y tế", "đạt điểm chất lượng", "mức sinh"],
    },
    {
        "key": "ngoai_chu_de",
        "name": "Ngoài chủ đề sức khỏe",
        "publish": False,
        "examples": [
            "Tin thời sự, pháp luật, kinh tế, thể thao, giải trí, thế giới",
            "Tai nạn giao thông trên quốc lộ",
            "Giá vàng hôm nay",
            "Đội tuyển bóng đá thắng trận",
            "Vụ án lừa đảo bị khởi tố",
        ],
        "keywords": [],
    },
]

# Dạng bài, đoán từ tiêu đề: huong_dan (kiến thức, hợp đăng app nhất),
# cau_chuyen (ca bệnh, nhân vật), khac. Tin ngành đã có chủ đề tin_nganh_y lo.
# Thứ tự quan trọng: khớp mẫu đầu tiên thì dừng.
KIND_PATTERNS = [
    ("huong_dan", r"^(vì sao|tại sao|có nên|nên|cách|làm sao|làm gì|ai nên|khi nào|những cách|các cách)\b"
                  r"|\b(chỉ cách|là gì|là bệnh gì|có phải|có giúp|có gây|có hết|có sao|thế nào|bao nhiêu|ra sao|nên làm|nên ăn|nên uống)\b"
                  r"|\?$"
                  r"|^\d+\s+(cách|việc|thói quen|thực phẩm|loại|dấu hiệu|nguyên nhân|sai lầm|lợi ích|bài tập|món|trái cây|mẹo)"
                  r"|\b(thói quen|dấu hiệu|bài tập|mẹo|lợi ích|sai lầm)\b"),
    ("cau_chuyen", r"^(bé|cô gái|chàng trai|thanh niên|nữ sinh|nam sinh|cụ ông|cụ bà|bác sĩ (cứu|phẫu thuật|mổ)|hai tháng|phát hiện)\b"
                   r"|\b(người đàn ông|người phụ nữ|bệnh nhân|người bệnh|cô gái|bé trai|bé gái|ca bệnh|phẫu thuật|cấp cứu)\b"
                   r"|\b\d+ tuổi\b"),
]
DEFAULT_KIND = "khac"
