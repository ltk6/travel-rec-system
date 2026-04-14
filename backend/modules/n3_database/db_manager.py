import os
import logging
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv
from pymongo import MongoClient

# Cấu hình logging giống N5
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
DB_NAME = "smart_tourism_db"

client: Optional[MongoClient] = None
db: Any = None

def _get_db():
    global client, db
    if db is None:
        try:
            # Timeout 3s để tránh treo máy nếu không có kết nối
            client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=3000)
            db = client[DB_NAME]
            client.admin.command('ping')
            logger.info(f"✅ N3: Đã kết nối Database tại {'Cloud' if '@' in MONGO_URI else 'Localhost'}")
        except Exception as e:
            logger.warning(f"⚠️ N3: Cảnh báo - Không thể kết nối DB. Hệ thống sẽ chạy fallback rỗng. Lỗi: {e}")
            db = None
    return db

def save_user_profile(user_data: Dict[str, Any]) -> Dict[str, Any]:
    """Lưu profile người dùng kèm vector từ N1."""
    database = _get_db()
    if database is None: return {"status": "error", "message": "DB Offline"}
    try:
        res = database.users.insert_one(user_data)
        return {"status": "success", "inserted_id": str(res.inserted_id)}
    except Exception as e:
        logger.error(f"Lỗi lưu User: {e}")
        return {"status": "error", "message": str(e)}

def save_location(location_data: Dict[str, Any]) -> Dict[str, Any]:
    """Lưu địa điểm du lịch mới."""
    database = _get_db()
    if database is None: return {"status": "error", "message": "DB Offline"}
    try:
        res = database.locations.insert_one(location_data)
        return {"status": "success", "inserted_id": str(res.inserted_id)}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def filter_locations(budget: float, duration: int) -> List[Dict[str, Any]]:
    """Lọc nhanh địa điểm theo ngân sách và thời gian (Pre-filtering cho N4)."""
    database = _get_db()
    if database is None: return []
    try:
        query = {
            "metadata.price_level": {"$lte": budget},
            "metadata.estimated_duration": {"$lte": duration}
        }
        return list(database.locations.find(query, {"_id": 0}))
    except Exception as e:
        logger.error(f"Lỗi truy vấn: {e}")
        return []

def get_all_locations() -> List[Dict[str, Any]]:
    database = _get_db()
    return list(database.locations.find({}, {"_id": 0})) if database else []