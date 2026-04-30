# N6 — Activity Ranking

Module xếp hạng hoạt động du lịch. Nhận danh sách hoạt động (do N5 sinh ra) và trả về top_k hoạt động phù hợp nhất với sở thích + ràng buộc + ngữ cảnh của người dùng.

---

## 1. Vai trò trong pipeline

```
N1 (embed) → N2 (image) → N3 (db) → N4 (rank locations)
                                          ↓
                                    N5 (gen activities)
                                          ↓
                                    N6 (rank activities)  ← module này
```

N6 **không** sinh hoạt động mới, **không** tạo embedding. Chỉ chấm điểm và sắp xếp các hoạt động đã có sẵn.

---

## 2. Công thức chấm điểm

Mỗi hoạt động nhận 1 điểm tổng trong khoảng `[0, 1]`, tính từ 3 nhóm điểm con:

```
Điểm tổng = 0.50 × Điểm khớp sở thích
          + 0.25 × Điểm phù hợp ràng buộc
          + 0.25 × Điểm phù hợp ngữ cảnh
```

| Nhóm điểm | Tín hiệu sử dụng | Phương pháp |
|---|---|---|
| **Sở thích** | vector `tag`, `context`, `emotion` của user ↔ vector `tag`, `text`, `intent` của hoạt động | Cosine similarity có trọng số |
| **Ràng buộc** | `price_level`, `estimated_duration` của hoạt động | So sánh với ngân sách + thời gian rảnh của user |
| **Ngữ cảnh** | `time_of_day_suitable`, `indoor_outdoor`, `weather_dependent` | Khớp với giờ trong ngày + thời tiết |

Trước khi chấm điểm, mọi hoạt động dài hơn thời gian rảnh của user sẽ bị **lọc cứng** (loại khỏi danh sách).

---

## 3. Input

```python
{
    "user_vectors": {
        "tag":     list[float] | None,   # vector sở thích từ tags
        "context": list[float] | None,   # vector ngữ cảnh từ text
        "emotion": list[float] | None,   # vector cảm xúc
        # "image" — reserved, hiện chưa dùng
    },

    "context": {
        "time_of_day": str | None,       # "morning" / "afternoon" / "night"
        # user_location — reserved
    },

    "activities": [                       # do N5 sinh ra
        {
            "activity_id": str,
            "location_id": str,
            "metadata": {
                "name": str,
                "price_level": float,            # [1.0, 5.0] — 1 rẻ, 5 đắt
                "estimated_duration": float,     # giờ
                "time_of_day_suitable": str,     # "morning" / "afternoon" / "night" / "anytime"
                "indoor_outdoor": str,           # "indoor" / "outdoor" / "mixed"
                "weather_dependent": bool,
                # ... các field khác (intensity, social_level, ...) — reserved
            },
            "vectors": {
                "text":   list[float] | None,
                "tag":    list[float] | None,
                "intent": list[float] | None,
            }
        }
    ],

    "constraints": {
        "duration": float | None,        # giờ rảnh — dùng cho lọc cứng + chấm điểm
        "weather":  str   | None,        # "sunny" / "rain" / "storm" / "snow" / ...
        # budget, people — reserved
    },

    "top_k": int                         # số hoạt động trả về
}
```

---

## 4. Output

```python
{
    "activities": [
        {
            "activity_id": str,
            "location_id": str,
            "score":       float,        # [0, 1], làm tròn 4 chữ số
            "reason":      str           # giải thích bằng tiếng Việt
        }
    ]
}
```

Danh sách đã được sắp xếp giảm dần theo `score`.

---

## 5. Cách sử dụng

```python
from modules.n6_activity_ranking import rank_activities

result = rank_activities({
    "user_vectors": {...},
    "context":      {...},
    "activities":   [...],
    "constraints":  {...},
    "top_k":        5,
})

for act in result["activities"]:
    print(act["score"], act["reason"])
```

---

## 6. Chi tiết các hàm con

### `hard_constraint_violated(metadata, constraints) → bool`
Lọc cứng. Trả `True` nếu `estimated_duration > duration` (hoạt động dài hơn thời gian rảnh) → loại khỏi danh sách. Không dùng cho ngân sách (ngân sách đi vào điểm mềm).

### `_semantic_score(user_vectors, act_vectors) → float ∈ [0, 1]`
Khớp sở thích bằng cosine similarity, theo 3 cặp kênh có trọng số:

| Kênh user | Kênh activity | Trọng số |
|---|---|---|
| `tag`     | `tag`    | 0.40 |
| `context` | `text`   | 0.35 |
| `emotion` | `intent` | 0.25 |

Cosine `[-1, 1]` được chuẩn hoá về `[0, 1]` bằng `(sim + 1) / 2` rồi lấy trung bình có trọng số. Cặp nào thiếu vector sẽ bị bỏ qua. Nếu không có cặp nào → trả về 0.5 (trung tính).

### `_constraint_score(metadata, constraints) → float ∈ [0, 1]`
Trung bình của 2 thành phần:

- **Ngân sách**: `(5.0 - price_level) / 4.0`, ép về `[0, 1]`. Hoạt động `price_level = 1.0` được 1.0; `price_level = 5.0` được 0.0.
- **Thời gian**: theo tỉ lệ `duration_act / duration_user`:
  - ≤ 10% → 0.7 (ngắn so với thời gian rảnh)
  - 10% – 70% → 1.0 (vừa đẹp)
  - \> 70% → giảm tuyến tính về 0 (chiếm gần hết)

### `_context_score(metadata, context, constraints) → float ∈ [0, 1]`
Trung bình của 2 thành phần:

- **Khung giờ**: `time_of_day_suitable == "anytime"` → 1.0; trùng giờ user → 1.0; lệch giờ → 0.3.
- **Thời tiết**: trời xấu (`rain`, `storm`, `snow`...) ưu tiên `indoor` (1.0) hoặc hoạt động không phụ thuộc thời tiết (0.8); ngoài trời + phụ thuộc thời tiết → 0.2. Trời đẹp ưu tiên `outdoor` (1.0).

### `_build_reason(metadata, sem_score, cons_score, ctx_score) → str`
Sinh câu giải thích tiếng Việt. Mỗi thành phần ≥ 0.75 → mô tả "Rất ..."; ≥ 0.55 → "Khá / ổn ...". Ví dụ:

> *Ngắm bình minh: Rất khớp với sở thích, rất phù hợp với ngân sách và thời gian, hợp khung giờ và thời tiết.*

---

## 7. Hành vi với input thiếu

Module thiết kế **fail-safe** — không raise exception khi thiếu dữ liệu:

| Tình huống | Xử lý |
|---|---|
| Thiếu `user_vectors` cho một kênh | Bỏ qua kênh đó, dùng các kênh còn lại |
| Thiếu hết vector | `_semantic_score = 0.5` (trung tính) |
| Thiếu `price_level` | Bỏ qua thành phần ngân sách |
| Thiếu `time_of_day` hoặc `weather` | Bỏ qua thành phần đó |
| `activities = []` | Trả về `{"activities": []}` |
| `top_k <= 0` | Trả về `{"activities": []}` |
| Vector 2 bên khác độ dài | Cosine = 0.0 |
| Vector toàn 0 (chia cho 0) | Cosine = 0.0 |

---

## 8. Cấu trúc file

```
n6_activity_ranking/
├── __init__.py            # Re-export hàm rank_activities
├── rank_activities.py     # Toàn bộ logic chấm điểm
├── requirements.txt       # Dependencies (chỉ math chuẩn)
└── README.md              # File này
```

Chỉ phụ thuộc `math` của Python chuẩn — không cần cài thêm thư viện.