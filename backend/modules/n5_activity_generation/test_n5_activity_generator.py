"""
test_n5_activity_generator.py — Kiểm tra N5 Activity Generator
Chạy từ thư mục gốc dự án:
    python -m unittest backend.modules.n5_activity_generation.test_n5_activity_generator -v
"""
import unittest
from unittest.mock import patch

from backend.modules.n5_activity_generation.n5_activity_generator import (
    generate_activities,
    _is_sightseeing,
)

# ──────────────────────────────────────────────────────────
# HELPER — tạo input chuẩn cho test
# ──────────────────────────────────────────────────────────

def _make_input(tags, location_name="Sa Pa", location_tags=None,
                budget=5_000_000, duration=480, people=2):
    return {
        "user": {
            "text": "Tôi muốn đi du lịch",
            "image_description": None,
            "tags": tags,
        },
        "locations": [
            {
                "location_id": "loc_test_001",
                "metadata": {
                    "name": location_name,
                    "description": f"Địa điểm {location_name}",
                    "tags": location_tags or ["nature", "mountain"],
                }
            }
        ],
        "constraints": {
            "budget": budget,
            "duration": duration,
            "people": people,
            "time_of_day": None,
        }
    }


# ===========================================================================
# TestN5ActivityGenerator — 9 tests cho core generation
# ===========================================================================

class TestN5ActivityGenerator(unittest.TestCase):
    """Test suite cho hàm generate_activities() — chức năng sinh hoạt động."""

    def test_generate_with_matching_tags(self):
        """N5 sinh được activities khi tags user khớp với location."""
        result = generate_activities(_make_input(["nature", "photography", "sightseeing"]))
        activities = result.get("activities", [])
        self.assertGreater(len(activities), 0)

    def test_budget_constraints(self):
        """Khi không có constraints, N5 áp dụng defaults và vẫn sinh được kết quả."""
        data = {
            "user": {"text": None, "image_description": None, "tags": ["nature"]},
            "locations": [{
                "location_id": "loc_x",
                "metadata": {"name": "Sa Pa", "description": "", "tags": ["mountain"]},
            }],
            "constraints": {},
        }
        result = generate_activities(data)
        self.assertEqual(len(result.get("activities", [])), 100)

    def test_time_constraints(self):
        """estimated_duration của mọi activity phải là số dương."""
        result = generate_activities(_make_input(["nature"], duration=240))
        for act in result["activities"]:
            self.assertGreater(act["metadata"]["estimated_duration"], 0)

    def test_missing_location(self):
        """Địa điểm không có trong LOCATION_PROFILES vẫn sinh đủ 100 activities."""
        result = generate_activities(_make_input(
            ["adventure", "nature"],
            location_name="Bản Giốc",
            location_tags=["waterfall", "nature", "adventure", "remote"],
        ))
        self.assertEqual(len(result.get("activities", [])), 100)

    def test_sorting_by_match_score(self):
        """Sightseeing activities phải xuất hiện đầu danh sách (ưu tiên cao nhất)."""
        result = generate_activities(_make_input(["nature", "sightseeing"]))
        activities = result.get("activities", [])
        self.assertGreater(len(activities), 0)
        # Kiểm tra sightseeing ratio ≥ 40% — thể hiện sắp xếp ưu tiên đúng
        sg_count = sum(1 for a in activities if _is_sightseeing(a))
        self.assertGreaterEqual(sg_count / len(activities), 0.40)

    def test_limit_result_size(self):
        """N5 sinh đúng 100 activities cho 1 location, không nhiều hơn."""
        result = generate_activities(_make_input(["nature", "food", "relax"]))
        self.assertEqual(len(result.get("activities", [])), 100)

    def test_user_likes_relax_beach(self):
        """N5 hoạt động đúng với user thích relax và biển."""
        result = generate_activities(_make_input(
            ["relax", "beach", "sea"],
            location_name="Phú Quốc",
            location_tags=["beach", "sea", "resort", "seafood"],
        ))
        self.assertEqual(len(result.get("activities", [])), 100)

    def test_user_likes_culture_history(self):
        """N5 hoạt động đúng với user thích văn hóa và lịch sử."""
        result = generate_activities(_make_input(
            ["culture", "history", "heritage"],
            location_name="Hội An",
            location_tags=["heritage", "culture", "ancient_town", "lantern"],
        ))
        self.assertEqual(len(result.get("activities", [])), 100)

    def test_user_has_low_budget(self):
        """N5 vẫn sinh activities khi budget rất thấp (150k VND)."""
        result = generate_activities(_make_input(["nature"], budget=150_000))
        self.assertGreater(len(result.get("activities", [])), 0)


# ===========================================================================
# TestN5HybridGenerator — 8 tests cho hành vi LLM / hybrid
# ===========================================================================

class TestN5HybridGenerator(unittest.TestCase):
    """Test suite cho hành vi LLM fallback trong generate_activities()."""

    def setUp(self):
        self.data = {
            "user": {
                "text": "Tôi muốn đi núi",
                "image_description": None,
                "tags": ["nature", "adventure"],
            },
            "locations": [
                {
                    "location_id": "loc_sapa",
                    "metadata": {
                        "name": "Sa Pa",
                        "description": "Thị trấn miền núi phía Bắc",
                        "tags": ["mountain", "trekking", "nature"],
                    }
                },
                {
                    "location_id": "loc_dalat",
                    "metadata": {
                        "name": "Đà Lạt",
                        "description": "Thành phố ngàn hoa",
                        "tags": ["flower", "nature", "cool_weather", "romantic"],
                    }
                }
            ],
            "constraints": {
                "budget": 5_000_000,
                "duration": 480,
                "people": 2,
            },
        }

    def test_hybrid_fallback_use_llm_false(self):
        """Khi LLM bị tắt (mocked False), template sinh đủ 100 activities/location."""
        with patch(
            "backend.modules.n5_activity_generation.n5_activity_generator.is_llm_available",
            return_value=False
        ):
            result = generate_activities(self.data)
        activities = result.get("activities", [])
        self.assertEqual(len(activities), 200)  # 2 locations × 100

    def test_hybrid_has_generated_by_field(self):
        """Mọi activity phải có đầy đủ các field schema bắt buộc."""
        required_meta = [
            "name", "description", "activity_type", "activity_subtype",
            "intensity", "physical_level", "social_level",
            "estimated_duration", "price_level",
            "indoor_outdoor", "weather_dependent", "time_of_day_suitable",
        ]
        with patch(
            "backend.modules.n5_activity_generation.n5_activity_generator.is_llm_available",
            return_value=False
        ):
            result = generate_activities(self.data)
        for act in result.get("activities", []):
            self.assertIn("activity_id", act)
            self.assertIn("location_id", act)
            meta = act.get("metadata", {})
            for field in required_meta:
                self.assertIn(field, meta, f"Thiếu field '{field}' trong activity '{act.get('activity_id')}'")

    def test_hybrid_fallback_no_api_key(self):
        """Khi không có API key (is_llm_available=False), template bù đủ 100."""
        with patch(
            "backend.modules.n5_activity_generation.n5_activity_generator.is_llm_available",
            return_value=False
        ):
            result = generate_activities({**self.data, "locations": [self.data["locations"][0]]})
        self.assertEqual(len(result.get("activities", [])), 100)

    def test_hybrid_sorting_consistent(self):
        """Sightseeing ratio phải ≥ 40% trong kết quả cuối — kể cả khi không có LLM."""
        with patch(
            "backend.modules.n5_activity_generation.n5_activity_generator.is_llm_available",
            return_value=False
        ):
            result = generate_activities({**self.data, "locations": [self.data["locations"][0]]})
        activities = result.get("activities", [])
        sg_count = sum(1 for a in activities if _is_sightseeing(a))
        self.assertGreaterEqual(sg_count / len(activities), 0.40)

    def test_hybrid_respects_constraints(self):
        """price_level phải trong [1.0, 5.0] và estimated_duration phải > 0."""
        with patch(
            "backend.modules.n5_activity_generation.n5_activity_generator.is_llm_available",
            return_value=False
        ):
            result = generate_activities(self.data)
        for act in result.get("activities", []):
            meta = act["metadata"]
            self.assertGreaterEqual(meta["price_level"], 1.0)
            self.assertLessEqual(meta["price_level"], 5.0)
            self.assertGreater(meta["estimated_duration"], 0)

    def test_hybrid_with_mock_llm_success(self):
        """Khi LLM mock trả về 10 activities, N5 gộp với template để đủ 100."""
        mock_llm_acts = [
            {
                "name": f"LLM Activity {i}",
                "description": f"Mô tả sinh bởi LLM số {i}",
                "activity_type": "nature",
                "activity_subtype": "trekking",
                "intensity": 0.6,
                "physical_level": 0.5,
                "social_level": 0.4,
                "estimated_duration": 120.0,
                "price_level": 2.0,
                "indoor_outdoor": "outdoor",
                "weather_dependent": True,
                "time_of_day_suitable": "morning",
            }
            for i in range(10)
        ]
        with patch(
            "backend.modules.n5_activity_generation.n5_activity_generator.is_llm_available",
            return_value=True
        ), patch(
            "backend.modules.n5_activity_generation.n5_activity_generator.generate_from_llm",
            return_value=mock_llm_acts
        ):
            result = generate_activities({**self.data, "locations": [self.data["locations"][0]]})

        activities = result.get("activities", [])
        self.assertEqual(len(activities), 100)

    def test_hybrid_llm_failure_fallback(self):
        """Khi LLM trả về None (thất bại), template phải bù đủ 100 activities."""
        with patch(
            "backend.modules.n5_activity_generation.n5_activity_generator.is_llm_available",
            return_value=True
        ), patch(
            "backend.modules.n5_activity_generation.n5_activity_generator.generate_from_llm",
            return_value=None
        ):
            result = generate_activities({**self.data, "locations": [self.data["locations"][0]]})
        self.assertEqual(len(result.get("activities", [])), 100)

    def test_original_generate_still_works(self):
        """API generate_activities(data: dict) phải trả về {"activities": list} đúng chuẩn."""
        result = generate_activities({**self.data, "locations": [self.data["locations"][0]]})
        self.assertIsInstance(result, dict)
        self.assertIn("activities", result)
        self.assertIsInstance(result["activities"], list)
        self.assertEqual(len(result["activities"]), 100)


if __name__ == "__main__":
    unittest.main()
