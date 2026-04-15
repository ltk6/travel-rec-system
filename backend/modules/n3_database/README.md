# Báo Cáo Module N3: Lưu Trữ & Truy Vấn (Database)

## 1. Mô tả nhiệm vụ N3
Module N3 đóng vai trò là "Trái tim lưu trữ" của hệ thống Smart Tourism. 
N3 nhận dữ liệu đã qua nhúng (embedding) từ N1 để lưu trữ lâu dài. Đồng thời, N3 cung cấp các API truy vấn tốc độ cao (Pre-filtering) cho N8, giúp lược bỏ các địa điểm vi phạm quy tắc cứng (vượt ngân sách, quá thời gian) trước khi chuyển dữ liệu sang phân hệ tính toán xếp hạng Vector.

**Giải thích Vector Search (Optional):** Hệ thống sử dụng thuật toán KNN (K-Nearest Neighbors) kết hợp với extension `pgvector` để tìm kiếm các vector địa điểm có khoảng cách không gian gần nhất với vector sở thích của người dùng, từ đó đưa ra gợi ý chính xác nhất.

## 2. Decomposition & Abstraction (Tư duy Máy tính)
- **Decomposition:** Chia tác vụ DB thành 2 nhóm độc lập: 
  1. Nhóm Ghi (Write): `save_user_profile`, `save_location`.
  2. Nhóm Đọc/Lọc (Read/Query): `filter_locations`.
- **Abstraction:** Che giấu hoàn toàn các phức tạp của PostgreSQL (Connections, URI, JSON Parsing, Vector string conversion). N8 chỉ cần gọi các hàm Python thuần túy với parameters đơn giản (`budget`, `duration`) và nhận về `List[Dict]` chuẩn.

## 3. Quản lý Môi trường An Toàn (Environment Variables)
N3 sử dụng `python-dotenv` để ẩn chuỗi kết nối an toàn.
- Nếu môi trường có biến `PG_URI`, hệ thống sẽ kết nối đến đúng Database đó.
- Tính năng **Fallback**: Nếu các thành viên khác tải code về không có file `.env`, hệ thống tự động trỏ về `localhost:5432` (cổng mặc định của PostgreSQL), giúp quá trình setup của nhóm dễ dàng hơn.

## 4. Cách chạy Unit Test (Mocking)
N3 sử dụng `unittest.mock` để giả lập Database Connection, cho phép test logic độc lập mà không cần bật DB thật.
```bash
python -m unittest test_n3.py -v