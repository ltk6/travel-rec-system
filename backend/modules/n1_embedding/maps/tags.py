"""
maps/tags.py
============
Normalizes quiz/user tags (Vietnamese or English) into rich English travel
keyword strings that embed well with BGE-M3.

Tags arrive from two sources:
  1. Quiz answers  (e.g. "thiên nhiên", "biển", "gia đình")
  2. User-typed tags  (free-form, mixed language)

All values are English travel keyword phrases for semantic alignment with
location profile vectors in the database.
"""

# ─────────────────────────────────────────────────────────────
# NATURE & LANDSCAPE
# ─────────────────────────────────────────────────────────────
NATURE_TAGS: dict[str, str] = {
    # Vietnamese → English
    "thiên nhiên":          "nature outdoor greenery scenic landscape",
    "biển":                 "beach coastal sea ocean surf wave sand",
    "núi":                  "mountain highland altitude peak summit trail",
    "rừng":                 "forest jungle eco-tourism canopy wildlife",
    "thác nước":            "waterfall cascade scenic nature photography",
    "hồ":                   "lake calm serene boating reflection scenic",
    "hang động":            "cave exploration geological adventure underground",
    "đảo":                  "island tropical isolated beach snorkeling reef",
    "đồng bằng":            "plains flatland pastoral countryside open",
    "đồi":                  "hill rolling-hills meadow green scenic walk",
    "suối":                 "stream creek freshwater cool nature scenic",
    "vịnh":                 "bay cove sheltered beach snorkeling scenic",
    "bán đảo":              "peninsula coastal cliffs scenic ocean view",
    "cao nguyên":           "plateau highland grassland scenic wide-open",
    "sa mạc":               "desert dunes arid vast unique landscape",
    "đồng lúa":             "rice-field paddy rural pastoral landscape",
    "vườn quốc gia":        "national-park wildlife conservation trekking eco",
    "khu bảo tồn":          "nature-reserve conservation wildlife sanctuary",
    "rừng ngập mặn":        "mangrove eco-tourism kayak birdwatching nature",
    "san hô":               "coral-reef diving snorkeling marine tropical",

    # English → enriched English
    "nature":               "nature outdoor scenic greenery landscape fresh-air",
    "beach":                "beach coastal ocean wave sand sun surf",
    "mountain":             "mountain highland trek summit trail peak altitude",
    "forest":               "forest jungle eco canopy wildlife trees",
    "waterfall":            "waterfall cascade scenic nature photography hiking",
    "lake":                 "lake serene calm boating rowing reflection",
    "cave":                 "cave underground exploration geological adventure",
    "island":               "island tropical isolated beach snorkeling reef",
    "hill":                 "hill rolling meadow green walk scenic countryside",
    "river":                "river boat cruise kayak scenic waterway",
    "sea":                  "sea ocean coastal beach surf horizon",
    "desert":               "desert dunes arid vast unique landscape camel",
    "jungle":               "jungle rainforest eco-tourism wildlife trekking dense",
    "valley":               "valley scenic gorge panoramic highland hiking",
    "cliff":                "cliff coastal dramatic viewpoint scenic photography",
    "wetland":              "wetland birdwatching eco-tourism nature serene",
    "national park":        "national-park wildlife conservation trekking hiking",
    "eco":                  "eco-tourism sustainable nature conservation wildlife",
}

# ─────────────────────────────────────────────────────────────
# URBAN & CULTURAL
# ─────────────────────────────────────────────────────────────
URBAN_TAGS: dict[str, str] = {
    # Vietnamese
    "thành phố":            "city urban metropolitan shopping nightlife vibrant modern",
    "làng quê":             "countryside village rural pastoral traditional quiet",
    "phố cổ":               "old-town heritage historic architecture charming cobblestone",
    "chùa":                 "temple pagoda spiritual meditation Buddhism sacred",
    "đình":                 "communal-house heritage traditional Vietnamese sacred",
    "nhà thờ":              "church cathedral colonial architecture historic spiritual",
    "bảo tàng":             "museum history heritage education exhibit cultural",
    "chợ":                  "market local vendor food craft shopping authentic",
    "chợ đêm":              "night-market street-food vendor local shopping evening",
    "phố đi bộ":            "pedestrian-street walking lively street-food shopping",
    "khu phố Tây":          "expat-area international nightlife cafe bar",
    "làng nghề":            "craft-village artisan traditional handmade workshop",
    "lễ hội":               "festival celebration local tradition culture crowd",
    "ẩm thực":              "food gastronomy culinary local-cuisine street-food",
    "nghệ thuật":           "art gallery creative exhibition museum cultural",
    "kiến trúc":            "architecture historic building design landmark",
    "di tích":              "heritage-site historic monument ancient ruin cultural",
    "văn hóa":              "cultural heritage local tradition festival community",
    "lịch sử":              "history heritage ancient monument museum educational",
    "phong tục":            "local-custom tradition culture authentic immersive",
    "tôn giáo":             "spiritual religious sacred pilgrimage cultural",
    "âm nhạc":              "music live-music concert festival performance",
    "múa":                  "dance performance cultural traditional festival",
    "sân khấu":             "theater performance show cultural entertainment",
    "rạp chiếu phim":       "cinema entertainment indoor city leisure",

    # English
    "city":                 "city urban metropolitan shopping nightlife vibrant",
    "village":              "village rural countryside traditional community",
    "old town":             "old-town heritage historic charming cobblestone",
    "temple":               "temple spiritual sacred meditation heritage",
    "museum":               "museum history heritage education exhibit",
    "market":               "market local vendor food craft shopping",
    "festival":             "festival celebration local tradition crowd cultural",
    "cultural":             "cultural heritage local tradition community",
    "heritage":             "heritage historic ancient architecture preservation",
    "history":              "history ancient monument heritage educational museum",
    "art":                  "art gallery creative museum exhibition cultural",
    "architecture":         "architecture design landmark historic building",
    "street food":          "street-food local vendor market authentic cheap",
    "local cuisine":        "local-cuisine authentic gastronomy culinary flavour",
    "craft":                "craft artisan handmade workshop traditional souvenir",
    "nightlife":            "nightlife bar club entertainment social vibrant evening",
    "shopping":             "shopping market souvenir local boutique mall",
    "spiritual":            "spiritual meditation sacred pilgrimage temple retreat",
}

# ─────────────────────────────────────────────────────────────
# ACTIVITIES & EXPERIENCES
# ─────────────────────────────────────────────────────────────
ACTIVITY_TAGS: dict[str, str] = {
    # Vietnamese
    "leo núi":              "mountain trekking hiking summit trail climbing",
    "lặn biển":             "diving scuba snorkeling coral reef underwater marine",
    "cắm trại":             "camping outdoor wilderness nature campfire stars",
    "dã ngoại":             "picnic outdoor nature countryside fresh-air",
    "chèo kayak":           "kayaking paddle water river lake adventure",
    "lướt sóng":            "surfing wave beach sport water adventure",
    "bơi lội":              "swimming beach pool water outdoor",
    "đi bộ":                "walking hiking trail nature scenic gentle",
    "đạp xe":               "cycling bike ride scenic countryside road-trip",
    "cưỡi ngựa":            "horse-riding countryside outdoor scenic leisure",
    "chụp ảnh":             "photography scenic viewpoint landscape artistic",
    "check-in":             "scenic photogenic viewpoint instagram aesthetic",
    "spa":                  "spa massage wellness relaxation body-treatment",
    "yoga":                 "yoga meditation wellness mindfulness retreat",
    "nấu ăn":               "cooking-class culinary food culture local",
    "câu cá":               "fishing boat lake river local tranquil",
    "ngắm sao":             "stargazing astronomy dark-sky rural night",
    "hot spring":           "hot-spring thermal bath wellness relaxation mineral",
    "zipline":              "zipline canopy adventure adrenaline outdoor",
    "paragliding":          "paragliding aerial view adventure adrenaline",
    "đi thuyền":            "boat-cruise river lake scenic tour water",
    "chèo thuyền":          "rowing boat paddle serene water",
    "thăm quan":            "sightseeing tour guided heritage city-tour",
    "mua sắm":              "shopping market souvenir boutique local",
    "ăn uống":              "dining food local-cuisine restaurant tasting",

    # English
    "trekking":             "trekking hiking mountain trail outdoor nature",
    "diving":               "diving scuba snorkeling coral reef underwater",
    "camping":              "camping outdoor wilderness nature fire stars",
    "kayaking":             "kayaking paddle water river adventure",
    "surfing":              "surfing wave beach sport water adrenaline",
    "cycling":              "cycling bike scenic countryside road",
    "photography":          "photography scenic viewpoint landscape artistic",
    "yoga":                 "yoga meditation wellness mindfulness retreat",
    "cooking class":        "cooking-class culinary local food experience",
    "fishing":              "fishing boat tranquil river lake local",
    "stargazing":           "stargazing dark-sky astronomy rural night",
    "zip line":             "zipline canopy adventure adrenaline outdoor",
    "boat cruise":          "boat-cruise scenic river lake water tour",
    "sightseeing":          "sightseeing tour guided heritage landmark",
    "wine tasting":         "wine-tasting vineyard gourmet fine-dining",
    "rock climbing":        "rock-climbing sport outdoor adventure challenge",
    "snorkeling":           "snorkeling reef tropical marine shallow water",
    "hot spring":           "hot-spring thermal mineral wellness relaxation",
}

# ─────────────────────────────────────────────────────────────
# ACCOMMODATION & COMFORT
# ─────────────────────────────────────────────────────────────
ACCOMMODATION_TAGS: dict[str, str] = {
    # Vietnamese
    "resort":               "resort luxury beachfront amenities pool service",
    "homestay":             "homestay local community authentic cultural",
    "nhà nghỉ":             "guesthouse budget affordable simple rest",
    "khách sạn":            "hotel comfort service amenities city",
    "villa":                "villa private luxury pool quiet exclusive",
    "glamping":             "glamping outdoor luxury nature scenic camping",
    "hostel":               "hostel budget social backpacker dorm community",
    "bungalow":             "bungalow tropical beach private nature",
    "nhà gỗ":               "wooden-cabin nature rustic retreat countryside",
    "căn hộ":               "apartment self-catering kitchen city comfortable",

    # English
    "hotel":                "hotel comfort amenities service city",
    "resort":               "resort luxury pool beachfront amenities",
    "villa":                "villa private pool exclusive luxury quiet",
    "homestay":             "homestay local authentic community cultural immersive",
    "hostel":               "hostel budget social backpacker community",
    "camping":              "camping outdoor nature wilderness tent",
    "glamping":             "glamping luxury outdoor scenic nature",
    "cabin":                "cabin rustic nature retreat woodland",
    "bungalow":             "bungalow tropical beach private peaceful",
    "treehouse":            "treehouse unique nature adventure elevated",
    "overwater bungalow":   "overwater-bungalow tropical reef luxury romantic",
}

# ─────────────────────────────────────────────────────────────
# MOOD & ATMOSPHERE
# ─────────────────────────────────────────────────────────────
ATMOSPHERE_TAGS: dict[str, str] = {
    # Vietnamese
    "yên tĩnh":             "quiet peaceful tranquil secluded serene silent",
    "đông vui":             "lively crowded vibrant social bustling energetic",
    "lãng mạn":             "romantic intimate scenic sunset couple private",
    "bình yên":             "peaceful calm serene gentle nature retreat",
    "hoang sơ":             "untouched wild pristine remote off-beaten-path",
    "huyền bí":             "mysterious atmospheric misty ethereal spiritual",
    "cổ kính":              "heritage ancient traditional atmospheric historic",
    "hiện đại":             "modern contemporary urban sleek design",
    "ấm cúng":              "cozy warm intimate comfortable homey",
    "thoáng đãng":          "open airy spacious panoramic wide scenic",
    "náo nhiệt":            "lively noisy energetic vibrant urban social",
    "thơ mộng":             "poetic scenic dreamy romantic picturesque",
    "gần gũi thiên nhiên":  "immersed-in-nature eco green outdoor fresh-air",

    # English
    "quiet":                "quiet peaceful tranquil secluded serene",
    "lively":               "lively vibrant social crowded energetic",
    "romantic":             "romantic scenic sunset intimate couple",
    "peaceful":             "peaceful calm serene nature gentle retreat",
    "mysterious":           "mysterious atmospheric misty foggy ethereal",
    "cozy":                 "cozy warm intimate comfortable indoor",
    "modern":               "modern contemporary urban design sleek",
    "rustic":               "rustic traditional wooden countryside charm",
    "luxurious":            "luxury premium exclusive upscale refined",
    "minimalist":           "minimalist clean simple calm uncluttered",
    "photogenic":           "photogenic scenic viewpoint aesthetic instagram",
    "hidden gem":           "hidden-gem off-beaten-path discovery unique local",
    "off the beaten path":  "remote off-beaten-path undiscovered unique",
    "instagrammable":       "photogenic scenic viewpoint aesthetic colorful",

    # Vietnamese social / group tags (commonly used as quiz answers)
    "cặp đôi":              "romantic couple private intimate sunset scenic",
    "vợ chồng":             "couple romantic private intimate scenic resort",
    "gia đình":             "family kid-friendly safe educational activities",
    "trẻ em":   "family kid-safe educational shallow-beach fun accessible",
    "bạn bè":               "group social fun nightlife adventure flexible",
    "một mình":             "solo independent flexible self-paced peaceful",
    "nhóm":                 "group social activities variety flexible",
    "vui vẻ":               "fun lively cheerful social activities entertainment",
    "thư giãn":             "relaxation slow rest spa wellness peaceful",
    "sang trọng":           "luxury upscale premium resort fine-dining exclusive",
    "bình dân":             "affordable mid-range comfortable local value",
}

# ─────────────────────────────────────────────────────────────
# MASTER REGISTRY
# ─────────────────────────────────────────────────────────────
ALL_TAGS: dict[str, str] = {
    **NATURE_TAGS,
    **URBAN_TAGS,
    **ACTIVITY_TAGS,
    **ACCOMMODATION_TAGS,
    **ATMOSPHERE_TAGS,
}