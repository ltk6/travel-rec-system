import os
import json
import logging
from typing import List, Dict, Any

from dotenv import load_dotenv
import psycopg2
from psycopg2.extras import RealDictCursor

load_dotenv()

PG_URI = os.getenv(
    "PG_URI",
    "postgresql://localhost:5432/smart_tourism_db"
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# ─────────────────────────────────────────────
# CONNECTION
# ─────────────────────────────────────────────

def _get_connection():
    return psycopg2.connect(
        PG_URI,
        cursor_factory=RealDictCursor
    )


# ─────────────────────────────────────────────
# INIT DB (NEW SCHEMA)
# ─────────────────────────────────────────────

def init_db():
    conn = _get_connection()
    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute("DROP TABLE IF EXISTS locations;")

                cur.execute("""
                    CREATE TABLE locations (
                        location_id VARCHAR(255) PRIMARY KEY,
                        vectors JSONB NOT NULL,
                        metadata JSONB NOT NULL,
                        geo JSONB NOT NULL
                    );
                """)
    finally:
        conn.close()


# ─────────────────────────────────────────────
# SAVE LOCATION (UPDATED)
# ─────────────────────────────────────────────

import os
import json
import logging
from typing import List, Dict, Any

from dotenv import load_dotenv
import psycopg2
from psycopg2.extras import RealDictCursor

load_dotenv()

PG_URI = os.getenv(
    "PG_URI",
    "postgresql://localhost:5432/smart_tourism_db"
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# ─────────────────────────────────────────────
# CONNECTION
# ─────────────────────────────────────────────

def _get_connection():
    return psycopg2.connect(
        PG_URI,
        cursor_factory=RealDictCursor
    )


# ─────────────────────────────────────────────
# INIT DB
# ─────────────────────────────────────────────

def init_db():
    conn = _get_connection()
    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute("DROP TABLE IF EXISTS users;")
                cur.execute("DROP TABLE IF EXISTS locations;")

                cur.execute("""
                    CREATE TABLE locations (
                        location_id VARCHAR(255) PRIMARY KEY,
                        vectors JSONB NOT NULL,
                        metadata JSONB NOT NULL,
                        geo JSONB NOT NULL
                    );
                """)
    finally:
        conn.close()


# ─────────────────────────────────────────────
# SAVE LOCATION
# ─────────────────────────────────────────────

def save_location(location_data: Dict[str, Any]) -> Dict[str, Any]:
    conn = _get_connection()
    try:
        with conn:
            with conn.cursor() as cur:

                cur.execute("""
                    INSERT INTO locations (location_id, vectors, metadata, geo)
                    VALUES (%s, %s, %s, %s)
                    ON CONFLICT (location_id)
                    DO UPDATE SET
                        vectors = EXCLUDED.vectors,
                        metadata = EXCLUDED.metadata,
                        geo = EXCLUDED.geo;
                """, (
                    location_data["location_id"],
                    json.dumps(location_data.get("vectors", {})),
                    json.dumps(location_data.get("metadata", {})),
                    json.dumps(location_data.get("geo", {}))
                ))

        return {"status": "success"}

    except Exception as e:
        logger.error(f"Location save error: {e}")
        return {"status": "error", "message": str(e)}

    finally:
        conn.close()


# ─────────────────────────────────────────────
# GET ALL LOCATIONS
# ─────────────────────────────────────────────

def get_all_locations() -> List[Dict[str, Any]]:
    conn = _get_connection()
    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT location_id, vectors, metadata, geo
                    FROM locations;
                """)

                rows = cur.fetchall()

                # IMPORTANT: psycopg2 returns JSONB already parsed as dict
                # (because of RealDictCursor), but still safe to ensure structure

                return [
                    {
                        "location_id": r["location_id"],
                        "vectors": r["vectors"],
                        "metadata": r["metadata"],
                        "geo": r["geo"]
                    }
                    for r in rows
                ]

    except Exception as e:
        logger.error(f"Fetch error: {e}")
        return []

    finally:
        conn.close()


# ─────────────────────────────────────────────
# DEBUG
# ─────────────────────────────────────────────

if __name__ == "__main__":
    init_db()
    print("DB initialized with MULTI-VECTOR schema")


# ─────────────────────────────────────────────
# GET ALL LOCATIONS
# ─────────────────────────────────────────────

def get_all_locations() -> List[Dict[str, Any]]:
    conn = _get_connection()
    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT location_id, vectors, metadata, geo
                    FROM locations;
                """)

                rows = cur.fetchall()

                # IMPORTANT: psycopg2 returns JSONB already parsed as dict
                # (because of RealDictCursor), but still safe to ensure structure

                return [
                    {
                        "location_id": r["location_id"],
                        "vectors": r["vectors"],
                        "metadata": r["metadata"],
                        "geo": r["geo"]
                    }
                    for r in rows
                ]

    except Exception as e:
        logger.error(f"Fetch error: {e}")
        return []

    finally:
        conn.close()


# ─────────────────────────────────────────────
# OPTIONAL DEBUG ENTRY
# ─────────────────────────────────────────────

if __name__ == "__main__":
    init_db()
    print("DB initialized with MULTI-VECTOR schema")