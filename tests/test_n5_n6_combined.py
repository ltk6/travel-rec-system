"""
tests/test_n5_n6_combined.py
============================
Test tổng hợp N5 (Activity Generation) + N6 (Activity Ranking).

Ưu tiên dùng 1 location thực lấy từ database.
Fallback về mock location khi DB không khả dụng.

Chạy từ thư mục gốc dự án:
    pytest tests/test_n5_n6_combined.py -v
"""

import math
import random
import pytest

# ---------------------------------------------------------------------------
# Import N5
# ---------------------------------------------------------------------------
from backend.modules.n5_activity_generation import generate_activities
from backend.modules.n5_activity_generation.n5_activity_generator import _is_sightseeing

# ---------------------------------------------------------------------------
# Import N6 — dùng qua package __init__ để xác nhận export hoạt động đúng
# ---------------------------------------------------------------------------
from backend.modules.n6_activity_ranking import rank_activities

# ---------------------------------------------------------------------------
# Import DB — skip DB tests nếu không kết nối được
# ---------------------------------------------------------------------------
try:
    from backend.n3_database.db_manager import get_all_locations
    _DB_MODULE_OK = True
except Exception:
    _DB_MODULE_OK = False

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
VECTOR_DIM = 16
TOP_K = 5

random.seed(42)


# ===========================================================================
# HELPERS
# ===========================================================================

def _make_vector(seed: float, dim: int = VECTOR_DIM) -> list:
    """Tạo unit vector giả lập có thể tái tạo theo seed."""
    rng = random.Random(seed)
    v = [rng.gauss(0, 1) for _ in range(dim)]
    norm = math.sqrt(sum(x * x for x in v))
    if norm == 0:
        return [0.0] * dim
    return [x / norm for x in v]


def _attach_vectors(activities: list) -> list:
    """
    Gán vectors mock cho activities dựa theo activity_type.
    Activities cùng loại nhận vectors gần nhau để semantic score có ý nghĩa.
    Hàm này KHÔNG thay đổi list gốc — trả về list mới với vectors đã gán.
    """
    type_seed = {
        "nature": 1.0, "adventure": 2.0, "relaxation": 3.0,
        "culture": 4.0, "food": 5.0, "nightlife": 6.0, "shopping": 7.0,
    }
    result = []
    for act in activities:
        act = dict(act)  # shallow copy để không mutate list gốc
        atype = act.get("metadata", {}).get("activity_type", "nature")
        s = type_seed.get(atype, 0.5)
        act["vectors"] = {
            "tag":    _make_vector(s),
            "text":   _make_vector(s + 0.1),
            "intent": _make_vector(s + 0.2),
        }
        result.append(act)
    return result


def _make_user_vectors(primary_seed: float = 1.0) -> dict:
    """Tạo user_vectors (nature-focused theo mặc định)."""
    return {
        "tag":     _make_vector(primary_seed),
        "context": _make_vector(primary_seed + 0.05),
        "emotion": _make_vector(primary_seed + 0.1),
    }


def _load_one_location_from_db():
    """Lấy 1 location từ DB. Trả về None nếu lỗi hoặc DB trống."""
    if not _DB_MODULE_OK:
        return None
    try:
        locs = get_all_locations()
        return locs[0] if locs else None
    except Exception:
        return None


def _build_activity(activity_id, activity_type, indoor_outdoor,
                    weather_dependent, time_of_day, duration, price_level,
                    vec_seed):
    """Helper tạo activity dict đầy đủ schema cho N6."""
    return {
        "activity_id": activity_id,
        "location_id": "loc_test",
        "metadata": {
            "name": f"Hoạt động {activity_id}",
            "description": f"Mô tả {activity_id}",
            "activity_type": activity_type,
            "activity_subtype": None,
            "intensity": 0.5,
            "physical_level": 0.3,
            "social_level": 0.5,
            "estimated_duration": float(duration),
            "price_level": float(price_level),
            "indoor_outdoor": indoor_outdoor,
            "weather_dependent": weather_dependent,
            "time_of_day_suitable": time_of_day,
        },
        "vectors": {
            "tag":    _make_vector(vec_seed),
            "text":   _make_vector(vec_seed + 0.1),
            "intent": _make_vector(vec_seed + 0.2),
        },
    }


# ===========================================================================
# FIXTURES
# ===========================================================================

@pytest.fixture(scope="module")
def db_location():
    """
    1 location thực lấy từ database.
    Test bị skip tự động nếu DB không khả dụng hoặc không có dữ liệu.
    """
    loc = _load_one_location_from_db()
    if loc is None:
        pytest.skip("Database không khả dụng hoặc chưa có location nào.")
    return loc


@pytest.fixture(scope="module")
def mock_location():
    """Location mẫu cố định — không cần DB."""
    return {
        "location_id": "loc_sapa_test",
        "metadata": {
            "name": "Sa Pa",
            "description": "Thị trấn vùng cao với ruộng bậc thang hùng vĩ",
            "tags": ["mountain", "trekking", "nature", "cool_weather", "photography"],
        },
        "vectors": {},
        "geo": {"lat": 22.3364, "lng": 103.8438},
    }


@pytest.fixture(scope="module")
def base_user_input():
    """User profile và constraints dùng chung."""
    return {
        "user": {
            "text": "Tôi muốn ngắm cảnh thiên nhiên và chụp ảnh",
            "image_description": None,
            "tags": ["nature", "photography", "sightseeing", "relax"],
        },
        "constraints": {
            "budget": 5_000_000,
            "duration": 480,
            "people": 2,
            "time_of_day": "morning",
        },
    }


# ===========================================================================
# N5 — TEST VỚI LOCATION TỪ DATABASE
# ===========================================================================

class TestN5WithDBLocation:
    """Tests N5 dùng 1 location thực lấy từ database."""

    @pytest.fixture(autouse=True)
    def _setup(self, db_location, base_user_input):
        n5_input = {
            **base_user_input,
            "locations": [{
                "location_id": db_location["location_id"],
                "metadata": db_location["metadata"],
            }],
        }
        result = generate_activities(n5_input)
        self.activities = result.get("activities", [])
        self.loc_id = db_location["location_id"]

    def test_generates_exactly_100_activities(self):
        assert len(self.activities) == 100, (
            f"N5 phải sinh đúng 100 activities cho 1 location, got {len(self.activities)}"
        )

    def test_all_activities_belong_to_correct_location(self):
        wrong = [a for a in self.activities if a.get("location_id") != self.loc_id]
        assert len(wrong) == 0, f"{len(wrong)} activities có location_id sai"

    def test_schema_has_all_required_fields(self):
        required_meta = [
            "name", "description", "activity_type", "activity_subtype",
            "intensity", "physical_level", "social_level",
            "estimated_duration", "price_level",
            "indoor_outdoor", "weather_dependent", "time_of_day_suitable",
        ]
        for act in self.activities:
            assert "activity_id" in act
            assert "location_id" in act
            meta = act.get("metadata", {})
            missing = [f for f in required_meta if f not in meta]
            assert not missing, (
                f"Activity '{act.get('activity_id')}' thiếu fields: {missing}"
            )

    def test_sightseeing_ratio_at_least_40_percent(self):
        sg_count = sum(1 for a in self.activities if _is_sightseeing(a))
        ratio = sg_count / len(self.activities)
        assert ratio >= 0.40, f"Sightseeing ratio {ratio:.1%} < ngưỡng 40%"

    def test_numeric_fields_within_valid_ranges(self):
        for act in self.activities:
            meta = act["metadata"]
            aid = act["activity_id"]
            assert 0.0 <= meta["intensity"] <= 1.0,        f"[{aid}] intensity={meta['intensity']} ngoài [0,1]"
            assert 1.0 <= meta["price_level"] <= 5.0,      f"[{aid}] price_level={meta['price_level']} ngoài [1,5]"
            assert meta["estimated_duration"] > 0,          f"[{aid}] estimated_duration <= 0"
            if meta["physical_level"] is not None:
                assert 0.0 <= meta["physical_level"] <= 1.0
            if meta["social_level"] is not None:
                assert 0.0 <= meta["social_level"] <= 1.0

    def test_valid_enum_values(self):
        valid_types = {"nature", "adventure", "relaxation", "culture", "food", "nightlife", "shopping"}
        valid_io    = {"indoor", "outdoor", "mixed"}
        valid_tod   = {"morning", "afternoon", "night", "anytime", None}
        for act in self.activities:
            meta = act["metadata"]
            aid  = act["activity_id"]
            assert meta["activity_type"]     in valid_types, f"[{aid}] activity_type='{meta['activity_type']}' không hợp lệ"
            assert meta["indoor_outdoor"]    in valid_io,    f"[{aid}] indoor_outdoor='{meta['indoor_outdoor']}' không hợp lệ"
            assert meta["time_of_day_suitable"] in valid_tod, f"[{aid}] time_of_day_suitable không hợp lệ"

    def test_no_duplicate_activity_ids(self):
        ids = [a["activity_id"] for a in self.activities]
        duplicates = [aid for aid in set(ids) if ids.count(aid) > 1]
        assert not duplicates, f"Tồn tại activity_id bị trùng: {duplicates[:5]}"

    def test_activity_type_diversity(self):
        types = set(a["metadata"]["activity_type"] for a in self.activities)
        assert len(types) >= 3, (
            f"N5 chỉ sinh được {len(types)} loại: {types}. Cần ít nhất 3."
        )


# ===========================================================================
# N5 — TEST VỚI MOCK LOCATION (không cần DB)
# ===========================================================================

class TestN5Mock:

    def test_empty_locations_returns_empty(self, base_user_input):
        result = generate_activities({**base_user_input, "locations": []})
        assert result == {"activities": []}

    def test_unknown_location_uses_fallback_and_generates_100(self, base_user_input):
        n5_input = {
            **base_user_input,
            "locations": [{
                "location_id": "loc_unknown_xyz",
                "metadata": {
                    "name": "Bản Giốc",
                    "description": "Thác nước ở Cao Bằng",
                    "tags": ["waterfall", "nature", "adventure"],
                },
            }],
        }
        result = generate_activities(n5_input)
        assert len(result.get("activities", [])) == 100

    def test_multiple_locations_generates_100_each(self, mock_location, base_user_input):
        second = {
            "location_id": "loc_dalat_test",
            "metadata": {
                "name": "Đà Lạt",
                "description": "Thành phố ngàn hoa",
                "tags": ["flower", "nature", "romantic", "cool_weather"],
            },
        }
        n5_input = {
            **base_user_input,
            "locations": [
                {"location_id": mock_location["location_id"], "metadata": mock_location["metadata"]},
                second,
            ],
        }
        activities = generate_activities(n5_input)["activities"]
        assert len(activities) == 200

        from collections import Counter
        dist = Counter(a["location_id"] for a in activities)
        assert dist[mock_location["location_id"]] == 100
        assert dist["loc_dalat_test"] == 100

    def test_user_tags_as_string_parses_correctly(self, mock_location):
        n5_input = {
            "user": {"text": None, "image_description": None, "tags": "nature,photography,relax"},
            "locations": [{"location_id": mock_location["location_id"], "metadata": mock_location["metadata"]}],
            "constraints": {},
        }
        assert len(generate_activities(n5_input)["activities"]) == 100

    def test_missing_constraints_uses_defaults(self, mock_location):
        n5_input = {
            "user": {"tags": ["nature"]},
            "locations": [{"location_id": mock_location["location_id"], "metadata": mock_location["metadata"]}],
            "constraints": {},
        }
        assert len(generate_activities(n5_input)["activities"]) == 100

    def test_price_level_output_range_is_1_to_5(self, mock_location, base_user_input):
        """N5 phải output price_level trong [1.0, 5.0] — đây là thang N6 dùng để tính budget_score."""
        n5_input = {
            **base_user_input,
            "locations": [{"location_id": mock_location["location_id"], "metadata": mock_location["metadata"]}],
        }
        for act in generate_activities(n5_input)["activities"]:
            pl = act["metadata"]["price_level"]
            assert 1.0 <= pl <= 5.0, f"price_level={pl} ngoài [1.0, 5.0]"


# ===========================================================================
# N6 — UNIT TESTS
# ===========================================================================

class TestN6:

    def test_returns_top_k_results(self):
        activities = [
            _build_activity(f"act_{i}", "nature", "outdoor", True, "morning", 120, 2.0, float(i))
            for i in range(20)
        ]
        result = rank_activities({
            "user_vectors": _make_user_vectors(),
            "context": {"time_of_day": "morning"},
            "activities": activities,
            "constraints": {"duration": 480, "weather": "sunny"},
            "top_k": TOP_K,
        })
        assert len(result["activities"]) == TOP_K

    def test_scores_in_valid_range_0_to_1(self):
        activities = [
            _build_activity(f"act_{i}", "nature", "outdoor", True, "morning", 120, 2.0, float(i))
            for i in range(10)
        ]
        result = rank_activities({
            "user_vectors": _make_user_vectors(),
            "context": {"time_of_day": "morning"},
            "activities": activities,
            "constraints": {"duration": 480, "weather": "sunny"},
            "top_k": TOP_K,
        })
        for act in result["activities"]:
            assert 0.0 <= act["score"] <= 1.0, f"score={act['score']} ngoài [0,1]"

    def test_results_sorted_descending_by_score(self):
        activities = [
            _build_activity(f"act_{i}", "nature", "outdoor", True, "morning", 120, 2.0, float(i))
            for i in range(15)
        ]
        result = rank_activities({
            "user_vectors": _make_user_vectors(),
            "context": {"time_of_day": "morning"},
            "activities": activities,
            "constraints": {"duration": 480, "weather": "sunny"},
            "top_k": TOP_K,
        })
        scores = [a["score"] for a in result["activities"]]
        assert scores == sorted(scores, reverse=True)

    def test_output_has_required_fields(self):
        result = rank_activities({
            "user_vectors": _make_user_vectors(),
            "context": {"time_of_day": "morning"},
            "activities": [_build_activity("act_1", "nature", "outdoor", True, "morning", 120, 2.0, 1.0)],
            "constraints": {"duration": 480, "weather": "sunny"},
            "top_k": 1,
        })
        for act in result["activities"]:
            assert "activity_id" in act
            assert "location_id" in act
            assert "score" in act
            assert isinstance(act.get("reason"), str) and len(act["reason"]) > 0

    def test_empty_activities_returns_empty(self):
        result = rank_activities({
            "user_vectors": _make_user_vectors(),
            "context": {"time_of_day": "morning"},
            "activities": [],
            "constraints": {"duration": 480, "weather": "sunny"},
            "top_k": TOP_K,
        })
        assert result == {"activities": []}

    def test_missing_top_k_uses_default_5(self):
        """top_k không được truyền → default 5 → trả về tối đa 5 kết quả, không crash."""
        activities = [
            _build_activity(f"act_{i}", "nature", "outdoor", True, "morning", 120, 2.0, float(i))
            for i in range(10)
        ]
        result = rank_activities({
            "user_vectors": _make_user_vectors(),
            "context": {"time_of_day": "morning"},
            "activities": activities,
            "constraints": {"duration": 480, "weather": "sunny"},
            # không có "top_k"
        })
        assert len(result["activities"]) == 5

    def test_top_k_larger_than_available_returns_all(self):
        activities = [
            _build_activity(f"act_{i}", "nature", "outdoor", True, "morning", 60, 2.0, float(i))
            for i in range(3)
        ]
        result = rank_activities({
            "user_vectors": _make_user_vectors(),
            "context": {"time_of_day": "morning"},
            "activities": activities,
            "constraints": {"duration": 480, "weather": "sunny"},
            "top_k": 10,
        })
        assert len(result["activities"]) == 3

    def test_hard_constraint_filters_activities_exceeding_duration(self):
        """Activities dài hơn duration của user phải bị loại hoàn toàn."""
        activities = [
            _build_activity(f"act_{i}", "nature", "outdoor", True, "morning",
                            duration=300, price_level=2.0, vec_seed=float(i))
            for i in range(10)
        ]
        result = rank_activities({
            "user_vectors": _make_user_vectors(),
            "context": {"time_of_day": "morning"},
            "activities": activities,
            "constraints": {"duration": 60, "weather": "sunny"},  # 300 > 60 → tất cả bị loại
            "top_k": TOP_K,
        })
        assert len(result["activities"]) == 0

    def test_budget_score_cheaper_activity_scores_higher(self):
        """
        Sau khi fix: budget_score = (5.0 - price_level) / 4.0
        price_level=1.0 → budget_score=1.0 (rẻ nhất)
        price_level=5.0 → budget_score=0.0 (đắt nhất)
        Với cùng semantic và context → activity rẻ hơn phải xếp trên.
        """
        same_vec = _make_vector(1.0)
        user_vec = {"tag": same_vec, "context": same_vec, "emotion": same_vec}

        cheap = _build_activity("act_cheap", "nature", "outdoor", False, "morning", 120, 1.0, 1.0)
        expensive = _build_activity("act_expensive", "nature", "outdoor", False, "morning", 120, 5.0, 1.0)
        # Gán cùng vector để loại trừ yếu tố semantic
        for act in [cheap, expensive]:
            act["vectors"] = {"tag": same_vec, "text": same_vec, "intent": same_vec}

        result = rank_activities({
            "user_vectors": user_vec,
            "context": {"time_of_day": "morning"},
            "activities": [expensive, cheap],  # truyền expensive trước để test không phụ thuộc thứ tự
            "constraints": {"duration": 480, "weather": "sunny"},
            "top_k": 2,
        })
        ranked_ids = [a["activity_id"] for a in result["activities"]]
        assert ranked_ids[0] == "act_cheap", (
            f"Activity rẻ hơn (price_level=1.0) phải xếp trên đắt hơn (price_level=5.0). "
            f"Thứ tự nhận được: {ranked_ids}"
        )

    def test_rainy_weather_prefers_indoor_over_outdoor(self):
        """Khi trời mưa, hoạt động indoor phải xếp cao hơn outdoor phụ thuộc thời tiết."""
        same_vec = _make_vector(1.0)
        user_vec = {"tag": same_vec, "context": same_vec, "emotion": same_vec}

        indoor = _build_activity("act_indoor", "culture", "indoor", False, "anytime", 120, 2.0, 4.0)
        outdoor = _build_activity("act_outdoor", "adventure", "outdoor", True, "morning", 120, 2.0, 4.0)
        # Cùng vector để semantic score bằng nhau
        for act in [indoor, outdoor]:
            act["vectors"] = {"tag": same_vec, "text": same_vec, "intent": same_vec}

        result = rank_activities({
            "user_vectors": user_vec,
            "context": {"time_of_day": "morning"},
            "activities": [indoor, outdoor],
            "constraints": {"duration": 480, "weather": "rainy"},
            "top_k": 2,
        })
        ranked_ids = [a["activity_id"] for a in result["activities"]]
        assert ranked_ids[0] == "act_indoor", (
            "Khi trời mưa, indoor phải xếp cao hơn outdoor có weather_dependent=True"
        )

    def test_time_of_day_match_boosts_score(self):
        """Activity khớp giờ user phải xếp cao hơn activity lệch giờ."""
        same_vec = _make_vector(1.0)
        user_vec = {"tag": same_vec, "context": same_vec, "emotion": same_vec}

        morning = _build_activity("act_morning", "nature", "outdoor", False, "morning", 120, 2.0, 1.0)
        night   = _build_activity("act_night",   "nature", "outdoor", False, "night",   120, 2.0, 1.0)
        for act in [morning, night]:
            act["vectors"] = {"tag": same_vec, "text": same_vec, "intent": same_vec}

        result = rank_activities({
            "user_vectors": user_vec,
            "context": {"time_of_day": "morning"},
            "activities": [morning, night],
            "constraints": {"duration": 480, "weather": "sunny"},
            "top_k": 2,
        })
        ranked_ids = [a["activity_id"] for a in result["activities"]]
        assert ranked_ids[0] == "act_morning", (
            "Activity khớp giờ 'morning' phải xếp cao hơn 'night' khi user context là morning"
        )


# ===========================================================================
# PIPELINE — N5 → N6 (DÙNG DB LOCATION)
# ===========================================================================

class TestPipelineWithDB:
    """Test toàn bộ pipeline N5 → N6 với location thực từ database."""

    def test_full_pipeline_produces_ranked_top_k(self, db_location, base_user_input):
        # N5
        n5_input = {
            **base_user_input,
            "locations": [{"location_id": db_location["location_id"],
                           "metadata": db_location["metadata"]}],
        }
        activities = generate_activities(n5_input)["activities"]
        assert len(activities) == 100

        # Gán vectors → N6
        result = rank_activities({
            "user_vectors": _make_user_vectors(),
            "context": {"time_of_day": base_user_input["constraints"]["time_of_day"]},
            "activities": _attach_vectors(activities),
            "constraints": {
                "duration": base_user_input["constraints"]["duration"],
                "weather": "sunny",
            },
            "top_k": TOP_K,
        })
        ranked = result["activities"]

        assert len(ranked) == TOP_K
        scores = [a["score"] for a in ranked]
        assert scores == sorted(scores, reverse=True)
        assert all(0.0 <= a["score"] <= 1.0 for a in ranked)
        assert all(len(a.get("reason", "")) > 0 for a in ranked)

    def test_pipeline_morning_vs_night_gives_different_top5(self, db_location, base_user_input):
        """Context khác nhau phải cho top-5 khác nhau."""
        n5_input = {
            **base_user_input,
            "locations": [{"location_id": db_location["location_id"],
                           "metadata": db_location["metadata"]}],
        }
        activities = _attach_vectors(generate_activities(n5_input)["activities"])

        morning_ids = set(
            a["activity_id"] for a in rank_activities({
                "user_vectors": _make_user_vectors(),
                "context": {"time_of_day": "morning"},
                "activities": activities,
                "constraints": {"duration": 480, "weather": "sunny"},
                "top_k": TOP_K,
            })["activities"]
        )
        night_ids = set(
            a["activity_id"] for a in rank_activities({
                "user_vectors": _make_user_vectors(),
                "context": {"time_of_day": "night"},
                "activities": activities,
                "constraints": {"duration": 480, "weather": "sunny"},
                "top_k": TOP_K,
            })["activities"]
        )
        assert morning_ids != night_ids, (
            "Top activities lúc sáng và tối phải khác nhau khi context thay đổi"
        )


# ===========================================================================
# PIPELINE — N5 → N6 (MOCK — không cần DB)
# ===========================================================================

class TestPipelineMock:
    """Test pipeline N5 → N6 với mock location — chạy được kể cả khi không có DB."""

    def test_pipeline_produces_valid_ranked_output(self, mock_location, base_user_input):
        n5_input = {
            **base_user_input,
            "locations": [{"location_id": mock_location["location_id"],
                           "metadata": mock_location["metadata"]}],
        }
        activities = _attach_vectors(generate_activities(n5_input)["activities"])

        result = rank_activities({
            "user_vectors": _make_user_vectors(),
            "context": {"time_of_day": "morning"},
            "activities": activities,
            "constraints": {"duration": 480, "weather": "sunny"},
            "top_k": TOP_K,
        })
        ranked = result["activities"]

        assert len(ranked) == TOP_K
        assert all("activity_id" in a and "score" in a and "reason" in a for a in ranked)
        scores = [a["score"] for a in ranked]
        assert scores == sorted(scores, reverse=True)

    def test_pipeline_rainy_weather_still_returns_results(self, mock_location, base_user_input):
        n5_input = {
            **base_user_input,
            "locations": [{"location_id": mock_location["location_id"],
                           "metadata": mock_location["metadata"]}],
        }
        activities = _attach_vectors(generate_activities(n5_input)["activities"])

        result = rank_activities({
            "user_vectors": _make_user_vectors(),
            "context": {"time_of_day": "morning"},
            "activities": activities,
            "constraints": {"duration": 480, "weather": "rainy"},
            "top_k": TOP_K,
        })
        ranked = result["activities"]

        assert len(ranked) == TOP_K
        assert all(0.0 <= a["score"] <= 1.0 for a in ranked)

    def test_pipeline_n6_activity_ids_reference_n5_output(self, mock_location, base_user_input):
        """activity_id trong kết quả N6 phải là subset của activities do N5 sinh ra."""
        n5_input = {
            **base_user_input,
            "locations": [{"location_id": mock_location["location_id"],
                           "metadata": mock_location["metadata"]}],
        }
        n5_activities = generate_activities(n5_input)["activities"]
        n5_ids = {a["activity_id"] for a in n5_activities}

        result = rank_activities({
            "user_vectors": _make_user_vectors(),
            "context": {"time_of_day": "morning"},
            "activities": _attach_vectors(n5_activities),
            "constraints": {"duration": 480, "weather": "sunny"},
            "top_k": TOP_K,
        })
        for ranked_act in result["activities"]:
            assert ranked_act["activity_id"] in n5_ids, (
                f"activity_id '{ranked_act['activity_id']}' trong kết quả N6 "
                f"không tồn tại trong output N5"
            )
