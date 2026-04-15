from db_manager import init_db, save_location

def seed_database():
    # Bước cực kỳ quan trọng đối với PostgreSQL: Tạo bảng trước
    init_db()
    
    locations = [
        {"location_id": "loc_001", "vector": [0.12, 0.85, 0.45, 0.1, 0.9], "metadata": {"name": "Bãi Sau Vũng Tàu", "description": "Biển nhộn nhịp", "tags": ["beach", "vibrant"], "price_level": 1500000, "estimated_duration": 1}, "geo": {"lat": 10.34, "lng": 107.08}},
        {"location_id": "loc_002", "vector": [0.75, 0.15, 0.9, 0.3, 0.2], "metadata": {"name": "Đỉnh Langbiang Đà Lạt", "description": "Nóc nhà Đà Lạt", "tags": ["mountain", "nature"], "price_level": 800000, "estimated_duration": 1}, "geo": {"lat": 12.04, "lng": 108.42}},
        {"location_id": "loc_003", "vector": [0.2, 0.9, 0.1, 0.8, 0.5], "metadata": {"name": "Phố Cổ Hội An", "description": "Di sản văn hóa", "tags": ["culture", "history"], "price_level": 2000000, "estimated_duration": 2}, "geo": {"lat": 15.88, "lng": 108.33}},
        {"location_id": "loc_004", "vector": [0.9, 0.8, 0.2, 0.1, 0.3], "metadata": {"name": "Vịnh Hạ Long", "description": "Kỳ quan thiên nhiên", "tags": ["sea", "nature"], "price_level": 5000000, "estimated_duration": 2}, "geo": {"lat": 20.91, "lng": 107.18}},
        {"location_id": "loc_005", "vector": [0.85, 0.3, 0.7, 0.4, 0.1], "metadata": {"name": "Fansipan Sapa", "description": "Nóc nhà Đông Dương", "tags": ["mountain", "adventure"], "price_level": 3500000, "estimated_duration": 1}, "geo": {"lat": 22.30, "lng": 103.77}},
        {"location_id": "loc_006", "vector": [0.1, 0.4, 0.2, 0.9, 0.8], "metadata": {"name": "Đại Nội Huế", "description": "Kiến trúc cung đình", "tags": ["history", "culture"], "price_level": 1200000, "estimated_duration": 1}, "geo": {"lat": 16.46, "lng": 107.57}},
        {"location_id": "loc_007", "vector": [0.05, 0.95, 0.3, 0.1, 0.7], "metadata": {"name": "Bãi Sao Phú Quốc", "description": "Cát trắng mịn", "tags": ["beach", "relax"], "price_level": 4000000, "estimated_duration": 2}, "geo": {"lat": 10.06, "lng": 104.03}},
        {"location_id": "loc_008", "vector": [0.6, 0.4, 0.8, 0.2, 0.5], "metadata": {"name": "Phong Nha - Kẻ Bàng", "description": "Hang động kỳ ảo", "tags": ["nature", "cave"], "price_level": 2500000, "estimated_duration": 3}, "geo": {"lat": 17.48, "lng": 106.27}},
        {"location_id": "loc_009", "vector": [0.3, 0.2, 0.1, 0.9, 0.6], "metadata": {"name": "Chợ Nổi Cái Răng", "description": "Văn hóa sông nước", "tags": ["culture", "river"], "price_level": 700000, "estimated_duration": 1}, "geo": {"lat": 9.99, "lng": 105.74}},
        {"location_id": "loc_010", "vector": [0.8, 0.1, 0.9, 0.2, 0.4], "metadata": {"name": "Mũi Né Phan Thiết", "description": "Đồi cát bay", "tags": ["beach", "nature"], "price_level": 2200000, "estimated_duration": 2}, "geo": {"lat": 10.94, "lng": 108.30}},
        {"location_id": "loc_011", "vector": [0.7, 0.3, 0.6, 0.5, 0.9], "metadata": {"name": "Đồng Văn Hà Giang", "description": "Cao nguyên đá", "tags": ["mountain", "adventure"], "price_level": 3000000, "estimated_duration": 4}, "geo": {"lat": 23.23, "lng": 105.25}},
        {"location_id": "loc_012", "vector": [0.15, 0.8, 0.2, 0.3, 0.6], "metadata": {"name": "Bà Nà Hills", "description": "Cầu Vàng nổi tiếng", "tags": ["entertainment", "photography"], "price_level": 4500000, "estimated_duration": 1}, "geo": {"lat": 15.99, "lng": 107.98}},
        {"location_id": "loc_013", "vector": [0.4, 0.5, 0.1, 0.7, 0.8], "metadata": {"name": "Thác Bản Giốc", "description": "Thác nước biên giới", "tags": ["nature", "waterfall"], "price_level": 2000000, "estimated_duration": 2}, "geo": {"lat": 22.85, "lng": 106.72}},
        {"location_id": "loc_014", "vector": [0.25, 0.6, 0.4, 0.9, 0.2], "metadata": {"name": "Tràng An Ninh Bình", "description": "Di sản kép", "tags": ["nature", "quiet"], "price_level": 1800000, "estimated_duration": 1}, "geo": {"lat": 20.25, "lng": 105.91}},
        {"location_id": "loc_015", "vector": [0.1, 0.9, 0.5, 0.2, 0.3], "metadata": {"name": "VinWonders Nha Trang", "description": "Công viên giải trí biển", "tags": ["entertainment", "fun"], "price_level": 3800000, "estimated_duration": 1}, "geo": {"lat": 12.21, "lng": 109.24}},
        {"location_id": "loc_016", "vector": [0.5, 0.1, 0.8, 0.3, 0.4], "metadata": {"name": "Thung Lũng Tình Yêu", "description": "Cảnh quan lãng mạn", "tags": ["romantic", "photography"], "price_level": 600000, "estimated_duration": 1}, "geo": {"lat": 11.97, "lng": 108.45}},
        {"location_id": "loc_017", "vector": [0.9, 0.2, 0.4, 0.1, 0.2], "metadata": {"name": "Mẫu Sơn Lạng Sơn", "description": "Đỉnh núi mây phủ", "tags": ["mountain", "cold"], "price_level": 1000000, "estimated_duration": 1}, "geo": {"lat": 21.85, "lng": 106.91}},
        {"location_id": "loc_018", "vector": [0.1, 0.5, 0.3, 0.8, 0.9], "metadata": {"name": "Làng Chài Mũi Né", "description": "Hải sản tươi sống", "tags": ["food", "culture"], "price_level": 500000, "estimated_duration": 1}, "geo": {"lat": 10.94, "lng": 108.29}},
        {"location_id": "loc_019", "vector": [0.6, 0.3, 0.2, 0.8, 0.7], "metadata": {"name": "Côn Đảo", "description": "Thiên nhiên hoang sơ", "tags": ["beach", "history"], "price_level": 6000000, "estimated_duration": 3}, "geo": {"lat": 8.68, "lng": 106.60}},
        {"location_id": "loc_020", "vector": [0.3, 0.4, 0.5, 0.6, 0.7], "metadata": {"name": "Đảo Lý Sơn", "description": "Vương quốc tỏi", "tags": ["beach", "island"], "price_level": 2500000, "estimated_duration": 2}, "geo": {"lat": 15.38, "lng": 109.11}}
    ]

    print(f"🚀 N3: Đang bơm {len(locations)} địa điểm vào PostgreSQL...")
    for loc in locations:
        save_location(loc)
    print("✨ Hoàn thành nạp dữ liệu!")

if __name__ == "__main__":
    seed_database()