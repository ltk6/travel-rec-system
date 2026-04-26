"""
maps/tags.py
============

Lightweight semantic tagging system for Vietnam travel destinations.

This module defines a controlled ontology of travel-related tags used to
represent both:
  1. User intent
  2. Location attributes

Design goals:
- High-signal, discriminative tags for ranking stability
- Compact 2–4 token English keyword phrases only
- No redundancy or semantic duplication
- Balanced coverage of Vietnam travel domain
- Embedding-friendly structure (single-vector fusion)

─────────────────────────────────────────────────────────────
LOCATION TAGGING RULE
─────────────────────────────────────────────────────────────

When assigning tags to a location:

1. Use ONLY stable, long-term attributes
2. Avoid temporary or seasonal states unless intrinsic (e.g. climate zone)
3. Prefer discriminative signals over generic descriptors
4. Limit total tags per category to:
      → 3 to 8 tags per category (soft range)
5. Do NOT duplicate semantic meaning across categories
6. Avoid over-tagging (quality > coverage)

─────────────────────────────────────────────────────────────
QUESTIONNAIRE TAGGING RULE
─────────────────────────────────────────────────────────────

When assigning tags from user inputs:

1. Map each answer to closest controlled vocabulary tag
2. Route intent into correct category (ENV / VIBE / ACT / FOOD / CONSTRAINT)
3. Do NOT infer missing preferences beyond user input
4. Keep representation minimal but high-signal
5. Preserve consistency with location tag space

─────────────────────────────────────────────────────────────
SECTION INDEX
─────────────────────────────────────────────────────────────

A. ENVIRONMENT   — terrain, nature, weather, setting
B. CULTURE       — heritage, cities, religion, arts
C. ACTIVITIES    — sports, tours, exploration
D. FOOD          — cuisine, dining
E. VIBE          — mood, atmosphere, aesthetic
F. CONSTRAINTS   — budget, group type, accessibility
"""

ENVIRONMENT = {
    "mountain"               : "mountain elevation",
    "hill"                   : "hill gentle terrain",
    "karst"                  : "limestone karst",
    "valley"                 : "valley enclosed lowland",
    "plateau"                : "plateau highland",
    "delta"                  : "river delta flat",
    "sand dune"              : "sand dune arid",
    "cave"                   : "cave underground",
    "cliff"                  : "cliff coastal elevation",

    "beach"                  : "beach coastal",
    "bay"                    : "bay sheltered water",
    "island"                 : "island remote coastal",
    "archipelago"            : "archipelago island chain",
    "lake"                   : "lake inland water",
    "river"                  : "river flowing water",
    "stream"                 : "stream freshwater",
    "waterfall"              : "waterfall vertical flow",
    "hot spring"             : "hot spring thermal",
    "wetland"                : "wetland ecosystem",
    "lagoon"                 : "lagoon coastal water",

    "forest"                 : "forest dense vegetation",
    "mangrove"               : "mangrove coastal forest",
    "coral reef"             : "coral reef marine",
    "rice terrace"           : "rice terrace rural",
    "national park"          : "national park reserve",

    "summer"                 : "summer hot season",
    "winter"                 : "winter cold season",
    "spring"                 : "spring mild season",
    "autumn"                 : "autumn cool season",
    "rainy season"           : "rainy wet season",
    "dry season"             : "dry clear season",
}

CULTURE = {
    "city"                   : "city urban",
    "village"                : "village rural",
    "old town"               : "old town heritage",
    "ethnic village"         : "ethnic village indigenous",
    "craft village"          : "craft village artisan",
    "colonial architecture"  : "colonial architecture",

    "temple"                 : "temple spiritual",
    "pagoda"                 : "pagoda buddhist",
    "church"                 : "church religious",
    "citadel"                : "citadel imperial",
    "museum"                 : "museum cultural",

    "market"                 : "market commerce",
    "night market"           : "night market evening",
    "floating market"        : "floating market river",
    "festival"               : "festival celebration",

    "art"                    : "art creative",
    "architecture"           : "architecture landmark",
    "history"                : "historical heritage",
}

ACTIVITIES = {
    "trekking"               : "trekking hiking",
    "motorbiking"            : "motorbike road trip",
    "cycling"                : "cycling biking",
    "caving"                 : "caving exploration",
    "rock climbing"          : "rock climbing",
    "zip lining"             : "zip lining canopy",
    "canyoning"              : "canyoning waterfall",
    "camping"                : "camping outdoor",
    "picnic"                 : "picnic outdoor",

    "scuba diving"           : "scuba diving",
    "snorkeling"             : "snorkeling reef",
    "kayaking"               : "kayaking water",
    "stand up paddle"        : "stand up paddle",
    "surfing"                : "surfing ocean",
    "kitesurfing"            : "kitesurfing wind",
    "boat cruise"            : "boat cruise",
    "basket boat"            : "basket boat traditional",
    "fishing"                : "fishing",
    "squid fishing"          : "squid fishing night",

    "paragliding"            : "paragliding aerial",
    "skydiving"              : "skydiving extreme",
    "hot air balloon"        : "hot air balloon aerial",

    "birdwatching"           : "birdwatching",
    "wildlife safari"        : "wildlife safari",

    "cooking class"          : "cooking class",
    "language class"         : "language learning",
    "lantern making"         : "lantern making craft",
    "pottery class"          : "pottery class artisan",
    "farm tour"              : "farm tour agriculture",
    "tea tasting"            : "tea tasting",
    "wine tasting"           : "wine tasting",

    "photography"            : "photography",
    "shopping"               : "shopping retail",
    "sightseeing"            : "sightseeing tour",
    "cultural show"          : "cultural show performance",
    "golf"                   : "golf sport",
}

FOOD = {
    "local cuisine"          : "local cuisine regional",
    "street food"            : "street food vendor",
    "fine dining"            : "fine dining upscale",

    "seafood"                : "seafood coastal",
    "vegetarian"             : "vegetarian plant based",
    "vegan"                  : "vegan plant based",
    "halal"                  : "halal dietary",

    "coffee"                 : "coffee cafe",
    "draft beer"             : "draft beer social",
    "tropical fruit"         : "tropical fruit",
}

VIBE = {
    "peaceful"               : "peaceful calm",
    "vibrant"                : "vibrant energetic",
    "chill"                  : "chill laid back",

    "romantic"               : "romantic intimate",
    "mysterious"             : "mysterious surreal",
    "wild"                   : "wild raw",
    "cozy"                   : "cozy warm",

    "modern"                 : "modern urban",
    "nostalgic"              : "nostalgic historic",
    "spiritual"              : "spiritual mindful",

    "rustic"                 : "rustic simple",
    "picturesque"            : "picturesque scenic",
    "bohemian"               : "bohemian artistic",
}

CONSTRAINT = {
    "day trip"               : "day trip short",
    "weekend"                : "weekend trip",
    "long stay"              : "long stay",

    "backpacking"            : "backpacking budget",
    "luxury"                 : "luxury travel",
    "mid range"              : "mid range",
    "eco travel"             : "eco travel",

    "solo"                   : "solo travel",
    "couple"                 : "couple travel",
    "family"                 : "family travel",
    "group"                  : "group travel",
    "corporate"              : "corporate travel",

    "pet friendly"           : "pet friendly",
}

ALL_TAGS: dict[str, str] = {
    **ENVIRONMENT,
    **CULTURE,
    **ACTIVITIES,
    **FOOD,
    **VIBE,
    **CONSTRAINT,
}