# Báo Cáo Module N3: Lưu Trữ & Truy Vấn (Database)

## 1. Mô tả nhiệm vụ N3
Module N3 đóng vai trò là "Trái tim lưu trữ" của hệ thống Smart Tourism. 
N3 nhận dữ liệu đã qua nhúng (embedding) từ N1 để lưu trữ lâu dài. Đồng thời, N3 cung cấp các API truy vấn tốc độ cao (Pre-filtering) cho N8, giúp lược bỏ các địa điểm vi phạm quy tắc cứng (vượt ngân sách, quá thời gian) trước khi chuyển dữ liệu sang N4 để tính toán xếp hạng Vector.

## 2. Decomposition & Abstraction (Tư duy Máy tính)
- **Decomposition:** Chia tác vụ DB thành 2 nhóm độc lập: 
  1. Nhóm Ghi (Write): `save_user_profile`, `save_location`.
  2. Nhóm Đọc/Lọc (Read/Query): `filter_locations`.
- **Abstraction:** Che giấu hoàn toàn các phức tạp của MongoDB (Connections, URI, JSON Parsing). N8 chỉ cần gọi các hàm Python thuần túy với parameters đơn giản (`budget`, `duration`) và nhận về `List[Dict]` chuẩn.

## 3. Quản lý Môi trường An Toàn (Environment Variables)
N3 sử dụng `python-dotenv` để ẩn chuỗi kết nối an toàn.
- Nếu môi trường có biến `MONGO_URI` (kết nối Cloud), hệ thống sẽ dùng Cloud.
- Tính năng **Fallback**: Nếu các thành viên khác tải code về không có file `.env`, hệ thống tự động trỏ về `localhost:27017` và vô hiệu hóa các lỗi crash, đảm bảo không ảnh hưởng đến việc test các module N1, N2, N4, N5, N6.

## 4. Cách chạy Unit Test (Mocking)
N3 sử dụng `unittest.mock` để giả lập Database. 
```bash
python -m unittest test_n3.py -v