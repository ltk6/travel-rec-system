import os
import json
import logging
from typing import List, Dict, Any
from dotenv import load_dotenv
import psycopg2
from psycopg2.extras import RealDictCursor
from pgvector.psycopg2 import register_vector

# Cấu hình logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()
PG_URI = os.getenv("PG_URI", "postgresql://localhost:5432/smart_tourism_db")

def _get_connection():
    """Thiết lập kết nối tới PostgreSQL và đăng ký extension pgvector."""
    conn = psycopg2.connect(PG_URI, cursor_factory=RealDictCursor)
    conn.autocommit = True
    
    # SỬA LỖI Ở ĐÂY: Phải cài extension vector VÀO DB TRƯỚC khi register
    cur = conn.cursor()
    cur.execute("CREATE EXTENSION IF NOT EXISTS vector;")
    cur.close()
    
    # Sau khi cài xong mới cho phép psycopg2 nhận dạng
    register_vector(conn)
    return conn

def init_db():
    """Khởi tạo cấu trúc bảng nếu chưa tồn tại."""
    conn = _get_connection()
    cur = conn.cursor()
    # Tạo bảng Users
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id VARCHAR(255) PRIMARY KEY,
            vector vector(5),
            metadata JSONB,
            constraints JSONB
        );
    """)
    # Tạo bảng Locations
    cur.execute("""
        CREATE TABLE IF NOT EXISTS locations (
            location_id VARCHAR(255) PRIMARY KEY,
            vector vector(5),
            metadata JSONB,
            geo JSONB
        );
    """)
    logger.info("✅ N3: Đã khởi tạo cấu trúc Database PostgreSQL.")
    cur.close()
    conn.close()

def save_user_profile(user_data: Dict[str, Any]) -> Dict[str, Any]:
    """Lưu profile người dùng vào PostgreSQL."""
    try:
        conn = _get_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO users (user_id, vector, metadata, constraints) VALUES (%s, %s, %s, %s) ON CONFLICT (user_id) DO UPDATE SET vector = EXCLUDED.vector, metadata = EXCLUDED.metadata, constraints = EXCLUDED.constraints;",
            (user_data.get("user_id"), user_data.get("vector"), json.dumps(user_data.get("metadata", {})), json.dumps(user_data.get("constraints", {})))
        )
        conn.close()
        return {"status": "success", "user_id": user_data.get("user_id")}
    except Exception as e:
        logger.error(f"Lỗi lưu User: {e}")
        return {"status": "error", "message": str(e)}

def save_location(location_data: Dict[str, Any]) -> Dict[str, Any]:
    """Lưu thông tin địa điểm vào PostgreSQL."""
    try:
        conn = _get_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO locations (location_id, vector, metadata, geo) VALUES (%s, %s, %s, %s) ON CONFLICT (location_id) DO UPDATE SET vector = EXCLUDED.vector, metadata = EXCLUDED.metadata, geo = EXCLUDED.geo;",
            (location_data.get("location_id"), location_data.get("vector"), json.dumps(location_data.get("metadata", {})), json.dumps(location_data.get("geo", {})))
        )
        conn.close()
        return {"status": "success", "location_id": location_data.get("location_id")}
    except Exception as e:
        logger.error(f"Lỗi lưu Location: {e}")
        return {"status": "error", "message": str(e)}

def filter_locations(budget: float, duration: int) -> List[Dict[str, Any]]:
    """Truy vấn lọc địa điểm theo ngân sách và thời gian (Pre-filtering)."""
    try:
        conn = _get_connection()
        cur = conn.cursor()
        # Lọc dữ liệu dựa trên các trường trong JSONB metadata
        cur.execute(
            "SELECT location_id, vector::text, metadata, geo FROM locations WHERE (metadata->>'price_level')::numeric <= %s AND (metadata->>'estimated_duration')::numeric <= %s;",
            (budget, duration)
        )
        rows = cur.fetchall()
        conn.close()
        
        # Chuyển đổi chuỗi vector từ DB về lại dạng list float cho Python
        for row in rows:
            if row['vector']:
                row['vector'] = [float(x) for x in row['vector'].strip('[]').split(',')]
        return rows
    except Exception as e:
        logger.error(f"Lỗi truy vấn: {e}")
        return []

def get_all_locations() -> List[Dict[str, Any]]:
    """Lấy toàn bộ danh sách địa điểm."""
    try:
        conn = _get_connection()
        cur = conn.cursor()
        cur.execute("SELECT location_id, vector::text, metadata, geo FROM locations;")
        rows = cur.fetchall()
        conn.close()
        for row in rows:
            if row['vector']:
                row['vector'] = [float(x) for x in row['vector'].strip('[]').split(',')]
        return rows
    except Exception as e:
        return []