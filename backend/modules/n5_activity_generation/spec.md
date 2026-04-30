# Báo Cáo Module N5: Phân Bổ Tiện Ích & Hoạt Động (Activity Generation)

## 1. Mô tả nhiệm vụ N5
Nhiệm vụ chính của module N5 là **đề xuất danh sách các hoạt động du lịch (activities)** phù hợp nhất cho người dùng.
N5 nhận đầu vào là các địa điểm nổi bật do module N4 đề xuất, sở thích cá nhân của người dùng (`user_tags`), cùng với quy tắc ràng buộc (constraints) như giới hạn ngân sách và tổng thời gian rảnh rỗi trong ngày. Đầu ra của hệ thống là danh sách top 12 các hoạt động được tính toán xếp hạng (ranking) dựa trên độ tương thích từ khóa để tạo tiền đề cho module N6 lên một lịch trình du lịch cụ thể chuẩn cá nhân hóa.

### Hybrid Approach (Nâng cấp)
Module N5 đã được nâng cấp từ **rule-based thuần túy** sang **hybrid approach** kết hợp LLM (Large Language Model) với template:

| Phương pháp | Ưu điểm | Nhược điểm |
|---|---|---|
| **Rule-based (Template)** | Ổn định, nhanh, không phụ thuộc mạng | Giới hạn bởi dữ liệu thủ công |
| **LLM (Gemini)** | Linh hoạt, cá nhân hóa cao, bao quát mọi địa điểm | Phụ thuộc API key & kết nối mạng |
| **Hybrid** | Kết hợp ưu điểm cả hai, fallback tự động | - |

**Lý do chọn Hybrid:**
1. **Giảm công xây dựng data thủ công**: LLM có thể sinh hoạt động cho bất kỳ địa điểm nào, không cần tạo template trước.
2. **Tăng tính cá nhân hóa**: LLM hiểu context sở thích, ngân sách, thời gian cụ thể để đề xuất phù hợp hơn.
3. **Fallback an toàn**: Khi LLM không khả dụng, hệ thống tự động dùng rule-based.

## 2. Decomposition & Abstraction (Tư duy Máy tính)

**Decomposition (Phân rã bài toán):**
Bài toán lớn "Đề xuất hoạt động du lịch" được chia nhỏ thành các bài toán thành phần tuần tự để giải quyết:
- **Truy xuất và Phân vùng** (Data Mapping): Chuyển hóa đối tượng là các điểm đến (locations) thành chi tiết các hoạt động đa dạng nhờ kho template cứng (`ACTIVITY_TEMPLATES`) hoặc sinh động bằng LLM.
- **So khớp tiêu chí** (Matching/Scoring): Với mỗi hoạt động, quét xem nội dung tag có đáp ứng được bao nhiêu sở thích người dùng tìm kiếm, từ đó cộng lại thành điểm match_score.
- **Tuân thủ ràng buộc** (Constraint Checking): Kiểm duyệt, loại bỏ ngay lập tức những hoạt động tiêu hao quá nhiều chi phí (vượt 50% tổng ngân sách) hoặc thâm hụt thời gian tham quan quá dài.
- **Chiết xuất cấu trúc** (Sorting & Extraction): Sắp xếp các lựa chọn tối ưu theo điểm số match_score để người dùng nhận được giải pháp được thỏa mãn tốt nhất (Greedy).

**Abstraction (Trừu tượng hóa):**
- Bỏ qua các chi tiết phức tạp của hoạt động thực tế như thời tiết, giao thông, nhà cung cấp, vị trí chính xác trên bản đồ.
- Trừu tượng hóa "Sở thích" hay "Thể loại" thành các từ khóa (`tags` dạng array of int/string).
- Trừu tượng hóa "Hoạt động" thành một Tuple/Dictionary lưu trữ duy nhất các đặc trưng thiết yếu để tính toán: Giá thành (`cost`), Thời gian tổn hao (`time`) và Hệ gen từ khóa (`tags`).

## 3. Algorithm Design

### 3.1 Rule-based (generate_activities)
Thuật toán được ứng dụng lối tiếp cận tham lam kết hợp Lọc - Sorting. Cụ thể qua mã giả (pseudocode):

```text
FUNCTION generate_activities(user_tags, locations, constraints):
    result_list = Rỗng
    budget_limit = constraints.get("budget") / 2
    time_limit = constraints.get("max_time_per_day")
    
    FOR EACH loc IN locations:
        IF loc.name TỒN TẠI TRONG ACTIVITY_TEMPLATES:
            activities = ACTIVITY_TEMPLATES[loc.name].activities
            
            FOR EACH act IN activities:
                # B1: Tính điểm Matching dựa theo tần suất tag
                score = Đếm số tag chung giữa user_tags VÀ act.tags
                
                # B2: Lọc các lựa chọn vi phạm sự cho phép về phí độ/thời gian
                IF act.cost > budget_limit HOẶC act.time > time_limit:
                    BỎ QUA hoạt động này
                
                # B3: Đưa lựa chọn tiềm năng vào danh sách ghi nhận
                THÊM (act, score) VÀO result_list
                
    # B4: Ưu tiên hóa theo điểm và giới hạn
    SẮP XẾP result_list THEO điểm score CHIỀU GIẢM DẦN
    TRẢ VỀ 12 kết quả đứng top đầu của result_list
```

### 3.2 Hybrid (generate_activities_hybrid)
```text
FUNCTION generate_activities_hybrid(user_tags, locations, constraints, use_llm=True):
    can_use_llm = use_llm AND có_API_key AND llm_module_available
    
    FOR EACH loc IN locations:
        llm_success = False
        
        IF can_use_llm:
            # Thử dùng LLM (Gemini) để sinh hoạt động
            llm_result = call_gemini_api(loc, user_tags, constraints)
            IF llm_result THÀNH CÔNG:
                # Post-processing: lọc constraints + tính match_score
                processed = post_process(llm_result)
                THÊM processed VÀO result_list
                llm_success = True
        
        IF NOT llm_success:
            # Fallback: dùng rule-based template (giống generate_activities)
            THÊM template_activities VÀO result_list
    
    SẮP XẾP result_list THEO match_score GIẢM DẦN
    TRẢ VỀ top 12 kết quả (mỗi kết quả có trường "generated_by")
```

## 4. Cấu trúc File

| File | Mô tả |
|---|---|
| `n5_activity_generator.py` | Logic chính: `generate_activities()` + `generate_activities_hybrid()` |
| `n5_activity_templates.py` | Database mẫu hoạt động theo địa điểm (rule-based) |
| `n5_llm_generator.py` | Module tích hợp LLM (Gemini API): prompt engineering, parse, validate |
| `test_n5_activity_generator.py` | 17 test cases (9 rule-based + 8 hybrid) |

## 5. Cách sử dụng

### 5.1 Rule-based (giữ nguyên API cũ)
```python
from n5_activity_generator import generate_activities

result = generate_activities(
    user_tags=["nature", "food"],
    locations=[{"name": "Sa Pa"}, {"name": "Huế"}],
    constraints={"budget": 5_000_000, "max_time_per_day": 480}
)
```

### 5.2 Hybrid (API mới)
```python
from n5_activity_generator import generate_activities_hybrid

# Dùng LLM (cần set GEMINI_API_KEY)
result = generate_activities_hybrid(
    user_tags=["nature", "food"],
    locations=[
        {"name": "Sa Pa", "description": "Thị trấn miền núi phía Bắc"},
        {"name": "Huế", "description": "Cố đô của triều Nguyễn"}
    ],
    constraints={"budget": 5_000_000, "max_time_per_day": 480},
    use_llm=True   # True: thử LLM → fallback template | False: chỉ template
)

# Mỗi activity có trường "generated_by": "llm" hoặc "template"
for act in result:
    print(f"{act['name']} - generated by: {act['generated_by']}")
```

### 5.3 Cài đặt LLM (Gemini)
```bash
# Set API key qua biến môi trường
set GEMINI_API_KEY=your_api_key_here

# (Tùy chọn) Đổi model
set GEMINI_MODEL=gemini-2.0-flash
```

Nếu không set `GEMINI_API_KEY`, hệ thống tự động fallback về rule-based.

## 6. Cách chạy Test
Dự án ứng dụng module thiết kế test `unittest` chuẩn của Python.
Cách thức chạy, từ thư mục `n5_activity`, nhập câu lệnh sau vào Terminal:

```bash
python -m unittest test_n5_activity_generator.py -v
```

Cờ `-v` (verbose) hỗ trợ xem rõ chi tiết danh sách từng hàm test đã chạy.

## 7. Kết quả Test mẫu
Module bao gồm **17 test cases** chia thành 2 nhóm:

### TestN5ActivityGenerator (9 tests) — Rule-based
- `test_generate_with_matching_tags`: Kiểm tra tag matching cơ bản.
- `test_budget_constraints`: Lọc theo ngân sách.
- `test_time_constraints`: Lọc theo thời gian.
- `test_missing_location`: Xử lý địa điểm không tồn tại.
- `test_sorting_by_match_score`: Sắp xếp đúng thứ tự.
- `test_limit_result_size`: Giới hạn 12 kết quả.
- `test_user_likes_relax_beach`: User thích relax + beach.
- `test_user_likes_culture_history`: User thích culture + history.
- `test_user_has_low_budget`: Ngân sách thấp (150k).

### TestN5HybridGenerator (8 tests) — Hybrid
- `test_hybrid_fallback_use_llm_false`: Fallback khi `use_llm=False`.
- `test_hybrid_has_generated_by_field`: Trường `generated_by` luôn có mặt.
- `test_hybrid_fallback_no_api_key`: Fallback khi không có API key.
- `test_hybrid_sorting_consistent`: Sắp xếp đúng trong hybrid mode.
- `test_hybrid_respects_constraints`: Tuân thủ constraints.
- `test_hybrid_with_mock_llm_success`: LLM thành công (mock).
- `test_hybrid_llm_failure_fallback`: LLM thất bại → fallback template.
- `test_original_generate_still_works`: Hàm gốc vẫn tương thích.

**Output minh họa ở cmd:**
```text
test_budget_constraints (...) ... ok
test_generate_with_matching_tags (...) ... ok
test_limit_result_size (...) ... ok
test_missing_location (...) ... ok
test_sorting_by_match_score (...) ... ok
test_time_constraints (...) ... ok
test_user_has_low_budget (...) ... ok
test_user_likes_culture_history (...) ... ok
test_user_likes_relax_beach (...) ... ok
test_hybrid_fallback_no_api_key (...) ... ok
test_hybrid_fallback_use_llm_false (...) ... ok
test_hybrid_has_generated_by_field (...) ... ok
test_hybrid_llm_failure_fallback (...) ... ok
test_hybrid_respects_constraints (...) ... ok
test_hybrid_sorting_consistent (...) ... ok
test_hybrid_with_mock_llm_success (...) ... ok
test_original_generate_still_works (...) ... ok

----------------------------------------------------------------------
Ran 17 tests in 0.003s

OK
```

