# =============================================================================
# n5_activity_templates.py
# Database mẫu các hoạt động du lịch theo địa điểm.
# File này chứa toàn bộ dữ liệu template cho module N5 Activity Generator.
# Có thể mở rộng thêm địa điểm và hoạt động mới tại đây.
# =============================================================================

from typing import Dict, Any

# Database mẫu activities theo location
# Mỗi location gồm: name, tags (đặc trưng địa điểm), và danh sách activities.
# Mỗi activity gồm: name, desc (mô tả), cost (VNĐ), time (phút), tags (phân loại).
ACTIVITY_TEMPLATES: Dict[str, Any] = {
    "Sa Pa": {
        "name": "Sa Pa",
        # Các tags đặc trưng: miền núi, thiên nhiên hùng vĩ, khí hậu mát mẻ, leo núi, văn hóa bản địa
        "tags": ["mountain", "nature", "cool", "trekking", "culture"],
        "activities": [
            {"name": "Trekking Fansipan", "desc": "Leo núi Fansipan bằng cáp treo hoặc trek nhẹ", "cost": 800000, "time": 240, "tags": ["adventure", "nature"]},
            {"name": "Thăm bản Cát Cát", "desc": "Khám phá văn hóa dân tộc và ruộng bậc thang", "cost": 150000, "time": 120, "tags": ["culture", "relax"]},
            {"name": "Chụp ảnh ruộng bậc thang", "desc": "Thưởng ngoạn và chụp ảnh tại ruộng bậc thang", "cost": 50000, "time": 90, "tags": ["photography", "nature"]},
            {"name": "Ăn đặc sản thắng cố & lợn cắp nách", "desc": "Thử ẩm thực địa phương", "cost": 200000, "time": 60, "tags": ["food"]},
        ]
    },
    "Phú Quốc": {
        "name": "Phú Quốc",
        # Các tags đặc trưng: biển đảo, nghỉ dưỡng, ngắm biển, thư giãn
        "tags": ["beach", "sea", "resort", "relax"],
        "activities": [
            {"name": "Snorkeling tại Bãi Sao", "desc": "Lặn ngắm san hô", "cost": 400000, "time": 180, "tags": ["adventure", "sea"]},
            {"name": "Thăm vườn tiêu", "desc": "Khám phá nông trại tiêu nổi tiếng", "cost": 100000, "time": 90, "tags": ["nature"]},
            {"name": "Ngắm hoàng hôn trên biển", "desc": "Thư giãn tại bãi biển", "cost": 50000, "time": 120, "tags": ["relax", "photography"]},
        ]
    },
    "Đà Lạt": {
        "name": "Đà Lạt",
        # Các tags đặc trưng: miền núi, khí hậu ôn đới, nhiều hoa, thích hợp ngắm cảnh và thư giãn
        "tags": ["mountain", "cool", "flower", "nature"],
        "activities": [
            {"name": "Tham quan đồi chè Cầu Đất", "desc": "Ngắm cảnh và thử trà", "cost": 150000, "time": 120, "tags": ["nature", "relax"]},
            {"name": "Chèo thuyền trên hồ Xuân Hương", "desc": "Hoạt động thư giãn", "cost": 100000, "time": 60, "tags": ["relax"]},
            {"name": "Thăm vườn hoa thành phố", "desc": "Chụp ảnh hoa", "cost": 80000, "time": 90, "tags": ["photography"]},
        ]
    },
    "Hội An": {
        "name": "Hội An",
        # Điểm đến đậm chất văn hóa, phù hợp cho người yêu lịch sử, nhiếp ảnh và thư giãn
        "tags": ["culture", "history", "food", "relax", "photography"],
        "activities": [
            {"name": "Tham quan phố cổ Hội An", "desc": "Khám phá các ngôi nhà cổ và hội quán", "cost": 120000, "time": 180, "tags": ["culture", "history", "photography"]},
            {"name": "Đi thuyền trên sông Hoài", "desc": "Ngắm phố cổ về đêm từ dưới thuyền và thả đèn hoa đăng", "cost": 150000, "time": 60, "tags": ["relax", "culture", "photography"]},
            {"name": "May áo dài lấy ngay", "desc": "May đo trang phục truyền thống tại các tiệm may nổi tiếng", "cost": 1000000, "time": 120, "tags": ["culture", "shopping"]},
            {"name": "Thưởng thức Cao Lầu & Mì Quảng", "desc": "Ăn các món đặc sản Hội An", "cost": 80000, "time": 60, "tags": ["food", "culture"]},
            {"name": "Đạp xe dạo quanh ruộng lúa", "desc": "Đạp xe ra vùng ven để ngắm cảnh và tận hưởng không khí trong lành", "cost": 50000, "time": 120, "tags": ["nature", "relax", "sports"]},
            {"name": "Tham gia lớp học nấu ăn", "desc": "Học làm các món ăn đặc trưng của miền Trung", "cost": 500000, "time": 150, "tags": ["food", "culture", "education"]},
            {"name": "Tham quan Rừng Dừa Bảy Mẫu", "desc": "Trải nghiệm ngồi thúng và xem biểu diễn múa thúng", "cost": 150000, "time": 120, "tags": ["nature", "adventure", "fun"]},
            {"name": "Tắm biển Cửa Đại/An Bàng", "desc": "Thư giãn trên bãi biển và tắm nắng", "cost": 0, "time": 180, "tags": ["beach", "relax"]},
        ]
    },
    "Hạ Long": {
        "name": "Hạ Long",
        # Thiên nhiên hùng vĩ trên biển, lý tưởng cho tour du thuyền và trải nghiệm khám phá
        "tags": ["sea", "nature", "cruise", "adventure"],
        "activities": [
            {"name": "Tour du thuyền Vịnh Hạ Long", "desc": "Ngắm các hòn đảo đá vôi và thưởng thức hải sản", "cost": 800000, "time": 240, "tags": ["sea", "nature", "relax"]},
            {"name": "Chèo Kayak trên Vịnh", "desc": "Tự do chèo thuyền kayak để đến gần các hang động", "cost": 200000, "time": 90, "tags": ["adventure", "sea", "sports"]},
            {"name": "Thăm Động Thiên Cung", "desc": "Tham quan hang động tự nhiên với nhũ đá tuyệt đẹp", "cost": 100000, "time": 60, "tags": ["nature", "sightseeing"]},
            {"name": "Vui chơi tại Sun World", "desc": "Chơi các trò chơi mạo hiểm và đi cáp treo Nữ Hoàng", "cost": 450000, "time": 240, "tags": ["fun", "entertainment"]},
            {"name": "Tắm biển Bãi Cháy", "desc": "Tắm biển và thưởng ngoạn hoàng hôn", "cost": 0, "time": 120, "tags": ["beach", "relax"]},
        ]
    },
    "Hà Giang": {
        "name": "Hà Giang",
        # Thiên đường của núi non, phiêu lưu bằng xe máy, hợp với người thích mạo hiểm và văn hóa bản địa
        "tags": ["mountain", "nature", "adventure", "culture", "motorbiking"],
        "activities": [
            {"name": "Lái xe máy đèo Mã Pí Lèng", "desc": "Trải nghiệm cung đường đèo hùng vĩ nhất Việt Nam", "cost": 250000, "time": 180, "tags": ["adventure", "motorbiking", "nature"]},
            {"name": "Đi thuyền trên sông Nho Quế", "desc": "Ngắm vực Tu Sản ngay dưới chân đèo Mã Pí Lèng", "cost": 120000, "time": 120, "tags": ["nature", "relax", "photography"]},
            {"name": "Tham quan Dinh Vua Mèo", "desc": "Tìm hiểu về gia tộc họ Vương và lịch sử vùng cao", "cost": 30000, "time": 60, "tags": ["culture", "history"]},
            {"name": "Check-in Cột cờ Lũng Cú", "desc": "Chinh phục điểm cực Bắc thiêng liêng của Tổ quốc", "cost": 40000, "time": 90, "tags": ["sightseeing", "history"]},
            {"name": "Chơi chợ phiên Đồng Văn", "desc": "Tham quan và thưởng thức thắng cố, rượu ngô", "cost": 100000, "time": 120, "tags": ["culture", "food"]},
            {"name": "Ngắm lúa chín Hoàng Su Phì", "desc": "Chụp ảnh tại các ruộng bậc thang ngút ngàn", "cost": 50000, "time": 150, "tags": ["nature", "photography"]},
        ]
    },
    "Nha Trang": {
        "name": "Nha Trang",
        # Thành phố biển phát triển, trung tâm giải trí và thể thao dưới nước
        "tags": ["beach", "sea", "entertainment", "relax"],
        "activities": [
            {"name": "Chơi VinWonders", "desc": "Khu vui chơi giải trí trên đảo Hòn Tre", "cost": 800000, "time": 360, "tags": ["fun", "entertainment", "family"]},
            {"name": "Tour 3 đảo", "desc": "Tham quan Hòn Mun, Hòn Tằm, trải nghiệm lặn biển", "cost": 500000, "time": 420, "tags": ["sea", "adventure", "nature"]},
            {"name": "Tắm bùn khoáng tháp Bà", "desc": "Thư giãn và cải thiện sức khỏe với bùn khoáng nóng", "cost": 250000, "time": 120, "tags": ["relax", "health"]},
            {"name": "Tham quan Tháp Bà Ponagar", "desc": "Khám phá kiến trúc đền tháp Chăm cổ", "cost": 30000, "time": 60, "tags": ["culture", "history"]},
            {"name": "Thưởng thức hải sản bãi biển", "desc": "Ăn tôm hùm, nhum biển với giá phải chăng", "cost": 500000, "time": 90, "tags": ["food"]},
        ]
    },
    "Huế": {
        "name": "Huế",
        # Cố đô yên bình, sở hữu các công trình kiến trúc Hoàng gia và ẩm thực cung đình độc đáo
        "tags": ["culture", "history", "food", "architecture", "relax"],
        "activities": [
            {"name": "Tham quan Đại Nội Huế", "desc": "Khám phá hoàng cung của các vị vua triều Nguyễn", "cost": 200000, "time": 180, "tags": ["history", "culture", "architecture"]},
            {"name": "Thăm Lăng tẩm các vua Nguyễn", "desc": "Tham quan lăng Khải Định, Minh Mạng, Tự Đức", "cost": 150000, "time": 180, "tags": ["history", "culture", "architecture"]},
            {"name": "Nghe Nhã nhạc cung đình Huế", "desc": "Đi thuyền rồng trên sông Hương và thưởng thức nhã nhạc", "cost": 100000, "time": 90, "tags": ["culture", "music", "relax"]},
            {"name": "Thưởng thức bún bò Huế & các loại bánh", "desc": "Ăn uống tại quán địa phương", "cost": 80000, "time": 60, "tags": ["food", "culture"]},
            {"name": "Tham quan chùa Thiên Mụ", "desc": "Vãn cảnh ngôi chùa cổ kính bên dòng sông Hương", "cost": 0, "time": 60, "tags": ["culture", "history", "sightseeing"]},
            {"name": "Đạp xe tham quan làng Thủy Biều", "desc": "Trải nghiệm làm thanh trà, nấu ăn và massage chân", "cost": 300000, "time": 180, "tags": ["nature", "culture", "relax"]},
        ]
    }
}
