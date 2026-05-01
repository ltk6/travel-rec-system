
import json
import os
import sys

# Add project root to path for imports
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from backend.modules.n5_activity_generation import generate_activities
from config.settings import GROQ_API_KEY
import logging

# Configure logging for test visibility
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# 1. Define Sample Input
sample_data = {
    "user": {
        "text": "Tôi muốn đi du lịch nghỉ dưỡng và ăn hải sản",
        "tags": ["beach", "relax", "seafood", "nature"]
    },
    "locations": [
        {
            "location_id": "loc_015",
            "metadata": {
                "name": "Bãi Sao Phú Quốc",
                "description": "Bãi biển đẹp nhất Phú Quốc với cát trắng mịn và nước xanh ngọc."
            }
        }
    ],
    "constraints": {
        "budget": 5000000,
        "duration": 3,
        "people": 2
    },
    "target_count": 20
}

def run_test():
    print("--- N5 Activity Generation Test ---")
    print(f"Generating activities for: {[loc['metadata']['name'] for loc in sample_data['locations']]}")
    
    # 2. Generate Activities
    # Note: If GROQ_API_KEY is not set, it will automatically fallback to Template mode
    result = generate_activities(sample_data)
    
    # 3. Save to JSON
    output_file = os.path.join(os.path.dirname(__file__), "output_activities.json")
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    
    # 4. Print Summary
    activities = result.get("activities", [])
    print(f"\nSuccessfully generated {len(activities)} activities.")
    print(f"Results saved to: {os.path.abspath(output_file)}")
    
    # Print first 3 activities as a teaser
    print("\nTop 3 Sample Activities:")
    for i, act in enumerate(activities[:3]):
        meta = act.get("metadata", {})
        print(f"{i+1}. {meta.get('name', 'N/A')} ({act.get('location_id', 'N/A')})")

if __name__ == "__main__":
    run_test()
