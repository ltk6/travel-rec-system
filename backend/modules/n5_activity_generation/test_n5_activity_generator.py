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

        meta = act.get("metadata", {})
        atype = meta.get("activity_type", "?")
        type_counts[atype] = type_counts.get(atype, 0) + 1

        if _is_sightseeing(act):
            sightseeing_count += 1

    print(f"\n  Per-location counts:")
    for loc, cnt in loc_counts.items():
        print(f"    {loc}: {cnt} activities")

    print(f"\n  Activity type distribution:")
    for atype, cnt in sorted(type_counts.items(), key=lambda x: -x[1]):
        print(f"    {atype}: {cnt}")

    sightseeing_ratio = sightseeing_count / len(activities) if activities else 0
    print(f"\n  Sightseeing activities: {sightseeing_count} ({sightseeing_ratio:.1%})")
    status = "✓ OK" if sightseeing_ratio >= 0.40 else "✗ BELOW TARGET (40%)"
    print(f"  Sightseeing ratio ≥ 40%: {status}")

    # Schema validation
    print(f"\n  Schema validation (first 3 activities):")
    required_meta_fields = [
        "name", "description", "activity_type", "activity_subtype",
        "intensity", "physical_level", "social_level",
        "estimated_duration", "price_level", "indoor_outdoor",
        "weather_dependent", "time_of_day_suitable"
    ]
    all_valid = True
    for i, act in enumerate(activities[:3]):
        missing = []
        meta = act.get("metadata", {})
        for f in required_meta_fields:
            if f not in meta:
                missing.append(f)
        if missing:
            print(f"    [{i+1}] MISSING: {missing}")
            all_valid = False
        else:
            print(f"    [{i+1}] {meta['name'][:50]} → {meta['activity_type']} / {meta['activity_subtype']}")

    if all_valid:
        print(f"\n  ✓ All schema fields present")

    # Sample output JSON
    if activities:
        print(f"\n  Sample activity (first):")
        print(json.dumps(activities[0], indent=4, ensure_ascii=False))


if __name__ == "__main__":
    run_test("Single location (Sa Pa) — 100 activities target", SAMPLE_INPUT_SINGLE)
    run_test("Multi-location (Phú Quốc + Nha Trang) — 200 total", SAMPLE_INPUT_MULTI)
    run_test("Unknown location (Bản Giốc) — fallback test", SAMPLE_INPUT_UNKNOWN_LOCATION)

    print(f"\n{'='*60}")
    print("  All tests completed.")
    print(f"{'='*60}\n")