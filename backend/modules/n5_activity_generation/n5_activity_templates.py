# =============================================================================
# n5_activity_templates.py
# Database mẫu các hoạt động du lịch theo địa điểm (PHIÊN BẢN MỞ RỘNG).
#
# File này chứa toàn bộ dữ liệu template cho module N5 Activity Generator.
# Có thể mở rộng thêm địa điểm và hoạt động mới tại đây.
#
# SCHEMA MỚI (v2):
#   Mỗi activity gồm đầy đủ các trường:
#     - activity_id:        ID duy nhất (str)
#     - location_id:        ID location (str)
#     - name:               Tên hoạt động (str)
#     - description:        Mô tả hấp dẫn 2-4 câu (str)
#     - tags:               5-7 tags phong phú để hỗ trợ embedding (list[str])
#     - cost:               Chi phí VNĐ/người (int)
#     - estimated_duration: Thời gian ước tính (phút) (int)
#     - best_time:          Thời gian tốt nhất trong ngày (list[str])
#     - suitable_for:       Đối tượng phù hợp (list[str])
#     - difficulty:         Mức độ khó (str: easy/medium/hard)
#     - season:             Tháng phù hợp nhất (list[str])
#     - reason_template:    Template ngắn giải thích cá nhân hóa (str)
#
# CÁC TRƯỜNG CŨ TƯƠNG THÍCH NGƯỢC:
#   - "desc" → alias cho "description" (dùng trong generate_activities gốc)
#   - "time" → alias cho "estimated_duration"
#   - "cost" → giữ nguyên
#   - "tags" → giữ nguyên nhưng mở rộng 5-7 tags
# =============================================================================

import json
import os
import logging
from typing import Dict, Any, List, Optional

logger = logging.getLogger(__name__)

# ===========================================================================
# ĐƯỜNG DẪN TỚI FILE JSON CHÍNH (tạo bởi LLM / script generate)
# ===========================================================================
_CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
_DATA_DIR = os.path.join(_CURRENT_DIR, "..", "..", "data")
_ACTIVITIES_JSON_PATH = os.path.join(_DATA_DIR, "activities.json")


def load_activities_from_json(json_path: str = None) -> List[Dict]:
    """
    Đọc danh sách activities từ file JSON.
    
    File JSON chứa toàn bộ activities với đầy đủ schema v2.
    Nếu file không tồn tại → trả về list rỗng và log warning.
    
    Returns:
        List[Dict]: Danh sách activities từ JSON.
    """
    path = json_path or _ACTIVITIES_JSON_PATH
    if not os.path.exists(path):
        logger.warning(f"Không tìm thấy file activities JSON: {path}")
        return []
    
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        if not isinstance(data, list):
            logger.error(f"File activities JSON không phải là array: {path}")
            return []
        
        logger.info(f"Đã load {len(data)} activities từ {path}")
        return data
    except json.JSONDecodeError as e:
        logger.error(f"Lỗi parse JSON tại {path}: {e}")
        return []
    except Exception as e:
        logger.error(f"Lỗi đọc file {path}: {e}")
        return []


def group_activities_by_location(activities: List[Dict]) -> Dict[str, Dict]:
    """
    Nhóm activities theo location_id, trả về dict tương thích với ACTIVITY_TEMPLATES cũ.
    
    Input: danh sách activities từ JSON (schema v2)
    Output: dict có dạng:
    {
        "Sa Pa": {
            "name": "Sa Pa",
            "tags": [...],   # tổng hợp unique tags từ tất cả activities
            "activities": [
                {
                    "name": "...",
                    "desc": "...",        # alias cho description
                    "cost": ...,
                    "time": ...,          # alias cho estimated_duration
                    "tags": [...],
                    # + tất cả các trường schema v2 khác
                }
            ]
        }
    }
    
    Đảm bảo backward-compatible với hàm generate_activities gốc.
    """
    # Mapping từ location_id → tên hiển thị
    LOCATION_ID_TO_NAME = {
        "loc_sapa": "Sa Pa",
        "loc_dalat": "Đà Lạt",
        "loc_hoian": "Hội An",
        "loc_phuquoc": "Phú Quốc",
        "loc_hagiang": "Hà Giang",
        "loc_phongnha": "Phong Nha",
        "loc_hue": "Huế",
        "loc_danang": "Đà Nẵng",
        "loc_halong": "Hạ Long",
        "loc_nhatrang": "Nha Trang",
    }
    
    grouped: Dict[str, Dict] = {}
    
    for act in activities:
        loc_id = act.get("location_id", "")
        loc_name = LOCATION_ID_TO_NAME.get(loc_id, loc_id.replace("loc_", "").replace("_", " ").title())
        
        if loc_name not in grouped:
            grouped[loc_name] = {
                "name": loc_name,
                "tags": [],
                "activities": [],
            }
        
        # Tạo activity entry tương thích ngược (có cả trường cũ và mới)
        activity_entry = {
            # Trường cũ (backward-compatible)
            "name": act.get("name", ""),
            "desc": act.get("description", ""),
            "cost": act.get("cost", 0),
            "time": act.get("estimated_duration", 60),
            "tags": act.get("tags", []),
            
            # Trường mới (schema v2)
            "activity_id": act.get("activity_id", ""),
            "location_id": act.get("location_id", ""),
            "description": act.get("description", ""),
            "estimated_duration": act.get("estimated_duration", 60),
            "best_time": act.get("best_time", []),
            "suitable_for": act.get("suitable_for", []),
            "difficulty": act.get("difficulty", "easy"),
            "season": act.get("season", []),
            "reason_template": act.get("reason_template", ""),
        }
        
        grouped[loc_name]["activities"].append(activity_entry)
        
        # Tổng hợp unique tags cho location
        for tag in act.get("tags", []):
            if tag not in grouped[loc_name]["tags"]:
                grouped[loc_name]["tags"].append(tag)
    
    return grouped


# ===========================================================================
# ACTIVITY_TEMPLATES: DICT CHÍNH DÙNG BỞI generate_activities()
#
# Ưu tiên: load từ activities.json (schema v2 đầy đủ)
# Fallback: dùng hardcoded templates bên dưới nếu JSON không tồn tại
# ===========================================================================

# Hardcoded fallback templates (schema v1 - tương thích ngược)
_FALLBACK_TEMPLATES: Dict[str, Any] = {
    "Sa Pa": {
        "name": "Sa Pa",
        "tags": ["mountain", "nature", "cool", "trekking", "culture"],
        "activities": [
            {"name": "Trekking Fansipan", "desc": "Leo núi Fansipan bằng cáp treo hoặc trek nhẹ", "cost": 800000, "time": 240, "tags": ["adventure", "nature", "trekking", "mountain", "iconic"]},
            {"name": "Thăm bản Cát Cát", "desc": "Khám phá văn hóa dân tộc và ruộng bậc thang", "cost": 150000, "time": 120, "tags": ["culture", "relax", "ethnic", "village", "photography"]},
            {"name": "Chụp ảnh ruộng bậc thang", "desc": "Thưởng ngoạn và chụp ảnh tại ruộng bậc thang", "cost": 50000, "time": 90, "tags": ["photography", "nature", "landscape", "scenic"]},
            {"name": "Ăn đặc sản thắng cố & lợn cắp nách", "desc": "Thử ẩm thực địa phương", "cost": 200000, "time": 60, "tags": ["food", "cuisine", "local_food", "culture"]},
        ]
    },
    "Phú Quốc": {
        "name": "Phú Quốc",
        "tags": ["beach", "sea", "resort", "relax", "island"],
        "activities": [
            {"name": "Snorkeling tại Bãi Sao", "desc": "Lặn ngắm san hô", "cost": 400000, "time": 180, "tags": ["adventure", "sea", "snorkeling", "nature"]},
            {"name": "Thăm vườn tiêu", "desc": "Khám phá nông trại tiêu nổi tiếng", "cost": 100000, "time": 90, "tags": ["nature", "agriculture", "education"]},
            {"name": "Ngắm hoàng hôn trên biển", "desc": "Thư giãn tại bãi biển", "cost": 50000, "time": 120, "tags": ["relax", "photography", "sunset", "beach"]},
        ]
    },
    "Đà Lạt": {
        "name": "Đà Lạt",
        "tags": ["mountain", "cool", "flower", "nature", "romantic"],
        "activities": [
            {"name": "Tham quan đồi chè Cầu Đất", "desc": "Ngắm cảnh và thử trà", "cost": 150000, "time": 120, "tags": ["nature", "relax", "tea", "photography"]},
            {"name": "Chèo thuyền trên hồ Xuân Hương", "desc": "Hoạt động thư giãn", "cost": 100000, "time": 60, "tags": ["relax", "lake", "romantic"]},
            {"name": "Thăm vườn hoa thành phố", "desc": "Chụp ảnh hoa", "cost": 80000, "time": 90, "tags": ["photography", "flower", "nature", "garden"]},
        ]
    },
    "Hội An": {
        "name": "Hội An",
        "tags": ["culture", "history", "food", "relax", "photography", "heritage"],
        "activities": [
            {"name": "Tham quan phố cổ Hội An", "desc": "Khám phá các ngôi nhà cổ và hội quán", "cost": 120000, "time": 180, "tags": ["culture", "history", "photography", "heritage"]},
            {"name": "Đi thuyền trên sông Hoài", "desc": "Ngắm phố cổ về đêm và thả đèn hoa đăng", "cost": 150000, "time": 60, "tags": ["relax", "culture", "photography", "romantic"]},
            {"name": "May áo dài lấy ngay", "desc": "May đo trang phục truyền thống", "cost": 1000000, "time": 120, "tags": ["culture", "shopping", "fashion", "traditional"]},
            {"name": "Thưởng thức Cao Lầu & Mì Quảng", "desc": "Ăn các món đặc sản Hội An", "cost": 80000, "time": 60, "tags": ["food", "culture", "local_food", "cuisine"]},
            {"name": "Đạp xe dạo quanh ruộng lúa", "desc": "Đạp xe ra vùng ven ngắm cảnh", "cost": 50000, "time": 120, "tags": ["nature", "relax", "sports", "cycling"]},
            {"name": "Tham gia lớp học nấu ăn", "desc": "Học làm các món ăn đặc trưng miền Trung", "cost": 500000, "time": 150, "tags": ["food", "culture", "education", "cooking"]},
            {"name": "Tham quan Rừng Dừa Bảy Mẫu", "desc": "Trải nghiệm ngồi thúng và múa thúng", "cost": 150000, "time": 120, "tags": ["nature", "adventure", "fun", "boat"]},
            {"name": "Tắm biển Cửa Đại/An Bàng", "desc": "Thư giãn trên bãi biển", "cost": 0, "time": 180, "tags": ["beach", "relax", "swimming"]},
        ]
    },
    "Hạ Long": {
        "name": "Hạ Long",
        "tags": ["sea", "nature", "cruise", "adventure", "island"],
        "activities": [
            {"name": "Tour du thuyền Vịnh Hạ Long", "desc": "Ngắm hòn đảo đá vôi và thưởng thức hải sản", "cost": 800000, "time": 240, "tags": ["sea", "nature", "relax", "cruise", "sightseeing"]},
            {"name": "Chèo Kayak trên Vịnh", "desc": "Tự do chèo thuyền kayak đến gần hang động", "cost": 200000, "time": 90, "tags": ["adventure", "sea", "sports", "kayak"]},
            {"name": "Thăm Động Thiên Cung", "desc": "Tham quan hang động tự nhiên với nhũ đá tuyệt đẹp", "cost": 100000, "time": 60, "tags": ["nature", "sightseeing", "cave", "geology"]},
            {"name": "Vui chơi tại Sun World", "desc": "Chơi các trò mạo hiểm và đi cáp treo", "cost": 450000, "time": 240, "tags": ["fun", "entertainment", "theme_park"]},
            {"name": "Tắm biển Bãi Cháy", "desc": "Tắm biển và thưởng ngoạn hoàng hôn", "cost": 0, "time": 120, "tags": ["beach", "relax", "swimming"]},
        ]
    },
    "Hà Giang": {
        "name": "Hà Giang",
        "tags": ["mountain", "nature", "adventure", "culture", "motorbiking"],
        "activities": [
            {"name": "Lái xe máy đèo Mã Pí Lèng", "desc": "Trải nghiệm cung đường đèo hùng vĩ nhất Việt Nam", "cost": 250000, "time": 180, "tags": ["adventure", "motorbiking", "nature", "scenic"]},
            {"name": "Đi thuyền trên sông Nho Quế", "desc": "Ngắm vực Tu Sản dưới chân đèo Mã Pí Lèng", "cost": 120000, "time": 120, "tags": ["nature", "relax", "photography", "canyon"]},
            {"name": "Tham quan Dinh Vua Mèo", "desc": "Tìm hiểu gia tộc họ Vương và lịch sử vùng cao", "cost": 30000, "time": 60, "tags": ["culture", "history", "architecture"]},
            {"name": "Check-in Cột cờ Lũng Cú", "desc": "Chinh phục điểm cực Bắc Tổ quốc", "cost": 40000, "time": 90, "tags": ["sightseeing", "history", "patriotic", "hiking"]},
            {"name": "Chơi chợ phiên Đồng Văn", "desc": "Tham quan và thưởng thức thắng cố, rượu ngô", "cost": 100000, "time": 120, "tags": ["culture", "food", "market", "ethnic"]},
            {"name": "Ngắm lúa chín Hoàng Su Phì", "desc": "Chụp ảnh tại ruộng bậc thang ngút ngàn", "cost": 50000, "time": 150, "tags": ["nature", "photography", "rice_terrace", "scenic"]},
        ]
    },
    "Nha Trang": {
        "name": "Nha Trang",
        "tags": ["beach", "sea", "entertainment", "relax", "diving"],
        "activities": [
            {"name": "Chơi VinWonders", "desc": "Khu vui chơi giải trí trên đảo Hòn Tre", "cost": 800000, "time": 360, "tags": ["fun", "entertainment", "family", "theme_park"]},
            {"name": "Tour 3 đảo", "desc": "Tham quan Hòn Mun, Hòn Tằm, trải nghiệm lặn biển", "cost": 500000, "time": 420, "tags": ["sea", "adventure", "nature", "island"]},
            {"name": "Tắm bùn khoáng tháp Bà", "desc": "Thư giãn với bùn khoáng nóng", "cost": 250000, "time": 120, "tags": ["relax", "health", "spa", "wellness"]},
            {"name": "Tham quan Tháp Bà Ponagar", "desc": "Khám phá kiến trúc đền tháp Chăm cổ", "cost": 30000, "time": 60, "tags": ["culture", "history", "architecture", "temple"]},
            {"name": "Thưởng thức hải sản bãi biển", "desc": "Ăn tôm hùm, nhum biển với giá hợp lý", "cost": 500000, "time": 90, "tags": ["food", "seafood", "local_food"]},
        ]
    },
    "Huế": {
        "name": "Huế",
        "tags": ["culture", "history", "food", "architecture", "relax", "heritage"],
        "activities": [
            {"name": "Tham quan Đại Nội Huế", "desc": "Khám phá hoàng cung của vua triều Nguyễn", "cost": 200000, "time": 180, "tags": ["history", "culture", "architecture", "heritage"]},
            {"name": "Thăm Lăng tẩm các vua Nguyễn", "desc": "Tham quan lăng Khải Định, Minh Mạng, Tự Đức", "cost": 150000, "time": 180, "tags": ["history", "culture", "architecture", "royal"]},
            {"name": "Nghe Nhã nhạc cung đình Huế", "desc": "Đi thuyền rồng trên sông Hương và thưởng thức nhã nhạc", "cost": 100000, "time": 90, "tags": ["culture", "music", "relax", "heritage"]},
            {"name": "Thưởng thức bún bò Huế & các loại bánh", "desc": "Ăn uống tại quán địa phương", "cost": 80000, "time": 60, "tags": ["food", "culture", "local_food", "cuisine"]},
            {"name": "Tham quan chùa Thiên Mụ", "desc": "Vãn cảnh ngôi chùa cổ kính bên sông Hương", "cost": 0, "time": 60, "tags": ["culture", "history", "sightseeing", "temple"]},
            {"name": "Đạp xe tham quan làng Thủy Biều", "desc": "Trải nghiệm làm thanh trà, nấu ăn và massage chân", "cost": 300000, "time": 180, "tags": ["nature", "culture", "relax", "cycling"]},
        ]
    },
}


def _build_activity_templates() -> Dict[str, Any]:
    """
    Xây dựng ACTIVITY_TEMPLATES từ nguồn dữ liệu tốt nhất có sẵn.
    
    Ưu tiên:
      1. Load từ activities.json (schema v2, đầy đủ 100+ activities)
      2. Fallback về _FALLBACK_TEMPLATES nếu JSON không tồn tại
    
    Kết quả được cache ở module level (ACTIVITY_TEMPLATES).
    """
    json_activities = load_activities_from_json()
    
    if json_activities:
        templates = group_activities_by_location(json_activities)
        logger.info(
            f"Loaded {len(json_activities)} activities cho {len(templates)} locations từ JSON"
        )
        return templates
    else:
        logger.info("Sử dụng fallback templates (hardcoded)")
        return _FALLBACK_TEMPLATES


# Module-level constant: dùng bởi n5_activity_generator.py
ACTIVITY_TEMPLATES: Dict[str, Any] = _build_activity_templates()


# ===========================================================================
# TIỆN ÍCH: Lấy danh sách tất cả locations, activities, thống kê
# ===========================================================================

def get_all_location_names() -> List[str]:
    """Trả về danh sách tên tất cả locations có trong templates."""
    return list(ACTIVITY_TEMPLATES.keys())


def get_activities_for_location(location_name: str) -> List[Dict]:
    """Trả về danh sách activities cho một location cụ thể."""
    template = ACTIVITY_TEMPLATES.get(location_name, {})
    return template.get("activities", [])


def get_total_activity_count() -> int:
    """Đếm tổng số activities trên tất cả locations."""
    total = 0
    for loc_data in ACTIVITY_TEMPLATES.values():
        total += len(loc_data.get("activities", []))
    return total


def get_stats() -> Dict:
    """
    Thống kê tổng quan về database activities.
    
    Returns:
        Dict với các key: total_locations, total_activities, locations_detail
    """
    stats = {
        "total_locations": len(ACTIVITY_TEMPLATES),
        "total_activities": 0,
        "locations_detail": {}
    }
    
    for loc_name, loc_data in ACTIVITY_TEMPLATES.items():
        count = len(loc_data.get("activities", []))
        stats["total_activities"] += count
        stats["locations_detail"][loc_name] = {
            "activity_count": count,
            "tags": loc_data.get("tags", []),
        }
    
    return stats


# ===========================================================================
# CHẠY TRỰC TIẾP: hiển thị thống kê
# ===========================================================================
if __name__ == "__main__":
    stats = get_stats()
    print(f"\n{'=' * 50}")
    print(f"  📊 THỐNG KÊ ACTIVITY TEMPLATES")
    print(f"{'=' * 50}")
    print(f"  Tổng locations: {stats['total_locations']}")
    print(f"  Tổng activities: {stats['total_activities']}")
    print()
    
    for loc_name, detail in stats["locations_detail"].items():
        print(f"  📍 {loc_name}: {detail['activity_count']} activities")
        print(f"     Tags: {', '.join(detail['tags'][:8])}...")
    print()
