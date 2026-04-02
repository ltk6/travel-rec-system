"""
maps/context.py
===============
Contextual signal maps.
  - SEASON_WEATHER : season/climate words don't embed reliably to travel scenes
  - SOCIAL_GROUP   : Vietnamese group terms need bridging to travel style
"""

# ── Season / Weather → travel scene
SEASON_WEATHER: dict[str, str] = {
    # Vietnamese
    "mùa hè":           "beach coastal water-sports sun outdoor hot",
    "mùa đông":         "highland cool mountain cozy indoor retreat warm",
    "mùa xuân":         "festival blossom green fresh outdoor mild",
    "mùa thu":          "scenic leaf colorful cool highland peaceful",
    "mùa mưa":          "indoor cozy cave waterfall green lush scenic",
    "mùa khô":          "beach outdoor activities dry sun clear-sky",
    "tết":              "festival cultural tradition local celebration crowd",
    "cuối tuần":        "short-trip nearby compact weekend getaway",
    "nóng":             "cool shade beach water highland mountain",
    "lạnh":             "warm indoor cozy highland fog scenic mountain",
    "mưa":              "indoor café cozy cave waterfall green lush",
    "nắng":             "sunny beach outdoor picnic clear-sky scenic",
    "sương mù":         "misty highland foggy atmospheric ethereal mountain",
    "mát mẻ":           "cool highland mountain fresh-air forest nature",
    # English
    "summer":           "beach water-sports sun coastal outdoor holiday",
    "winter":           "highland cool cozy mountain indoor warm retreat",
    "spring":           "blossom outdoor fresh mild festival green",
    "autumn":           "leaf colorful cool scenic highland peaceful",
    "rainy season":     "indoor cozy waterfall cave green lush",
    "dry season":       "beach outdoor clear-sky activities sunny",
    "long weekend":     "short-trip nearby compact quick-getaway",
    "hot":              "cool shade highland beach water",
    "cold":             "warm indoor cozy highland scenic mountain",
    "sunny":            "beach outdoor picnic clear-sky sunshine scenic",
    "foggy":            "misty highland atmospheric ethereal mountain scenic",
    "cool":             "cool highland mountain fresh-air forest",
}

# ── Social group → travel style
SOCIAL_GROUP: dict[str, str] = {
    # Vietnamese
    "một mình":         "solo independent flexible self-paced peaceful discovery",
    "cặp đôi":          "romantic couple private intimate sunset scenic",
    "vợ chồng":         "couple romantic private intimate scenic resort",
    "gia đình":         "family kid-friendly safe educational activities",
    "trẻ em":           "family kid-safe educational fun shallow-beach",
    "bạn bè":           "group social fun nightlife adventure flexible",
    "nhóm bạn":         "group social activities adventure fun variety",
    "sinh viên":        "budget backpacker social affordable fun hostel",
    "người lớn tuổi":   "accessible gentle scenic comfortable easy cultural",
    "người già":   "accessible gentle scenic comfortable easy cultural",
    "ông bà":           "accessible comfortable gentle scenic heritage cultural",
    # English
    "alone":            "solo independent flexible self-paced peaceful",
    "solo":             "solo independent flexible self-discovery peaceful",
    "couple":           "romantic couple intimate sunset private scenic",
    "two of us":        "romantic couple private intimate scenic",
    "family":           "family kid-friendly safe educational comfortable",
    "with kids":        "kid-safe shallow-beach fun educational accessible",
    "elderly":          "accessible comfortable gentle scenic cultural heritage",
    "friends":          "group social fun nightlife activities adventure",
    "group":            "group variety social activities flexible",
    "newlyweds":        "honeymoon romantic luxury private resort scenic",
    "students":         "budget affordable backpacker social hostel fun",
    "backpackers":      "budget hostel social flexible backpacker",
}

ALL_CONTEXT: dict[str, str] = {
    **SEASON_WEATHER,
    **SOCIAL_GROUP,
}