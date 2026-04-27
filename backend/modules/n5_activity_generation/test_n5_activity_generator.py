"""
test_n5_activity_generator.py — Kiểm tra N5 Activity Generator
Chạy từ root project: python -m backend.modules.n5_activity_generation.test_n5_activity_generator
"""
import sys, json

from backend.modules.n5_activity_generation.n5_activity_generator import (
    generate_activities,
    _is_sightseeing,
)


# ──────────────────────────────────────────────────────────
# SAMPLE INPUT từ N4
# ──────────────────────────────────────────────────────────
SAMPLE_INPUT_SINGLE = {
    "user": {
        "text": "Tôi muốn đi nơi thiên nhiên, ngắm cảnh đẹp, chụp ảnh",
        "image_description": None,
        "tags": ["nature", "photography", "sightseeing", "relax"],
    },
    "locations": [
        {
            "location_id": "loc_sapa_001",
            "metadata": {
                "name": "Sa Pa",
                "description": "Thị trấn vùng cao Lào Cai với ruộng bậc thang",
                "tags": ["mountain", "trekking", "nature", "cool_weather", "photography"],
            }
        }
    ],
    "constraints": {
        "budget": 5_000_000,
        "duration": 3,
        "people": 2,
        "time_of_day": "morning",
    }
}

SAMPLE_INPUT_MULTI = {
    "user": {
        "text": "Gia đình 4 người, thích biển và ẩm thực",
        "image_description": None,
        "tags": ["beach", "food", "relax", "family"],
    },
    "locations": [
        {
            "location_id": "loc_pq_001",
            "metadata": {
                "name": "Phú Quốc",
                "description": "Đảo ngọc phía Nam",
                "tags": ["beach", "sea", "resort", "seafood"],
            }
        },
        {
            "location_id": "loc_nt_001",
            "metadata": {
                "name": "Nha Trang",
                "description": "Thành phố biển năng động",
                "tags": ["beach", "sea", "entertainment", "seafood"],
            }
        }
    ],
    "constraints": {
        "budget": 8_000_000,
        "duration": 5,
        "people": 4,
        "time_of_day": None,
    }
}

SAMPLE_INPUT_UNKNOWN_LOCATION = {
    "user": {
        "text": "Muốn khám phá nơi mới",
        "image_description": None,
        "tags": ["adventure", "nature"],
    },
    "locations": [
        {
            "location_id": "loc_unknown_xyz",
            "metadata": {
                "name": "Bản Giốc",
                "description": "Thác nước hùng vĩ ở Cao Bằng",
                "tags": ["waterfall", "nature", "adventure", "remote"],
            }
        }
    ],
    "constraints": {
        "budget": 3_000_000,
        "duration": 2,
        "people": 2,
        "time_of_day": None,
    }
}


def run_test(name: str, input_data: dict):
    print(f"\n{'='*60}")
    print(f"  TEST: {name}")
    print(f"{'='*60}")

    result = generate_activities(input_data)
    activities = result.get("activities", [])

    print(f"\n  Total activities generated: {len(activities)}")

    # Per-location breakdown
    loc_counts = {}
    type_counts = {}
    sightseeing_count = 0

    for act in activities:
        loc = act.get("location_id", "?")
        loc_counts[loc] = loc_counts.get(loc, 0) + 1

class TestN5HybridGenerator(unittest.TestCase):
    """
    Test suite cho hàm generate_activities_hybrid().
    """

    def setUp(self):
        """Chuẩn bị dữ liệu chung cho các test hybrid"""
        self.user_tags = ["nature", "adventure"]
        self.locations = [
            {"name": "Sa Pa", "location_id": "loc_sapa"},
            {"name": "Đà Lạt", "location_id": "loc_dalat"}
        ]
        self.constraints = {
            "budget": 5_000_000,
            "max_time_per_day": 480
        }

    def test_hybrid_fallback_use_llm_false(self):
        """Khi use_llm=False, hybrid phải dùng rule-based và trả kết quả 'template'."""
        result = generate_activities_hybrid(
            self.user_tags, self.locations, self.constraints, use_llm=False
        )
        
        self.assertTrue(len(result) > 0)
        for act in result:
            self.assertEqual(act.get("generated_by"), "template")

    def test_hybrid_has_generated_by_field(self):
        """Mọi activity từ hybrid đều phải có trường generated_by."""
        result = generate_activities_hybrid(
            self.user_tags, self.locations, self.constraints, use_llm=False
        )
        
        for act in result:
            self.assertIn("generated_by", act)
            self.assertIn(act["generated_by"], ["llm", "template"])

    def test_hybrid_fallback_no_api_key(self):
        """Khi không có API key, hybrid phải fallback về template dù use_llm=True."""
        with patch("backend.modules.n5_activity_generation.n5_activity_generator._is_llm_available", 
                   return_value=False):
            result = generate_activities_hybrid(
                self.user_tags, self.locations, self.constraints, use_llm=True
            )
        
        self.assertTrue(len(result) > 0)
        for act in result:
            self.assertEqual(act.get("generated_by"), "template")

    def test_hybrid_sorting_consistent(self):
        """Kết quả hybrid phải được sắp xếp theo match_score giảm dần."""
        result = generate_activities_hybrid(
            self.user_tags, self.locations, self.constraints, use_llm=False
        )
        
        scores = [act.get("match_score", 0) for act in result]
        self.assertEqual(scores, sorted(scores, reverse=True))

    def test_hybrid_respects_constraints(self):
        """Hybrid phải tuân thủ constraints dù dùng template hay LLM."""
        constraints = {
            "budget": 300_000,
            "max_time_per_day": 120,
        }
        result = generate_activities_hybrid(
            ["adventure", "nature"], self.locations, constraints, use_llm=False
        )
        
        for act in result:
            self.assertLessEqual(act.get("cost", 0), 300_000 * 0.4)   # cho phép margin
            self.assertLessEqual(act.get("estimated_time_minutes", 0), 120)

    def test_hybrid_with_mock_llm_success(self):
        """Test hybrid với mock LLM thành công (phiên bản ổn định)."""
        mock_llm_activities = [
            {
                "activity_id": "mock_llm_001",
                "location_id": "loc_sapa",
                "name": "Trekking ruộng bậc thang Sa Pa",
                "description": "Trải nghiệm trekking nhẹ nhàng ngắm ruộng bậc thang vào buổi sáng.",
                "tags": ["trekking", "nature", "photography"],
                "cost": 280000,
                "estimated_duration": 210,          # hoặc estimated_time_minutes tùy code của bạn
                "best_time": ["morning"],
                "suitable_for": ["couple", "group_small"],
                "difficulty": "medium",
                "season": ["sep", "oct"],
                "reason_template": "Phù hợp với người thích thiên nhiên",
                "generated_by": "llm",
                "match_score": 0.92
            }
        ]

        # Giả sử hàm hybrid gọi llm_generator.generate_activities
        with patch("backend.modules.n5_activity_generation.n5_activity_generator.generate_activities_from_llm", 
                   return_value=mock_llm_activities):
            
            result = generate_activities_hybrid(
                self.user_tags, self.locations, self.constraints, use_llm=True
            )

        self.assertIsInstance(result, list)
        self.assertGreater(len(result), 0, 
            "Hybrid phải trả về ít nhất 1 activity khi mock LLM thành công")

        if result:
            first = result[0]
            self.assertIn("generated_by", first)
            self.assertIn("match_score", first)
            self.assertIn("reason_template", first)

    def test_hybrid_llm_failure_fallback(self):
        """Khi LLM thất bại, hybrid phải fallback về template."""
        with patch("backend.modules.n5_activity_generation.n5_activity_generator.generate_activities_from_llm", 
                   return_value=None):
            
            result = generate_activities_hybrid(
                self.user_tags, self.locations, self.constraints, use_llm=True
            )
        
        self.assertTrue(len(result) > 0)
        for act in result:
            self.assertEqual(act.get("generated_by"), "template")

    def test_original_generate_still_works(self):
        """Hàm generate_activities gốc phải vẫn hoạt động bình thường."""
        result = generate_activities(self.user_tags, self.locations, self.constraints)
        self.assertTrue(len(result) > 0)
        for act in result:
            self.assertEqual(act.get("generated_by"), "template")


if __name__ == '__main__':
    unittest.main()
