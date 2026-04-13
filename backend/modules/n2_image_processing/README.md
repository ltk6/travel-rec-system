# 🌍 Module N2: Image Feature Extraction for Tourism

Đây là thành phần xử lý thị giác máy tính (**Computer Vision**) trong hệ thống **Travel Recommendation System**. Module có nhiệm vụ phân tích hình ảnh du lịch và chuyển hóa thành văn bản mô tả giàu ngữ nghĩa để phục vụ cho các module gợi ý phía sau.

---

## 🛠 Công nghệ & Thư viện
* **Core:** Python 3.10+
* **Framework:** FastAPI
* **AI Model:** Google Gemini 2.5 Flash
* **Libraries:** `google-generativeai`, `Pillow`, `requests`, `uvicorn`

---

## ⚙️ Cài đặt môi trường

### 1. Cài đặt thư viện
Mở Terminal và chạy lệnh sau để cài đặt các phụ thuộc:
```bash
pip install -r requirements.txt
```
### 2. Cấu hình API Key
Mở file `process_image.py` và dán API Key của bạn vào dòng cấu hình:
```bash
genai.configure(api_key="AIzaSy... (Key của bạn)")
```

### 🚀 Hướng dẫn Chạy & Test (2 Cách)
Để test module này, trước hết bạn phải khởi động Server (Bộ não):
```Bash
python -m uvicorn process_image:app --reload
```
Lưu ý: Đợi Terminal báo Application startup complete mới bắt đầu thực hiện các bước test bên dưới.

* **Cách 1: Test bằng Giao diện Web (Swagger UI)
Đây là cách trực quan nhất, không cần viết thêm code.

Truy cập: http://127.0.0.1:8000/docs

Tìm đến Endpoint POST /api/v1/process-image.

Nhấn Try it out.

Ở phần file, nhấn Choose File và chọn một ảnh có sẵn trong máy.

Nhấn Execute và xem kết quả JSON ở ô phía dưới.

* **Cách 2: Test bằng Script Terminal (test_api.py)
Đây là cách mô phỏng chính xác việc Module khác gọi API của bạn bằng mã nguồn.

Mở một Terminal mới (song song với Terminal đang chạy Server).

Chạy lệnh:

```Bash
python test_api.py
```
Kết quả sẽ được in trực tiếp ra màn hình Terminal dưới dạng JSON.

### 📡 Chi tiết API (Data Contract)
Endpoint: /api/v1/process-image

Method: POST

Body (Multipart): file (Ảnh định dạng .jpg, .png, .webp)

Kết quả trả về (Response):

```JSON
{
  "image_decription": "Đoạn văn mô tả đặc trưng du lịch do AI sinh ra, bao gồm loại hình địa điểm, kiến trúc và không khí..."
}
```
