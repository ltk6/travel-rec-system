import unittest
from unittest.mock import patch, MagicMock
from backend.modules.n5_activity_generation.n5_activity_generator import generate_activities, generate_activities_hybrid
from backend.modules.n5_activity_generation.n5_activity_templates import ACTIVITY_TEMPLATES

class TestN5ActivityGenerator(unittest.TestCase):
    # ======== CÁC TEST CASES TRƯỚC ĐÓ ========
    def test_generate_with_matching_tags(self):
        user_tags = ["beach", "sea"]
        locations = [{"name": "Phú Quốc"}, {"name": "Hạ Long"}]
        constraints = {"budget": 10000000, "max_time_per_day": 480}
        
        result = generate_activities(user_tags, locations, constraints)
        self.assertTrue(len(result) > 0)
        
        # Verify the highest score activity has relevant tags
        top_activity = result[0]
        self.assertTrue(top_activity["match_score"] > 0)
        self.assertTrue(any(tag in top_activity["tags"] for tag in user_tags))

    def test_budget_constraints(self):
        user_tags = ["culture"]
        locations = [{"name": "Hội An"}]
        constraints = {"budget": 100000, "max_time_per_day": 480}
        
        result = generate_activities(user_tags, locations, constraints)
        for act in result:
            self.assertTrue(act["cost"] <= 50000)

    def test_time_constraints(self):
        user_tags = ["relax"]
        locations = [{"name": "Đà Lạt"}]
        constraints = {"budget": 1000000, "max_time_per_day": 60}
        
        result = generate_activities(user_tags, locations, constraints)
        for act in result:
            self.assertTrue(act["estimated_time_minutes"] <= 60)

    def test_missing_location(self):
        user_tags = ["relax"]
        locations = [{"name": "Not Exist City"}, {"name": "Đà Lạt"}]
        constraints = {"budget": 1000000, "max_time_per_day": 400}
        
        result = generate_activities(user_tags, locations, constraints)
        for act in result:
            self.assertEqual(act["location_name"], "Đà Lạt")

    def test_sorting_by_match_score(self):
        user_tags = ["relax", "photography"]
        locations = [{"name": "Đà Lạt"}, {"name": "Phú Quốc"}]
        constraints = {"budget": 1000000, "max_time_per_day": 400}
        
        result = generate_activities(user_tags, locations, constraints)
        
        scores = [act["match_score"] for act in result]
        self.assertEqual(scores, sorted(scores, reverse=True))

    def test_limit_result_size(self):
        user_tags = ["culture", "relax", "food", "nature", "history", "photography", "adventure", "fun"]
        locations = [
            {"name": "Hội An"}, {"name": "Sa Pa"}, {"name": "Hạ Long"}, 
            {"name": "Huế"}, {"name": "Đà Lạt"}
        ]
        constraints = {"budget": 100000000, "max_time_per_day": 1000}
        result = generate_activities(user_tags, locations, constraints)
        self.assertTrue(len(result) <= 12)

    # ======== 3 TEST CASES MỚI THEO YÊU CẦU ========
    
    def test_user_likes_relax_beach(self):
        """Test case 1: User thích relax + beach"""
        user_tags = ["relax", "beach"]
        locations = [{"name": "Phú Quốc"}, {"name": "Hội An"}, {"name": "Hạ Long"}]
        constraints = {"budget": 10000000, "max_time_per_day": 480}
        
        result = generate_activities(user_tags, locations, constraints)
        self.assertTrue(len(result) > 0)
        
        # Mọi activity trả về nếu có score > 0 thì phải có tag relax hoặc beach
        top_activity = result[0]
        self.assertTrue("relax" in top_activity["tags"] or "beach" in top_activity["tags"])
        
    def test_user_likes_culture_history(self):
        """Test case 2: User thích culture + history"""
        user_tags = ["culture", "history"]
        locations = [{"name": "Huế"}, {"name": "Hội An"}, {"name": "Sa Pa"}]
        constraints = {"budget": 10000000, "max_time_per_day": 480}
        
        result = generate_activities(user_tags, locations, constraints)
        self.assertTrue(len(result) > 0)
        
        # Top 3 (phần lớn) nên thuộc các activity văn hoá lịch sử (vì điểm cao hơn được sếp hạng)
        for idx in range(min(3, len(result))):
            act = result[idx]
            self.assertTrue("culture" in act["tags"] or "history" in act["tags"])

    def test_user_has_low_budget(self):
        """Test case 3: User có ngân sách thấp"""
        user_tags = ["relax", "nature", "adventure"]
        locations = [{"name": "Sa Pa"}, {"name": "Nha Trang"}, {"name": "Huế"}]
        
        # Ngân sách tổng là 150_000 => limit activity = 75_000
        constraints = {"budget": 150000, "max_time_per_day": 480}
        
        result = generate_activities(user_tags, locations, constraints)
        
        for act in result:
            self.assertTrue(act["cost"] <= 75000)
            
        # Kiểm tra xem các module lớn có bị lọc đi không (VD: VinWonders 800k)
        names = [act["name"] for act in result]
        self.assertNotIn("Chơi VinWonders", names)
        self.assertNotIn("Trekking Fansipan", names)


# ======== TEST CASES CHO HYBRID APPROACH ========

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