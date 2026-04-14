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
    
    Kiểm tra các kịch bản:
      - Fallback về rule-based khi use_llm=False
      - Trường generated_by có mặt trong output
      - Hybrid hoạt động đúng khi LLM không khả dụng
      - Post-processing LLM activities tuân thủ constraints
    """
    
    def test_hybrid_fallback_use_llm_false(self):
        """Khi use_llm=False, hybrid phải dùng rule-based và trả kết quả 'template'."""
        user_tags = ["nature", "adventure"]
        locations = [{"name": "Sa Pa"}, {"name": "Đà Lạt"}]
        constraints = {"budget": 5_000_000, "max_time_per_day": 480}
        
        result = generate_activities_hybrid(
            user_tags, locations, constraints, use_llm=False
        )
        
        self.assertTrue(len(result) > 0)
        # Tất cả phải được đánh dấu là template vì use_llm=False
        for act in result:
            self.assertEqual(act["generated_by"], "template")
    
    def test_hybrid_has_generated_by_field(self):
        """Mọi activity từ hybrid đều phải có trường generated_by."""
        user_tags = ["food", "culture"]
        locations = [{"name": "Huế"}, {"name": "Hội An"}]
        constraints = {"budget": 10_000_000, "max_time_per_day": 480}
        
        result = generate_activities_hybrid(
            user_tags, locations, constraints, use_llm=False
        )
        
        for act in result:
            self.assertIn("generated_by", act)
            self.assertIn(act["generated_by"], ["llm", "template"])
    
    def test_hybrid_fallback_no_api_key(self):
        """Khi không có API key, hybrid phải fallback về template dù use_llm=True."""
        user_tags = ["relax", "beach"]
        locations = [{"name": "Phú Quốc"}]
        constraints = {"budget": 5_000_000, "max_time_per_day": 480}
        
        # Mock: giả lập không có API key
        with patch("n5_activity_generator._is_llm_available", return_value=False):
            result = generate_activities_hybrid(
                user_tags, locations, constraints, use_llm=True
            )
        
        self.assertTrue(len(result) > 0)
        for act in result:
            self.assertEqual(act["generated_by"], "template")
    
    def test_hybrid_sorting_consistent(self):
        """Kết quả hybrid phải được sắp xếp theo match_score giảm dần."""
        user_tags = ["culture", "nature", "food"]
        locations = [
            {"name": "Huế"}, {"name": "Sa Pa"}, {"name": "Hội An"}
        ]
        constraints = {"budget": 10_000_000, "max_time_per_day": 480}
        
        result = generate_activities_hybrid(
            user_tags, locations, constraints, use_llm=False
        )
        
        scores = [act["match_score"] for act in result]
        self.assertEqual(scores, sorted(scores, reverse=True))
    
    def test_hybrid_respects_constraints(self):
        """Hybrid phải tuân thủ constraints dù dùng template hay LLM."""
        user_tags = ["adventure", "nature"]
        locations = [{"name": "Nha Trang"}, {"name": "Hạ Long"}]
        constraints = {
            "budget": 300_000,
            "max_time_per_day": 120,
            "exclude_tags": ["fun"],
        }
        
        result = generate_activities_hybrid(
            user_tags, locations, constraints, use_llm=False
        )
        
        max_cost = 300_000 * 0.30  # 90,000
        for act in result:
            self.assertLessEqual(act["cost"], max_cost)
            self.assertLessEqual(act["estimated_time_minutes"], 120)
            self.assertNotIn("fun", act["tags"])
    
    def test_hybrid_with_mock_llm_success(self):
        """Giả lập LLM trả về thành công → activities phải có generated_by='llm'."""
        # Dữ liệu giả từ LLM
        mock_llm_result = [
            {
                "name": "Ngắm cánh đồng muối",
                "desc": "Trải nghiệm tham quan cánh đồng muối truyền thống",
                "cost": 50000,
                "time": 90,
                "tags": ["nature", "culture"],
            },
            {
                "name": "Ăn bánh căn",
                "desc": "Thưởng thức bánh căn - đặc sản Ninh Thuận",
                "cost": 30000,
                "time": 45,
                "tags": ["food"],
            },
        ]
        
        user_tags = ["nature", "food"]
        locations = [{"name": "Ninh Thuận", "description": "Vùng đất nắng gió miền Trung"}]
        constraints = {"budget": 5_000_000, "max_time_per_day": 480}
        
        with patch("n5_activity_generator.LLM_MODULE_AVAILABLE", True), \
             patch("n5_activity_generator._is_llm_available", return_value=True), \
             patch("n5_activity_generator.generate_activities_from_llm", return_value=mock_llm_result):
            
            result = generate_activities_hybrid(
                user_tags, locations, constraints, use_llm=True
            )
        
        self.assertTrue(len(result) > 0)
        # Kết quả phải đến từ LLM vì mock thành công
        for act in result:
            self.assertEqual(act["generated_by"], "llm")
            self.assertEqual(act["location_name"], "Ninh Thuận")
    
    def test_hybrid_llm_failure_fallback(self):
        """Khi LLM thất bại (trả None), hybrid phải fallback về template."""
        user_tags = ["nature"]
        locations = [{"name": "Sa Pa"}]
        constraints = {"budget": 5_000_000, "max_time_per_day": 480}
        
        with patch("n5_activity_generator.LLM_MODULE_AVAILABLE", True), \
             patch("n5_activity_generator._is_llm_available", return_value=True), \
             patch("n5_activity_generator.generate_activities_from_llm", return_value=None):
            
            result = generate_activities_hybrid(
                user_tags, locations, constraints, use_llm=True
            )
        
        self.assertTrue(len(result) > 0)
        # Fallback: tất cả phải là template
        for act in result:
            self.assertEqual(act["generated_by"], "template")
            self.assertEqual(act["location_name"], "Sa Pa")
    
    def test_original_generate_still_works(self):
        """Hàm generate_activities gốc phải vẫn hoạt động bình thường."""
        user_tags = ["nature", "adventure"]
        locations = [{"name": "Sa Pa"}]
        constraints = {"budget": 5_000_000, "max_time_per_day": 480}
        
        result = generate_activities(user_tags, locations, constraints)
        self.assertTrue(len(result) > 0)
        # Hàm gốc giờ có trường generated_by = "template"
        for act in result:
            self.assertEqual(act["generated_by"], "template")


if __name__ == '__main__':
    unittest.main()

