"""
maps/emotions.py
================
Maps emotional states to travel experience keywords.

Users rarely say "I want a wellness resort." They say "I'm burned out" or
"Tôi đang rất mệt mỏi." These maps bridge that gap so the embedding vector
lands in the right semantic neighbourhood of the location database.
"""

# ── Exhaustion / Stress → restorative travel
EXHAUSTION_STRESS: dict[str, str] = {
    # Vietnamese
    "mệt mỏi":          "relaxation spa resort slow-travel rest wellness retreat",
    "kiệt sức":         "deep-rest wellness spa secluded resort recovery",
    "mệt":              "relaxation peaceful rest resort quiet",
    "uể oải":           "fresh-air nature walk scenic gentle-activity",
    "căng thẳng":       "relaxation nature tranquil meditation wellness retreat peaceful",
    "lo lắng":          "calm serene nature scenic meditation mindfulness",
    "áp lực":           "escape nature secluded quiet stress-relief retreat",
    "stress":           "relaxation nature wellness meditation tranquil",
    "bồn chồn":         "calm quiet scenic nature walk meditation",
    "quá tải":          "escape off-grid nature quiet secluded retreat",
    # English
    "exhausted":        "spa wellness resort secluded rest recovery",
    "burned out":       "deep-rest wellness retreat nature slow-travel",
    "tired":            "relaxation resort beach quiet rest",
    "drained":          "nature retreat wellness calm rejuvenate",
    "stressed":         "relaxation spa nature retreat peaceful wellness meditation",
    "anxious":          "calm serene nature meditation mindfulness tranquil",
    "overwhelmed":      "escape secluded quiet nature off-grid retreat",
    "tense":            "spa massage wellness relaxation tranquil",
    "on edge":          "peaceful nature quiet retreat mindfulness",
}
 
# ── Boredom → active / varied travel
BOREDOM: dict[str, str] = {
    # Vietnamese
    "chán":             "entertainment activities nightlife adventure variety stimulating",
    "nhàm chán":        "new-experience unique discovery adventure variety",
    "buồn tẻ":          "vibrant lively entertainment variety unique",
    "tẻ nhạt":          "stimulating discovery adventure entertainment variety",
    # English
    "bored":            "entertainment activities nightlife adventure variety stimulating",
    "stagnant":         "new-experience discovery stimulating vibrant",
    "monotonous":       "variety unique discovery adventure stimulating",
    "dull":             "vibrant colorful lively entertainment adventure",
}
 
# ── Sadness / Loneliness → uplifting or healing travel
SADNESS: dict[str, str] = {
    # Vietnamese
    "buồn":             "uplifting scenic colorful cheerful vibrant festival",
    "cô đơn":           "social community lively festival crowd people-watching",
    "trống rỗng":       "vibrant lively social cultural discovery",
    "chán nản":         "new-experience discovery adventure vibrant stimulating",
    "nặng nề":          "light cheerful colorful scenic uplifting",
    "nhớ nhà":          "cozy warm local community comfort familiar",
    # English
    "sad":              "uplifting scenic beautiful colorful cheerful",
    "lonely":           "social community festival crowd lively people-watching",
    "empty":            "vibrant lively social cultural stimulating",
    "down":             "cheerful colorful vibrant warm social",
    "heartbroken":      "scenic peaceful healing nature beautiful",
    "melancholy":       "scenic beautiful gentle nature peaceful artistic",
    "homesick":         "cozy warm community local familiar comfort",
}
 
# ── Romance → romantic travel
ROMANCE: dict[str, str] = {
    # Vietnamese
    "lãng mạn":         "romantic sunset couple candlelight scenic private intimate",
    "kỷ niệm":          "romantic special anniversary couple scenic",
    "tuần trăng mật":   "honeymoon luxury romantic private resort scenic",
    "tình cảm":         "romantic intimate scenic private couple",
    # English
    "romantic":         "romantic sunset couple private intimate scenic",
    "anniversary":      "romantic special scenic luxury private couple",
    "honeymoon":        "honeymoon luxury romantic private resort scenic",
    "proposal":         "scenic viewpoint private romantic sunset luxury",
    "valentine":        "romantic couple scenic private luxury sunset",
}
 
ALL_EMOTIONS: dict[str, str] = {
    **EXHAUSTION_STRESS,
    **BOREDOM,
    **SADNESS,
    **ROMANCE,
}