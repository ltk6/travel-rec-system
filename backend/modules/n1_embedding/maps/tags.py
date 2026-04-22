"""
maps/tags.py
============
Normalizes quiz/user tags (Vietnamese or English) into rich English travel
keyword strings that embed well with BGE-M3.

Tags arrive from two sources:
  1. Quiz answers  (e.g. "thiên nhiên", "biển", "gia đình")
  2. Location database labels  (applied by the content team when building locations)

All values are English travel keyword phrases for semantic alignment between
user-preference vectors and location-profile vectors in the database.

─────────────────────────────────────────────────────────────
SECTION INDEX
─────────────────────────────────────────────────────────────
  A. NATURE & LANDSCAPE           — terrain, ecosystem, water, sky
  B. URBAN & CULTURAL             — city life, heritage, food, arts
  C. ACTIVITIES & EXPERIENCES     — sports, exploration, learning
  D. ACCOMMODATION & FACILITIES   — stay types, amenities
  E. MOOD & ATMOSPHERE            — vibe, aesthetic, ambience
  F. TRAVEL STYLE & TRIP TYPE     — how people travel
  G. SOCIAL GROUP & PARTY TYPE    — who is travelling
  H. BUDGET & PRICE TIER          — cost sensitivity
  I. GEOGRAPHY & REGION           — location descriptors (VN-focused + global)
  J. SEASON & WEATHER SUITABILITY — best-time-to-visit labels
  K. ACCESSIBILITY & COMFORT      — mobility, age, health
  L. SUSTAINABILITY & ETHICS      — eco, responsible tourism
  M. PHOTOGRAPHY & CONTENT        — visual / social-media value
  N. FOOD & DRINK                 — cuisine, dietary, beverage
  O. WELLNESS & HEALTH            — body, mind, spiritual care
  P. EVENTS & FESTIVALS           — time-bound attractions
  Q. NIGHTLIFE & ENTERTAINMENT    — evening / night options
  R. WATER ACTIVITIES             — sea, river, lake sports
  S. LAND SPORTS & ADVENTURE      — terrain-based activity
  T. AIR & EXTREME SPORTS         — high-adrenaline / aerial
  U. KIDS & FAMILY AMENITIES      — child-specific features
  V. PETS & ANIMALS               — wildlife, farm, pet-friendly
  W. ROMANCE & COUPLES            — couple-specific experiences
  X. EDUCATION & LEARNING         — study, workshop, immersive

NOTE FOR LOCATION DATABASE TEAM
──────────────────────────────────────────────────────────────────────────
  • Apply tags liberally — a location can hold dozens of tags.
  • Use the EXACT key strings (left side) when tagging locations.
  • Prefer Vietnamese keys for Vietnamese domestic destinations.
  • Prefer English keys for internationally-described destinations.
  • Add new keys to the appropriate section rather than creating ad-hoc strings.
  • When a new key is added here, also rebuild the vector index.
──────────────────────────────────────────────────────────────────────────
"""

# ═════════════════════════════════════════════════════════════
# A. NATURE & LANDSCAPE
# ═════════════════════════════════════════════════════════════

NATURE_TAGS: dict[str, str] = {
    # ── Terrain / landform ──────────────────────────────────
    "thiên nhiên":          "nature outdoor greenery scenic landscape",
    "núi":                  "mountain highland altitude peak summit trail",
    "đồi":                  "hill rolling-hills meadow green scenic walk",
    "cao nguyên":           "plateau highland grassland scenic wide-open altitude",
    "đồng bằng":            "plains flatland pastoral countryside open",
    "thung lũng":           "valley gorge panoramic highland scenic hiking",
    "vách đá":              "cliff coastal dramatic viewpoint scenic photography",
    "hang động":            "cave exploration geological adventure underground",
    "sa mạc":               "desert dunes arid vast unique landscape",
    "đồng lúa":             "rice-field paddy rural pastoral landscape green",
    "vùng đất ngập nước":   "wetland birdwatching eco-tourism nature serene",

    # ── Water bodies ────────────────────────────────────────
    "biển":                 "beach coastal sea ocean surf wave sand",
    "vịnh":                 "bay cove sheltered beach snorkeling scenic",
    "đảo":                  "island tropical isolated beach snorkeling reef",
    "bán đảo":              "peninsula coastal cliffs scenic ocean view",
    "hồ":                   "lake calm serene boating reflection scenic",
    "sông":                 "river boat cruise kayak scenic waterway",
    "suối":                 "stream creek freshwater cool nature scenic",
    "thác nước":            "waterfall cascade scenic nature photography",
    "rừng ngập mặn":        "mangrove eco-tourism kayak birdwatching nature",
    "san hô":               "coral-reef diving snorkeling marine tropical",
    "đầm phá":              "lagoon calm sheltered water fishing scenic",
    "mạch nước nóng":       "hot-spring thermal mineral water wellness relaxation",

    # ── Vegetation / ecosystem ──────────────────────────────
    "rừng":                 "forest jungle eco-tourism canopy wildlife trees",
    "rừng nhiệt đới":       "rainforest tropical dense canopy wildlife eco",
    "vườn quốc gia":        "national-park wildlife conservation trekking eco",
    "khu bảo tồn":          "nature-reserve conservation wildlife sanctuary",
    "rừng thông":           "pine-forest highland cool aromatic scenic walk",
    "đồng cỏ":              "grassland meadow open-air scenic mild nature",
    "vườn hoa":             "flower-garden bloom colorful scenic photography",
    "vườn trà":             "tea-plantation highland green rows scenic cultural",
    "vườn cà phê":          "coffee-plantation highland culture local experience",

    # ── Sky / atmosphere ────────────────────────────────────
    "bầu trời sao":         "stargazing dark-sky astronomy rural night clear",
    "bình minh":            "sunrise early-morning golden scenic photography",
    "hoàng hôn":            "sunset golden-hour scenic romantic photography",
    "sương mù":             "misty foggy atmospheric ethereal highland scenic",
    "mây":                  "cloud highland misty ethereal scenic dramatic",

    # ── English equivalents / aliases ───────────────────────
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
    "desert":               "desert dunes arid vast unique landscape",
    "jungle":               "jungle rainforest eco-tourism wildlife trekking dense",
    "valley":               "valley scenic gorge panoramic highland hiking",
    "cliff":                "cliff coastal dramatic viewpoint scenic photography",
    "wetland":              "wetland birdwatching eco-tourism nature serene",
    "national park":        "national-park wildlife conservation trekking hiking",
    "eco":                  "eco-tourism sustainable nature conservation wildlife",
    "highland":             "highland cool mountain plateau scenic altitude",
    "tropical":             "tropical warm lush beach island palm humid",
    "coastal":              "coastal beach ocean shoreline scenic breeze",
    "hot spring":           "hot-spring thermal bath wellness relaxation mineral",
    "rice field":           "rice-field paddy rural pastoral green landscape",
    "mangrove":             "mangrove eco kayak birdwatching nature waterway",
    "coral reef":           "coral-reef diving snorkeling marine tropical reef",
    "lagoon":               "lagoon calm sheltered turquoise scenic photography",
    "pine forest":          "pine-forest highland cool scenic aromatic walk",
    "tea plantation":       "tea-plantation highland rows green scenic cultural",
    "flower garden":        "flower-garden bloom colorful scenic photography",
    "sunrise":              "sunrise early golden scenic photography peaceful",
    "sunset":               "sunset golden romantic scenic photography couples",
    "stargazing":           "stargazing dark-sky astronomy rural night",
    "fog":                  "foggy misty atmospheric ethereal highland scenic",
}


# ═════════════════════════════════════════════════════════════
# B. URBAN & CULTURAL
# ═════════════════════════════════════════════════════════════

URBAN_TAGS: dict[str, str] = {
    # ── Settlement type ─────────────────────────────────────
    "thành phố":            "city urban metropolitan shopping nightlife vibrant modern",
    "làng quê":             "countryside village rural pastoral traditional quiet",
    "phố cổ":               "old-town heritage historic architecture charming cobblestone",
    "thị trấn":             "small-town local charm community quiet authentic",
    "khu đô thị mới":       "new-district modern urban amenities infrastructure",

    # ── Religious & heritage sites ──────────────────────────
    "chùa":                 "temple pagoda spiritual meditation Buddhism sacred",
    "đình":                 "communal-house heritage traditional Vietnamese sacred",
    "đền":                  "shrine sacred spiritual pilgrimage heritage Vietnamese",
    "nhà thờ":              "church cathedral colonial architecture historic spiritual",
    "thánh địa":            "holy-site pilgrimage sacred religious heritage",
    "di tích":              "heritage-site historic monument ancient ruin cultural",
    "cố đô":                "ancient-capital imperial palace heritage history",
    "lăng tẩm":             "royal-tomb mausoleum heritage imperial history scenic",

    # ── Museums & galleries ─────────────────────────────────
    "bảo tàng":             "museum history heritage education exhibit cultural",
    "gallery":              "art-gallery contemporary exhibit creative cultural",
    "trung tâm văn hóa":    "cultural-center performance exhibition community",

    # ── Markets & commerce ──────────────────────────────────
    "chợ":                  "market local vendor food craft shopping authentic",
    "chợ đêm":              "night-market street-food vendor local shopping evening",
    "chợ nổi":              "floating-market river boat local produce unique",
    "phố đi bộ":            "pedestrian-street walking lively street-food shopping",
    "trung tâm thương mại": "shopping-mall retail modern air-conditioned city",

    # ── Craft & living culture ──────────────────────────────
    "làng nghề":            "craft-village artisan traditional handmade workshop",
    "làng gốm":             "pottery-village craft artisan ceramic traditional",
    "làng tranh":           "painting-village art folk-art craft traditional",
    "làng dệt":             "weaving-village textile craft ethnic traditional",
    "lễ hội":               "festival celebration local tradition culture crowd",
    "phong tục":            "local-custom tradition culture authentic immersive",

    # ── Arts & performance ──────────────────────────────────
    "nghệ thuật":           "art gallery creative exhibition museum cultural",
    "âm nhạc":              "music live-music concert festival performance",
    "múa rối nước":         "water-puppet traditional performing-art Vietnamese heritage",
    "hát bội":              "traditional-opera folk-art heritage performance",
    "sân khấu":             "theater performance show cultural entertainment",
    "opera":                "opera classical performance venue fine-arts",

    # ── Architecture ────────────────────────────────────────
    "kiến trúc":            "architecture historic building design landmark",
    "kiến trúc Pháp":       "french-colonial architecture heritage elegant historic",
    "kiến trúc Chăm":       "cham-tower ancient ruins heritage sculpture red-brick",
    "phố Tây":              "expat-area international bar café nightlife street",

    # ── English equivalents ─────────────────────────────────
    "city":                 "city urban metropolitan shopping nightlife vibrant",
    "village":              "village rural countryside traditional community",
    "old town":             "old-town heritage historic charming cobblestone",
    "temple":               "temple spiritual sacred meditation heritage",
    "pagoda":               "pagoda Buddhist sacred spiritual peaceful heritage",
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
    "night market":         "night-market street-food local vendor evening lively",
    "floating market":      "floating-market river boat local unique cultural",
    "water puppet":         "water-puppet traditional performance Vietnamese heritage",
    "colonial":             "colonial architecture heritage elegant historic period",
    "culture":              "cultural heritage tradition local experience community",
    "local":                "local authentic daily-life community culture experience",
    "authentic":            "authentic local traditional immersive cultural",
    "pilgrimage":           "pilgrimage sacred spiritual religious heritage holy",
}


# ═════════════════════════════════════════════════════════════
# C. ACTIVITIES & EXPERIENCES
# ═════════════════════════════════════════════════════════════

ACTIVITY_TAGS: dict[str, str] = {
    # ── Trekking & hiking ────────────────────────────────────
    "leo núi":              "mountain trekking hiking summit trail climbing",
    "đi bộ đường dài":      "trekking multi-day trail mountain wilderness camping",
    "đi bộ":                "walking hiking trail nature scenic gentle stroll",
    "leo thác":             "waterfall-trekking nature trail wet adventure",

    # ── Water sports ────────────────────────────────────────
    "lặn biển":             "diving scuba snorkeling coral reef underwater marine",
    "lặn snorkel":          "snorkeling reef tropical marine shallow-water",
    "chèo kayak":           "kayaking paddle water river lake adventure",
    "chèo thuyền":          "rowing boat paddle serene water",
    "lướt sóng":            "surfing wave beach sport water adventure",
    "bơi lội":              "swimming beach pool water outdoor",
    "đi thuyền":            "boat-cruise river lake scenic tour water",
    "câu cá":               "fishing boat lake river local tranquil",
    "chèo SUP":             "stand-up-paddleboard SUP water coastal calm balance",
    "wakeboard":            "wakeboarding water-sport lake thrill speed",
    "bơi hang":             "cave-swimming underground cool unique adventure",

    # ── Land sports ─────────────────────────────────────────
    "đạp xe":               "cycling bike ride scenic countryside road-trip",
    "cưỡi ngựa":            "horse-riding countryside outdoor scenic leisure",
    "leo vách đá":          "rock-climbing sport outdoor adventure challenge",
    "zipline":              "zipline canopy adventure adrenaline outdoor",
    "cắm trại":             "camping outdoor wilderness nature campfire stars",
    "dã ngoại":             "picnic outdoor nature countryside fresh-air relaxed",
    "đi jeep":              "jeep-tour off-road adventure highland rural terrain",
    "trượt cát":            "sandboarding dune sand adventure",
    "đua moto":             "motorbike-trail adventure scenic rural road-trip",

    # ── Air / extreme ────────────────────────────────────────
    "dù lượn":              "paragliding aerial view adventure adrenaline scenic",
    "nhảy dù":              "skydiving extreme adrenaline freefall aerial",
    "khinh khí cầu":        "hot-air-balloon aerial scenic sunrise romantic",

    # ── Wildlife & nature watching ───────────────────────────
    "ngắm chim":            "birdwatching binoculars wetland nature eco quiet",
    "xem động vật hoang dã":"wildlife-safari animals nature eco observation",
    "thăm vườn thú":        "zoo animals family educational entertainment",
    "snorkling rạn san hô": "snorkeling coral marine ecosystem colorful reef",

    # ── Learning & creative ──────────────────────────────────
    "nấu ăn":               "cooking-class culinary food culture local hands-on",
    "học tiếng Việt":       "language-class culture immersive local Vietnamese",
    "vẽ tranh":             "painting-class art creative workshop cultural",
    "làm gốm":              "pottery-class craft hands-on artisan traditional",
    "làm bánh":             "baking-class culinary hands-on local food",

    # ── Photography & content ───────────────────────────────
    "chụp ảnh":             "photography scenic viewpoint landscape artistic",
    "check-in":             "scenic photogenic viewpoint instagram aesthetic",
    "quay phim":            "videography scenic drone cinematic landscape",

    # ── Wellness ────────────────────────────────────────────
    "spa":                  "spa massage wellness relaxation body-treatment",
    "yoga":                 "yoga meditation wellness mindfulness retreat",
    "thiền":                "meditation mindfulness silent retreat wellness spiritual",
    "tắm bùn":              "mud-bath mineral wellness spa relax therapeutic",
    "tắm suối khoáng":      "mineral-spring thermal bath wellness relaxation",
    "ngắm sao":             "stargazing astronomy dark-sky rural night clear",

    # ── Shopping & souvenir ──────────────────────────────────
    "mua sắm":              "shopping market souvenir boutique local",
    "thời trang":           "fashion boutique local design shopping",
    "thủ công mỹ nghệ":     "handicraft souvenir traditional artisan shop",

    # ── Culinary experiences ─────────────────────────────────
    "ăn uống":              "dining food local-cuisine restaurant tasting",
    "thử ẩm thực":          "food-tasting culinary tour local street market",
    "coffee tour":          "coffee plantation tasting highland culture",

    # ── Sightseeing ─────────────────────────────────────────
    "thăm quan":            "sightseeing tour guided heritage city-tour",
    "du ngoạn":             "scenic tour guided drive nature landscape",

    # ── English equivalents ─────────────────────────────────
    "trekking":             "trekking hiking mountain trail outdoor nature",
    "diving":               "diving scuba snorkeling coral reef underwater",
    "camping":              "camping outdoor wilderness nature fire stars",
    "kayaking":             "kayaking paddle water river adventure",
    "surfing":              "surfing wave beach sport water adrenaline",
    "cycling":              "cycling bike scenic countryside road",
    "photography":          "photography scenic viewpoint landscape artistic",
    "cooking class":        "cooking-class culinary local food experience",
    "fishing":              "fishing boat tranquil river lake local",
    "zip line":             "zipline canopy adventure adrenaline outdoor",
    "boat cruise":          "boat-cruise scenic river lake water tour",
    "sightseeing":          "sightseeing tour guided heritage landmark",
    "wine tasting":         "wine-tasting vineyard gourmet fine-dining",
    "rock climbing":        "rock-climbing sport outdoor adventure challenge",
    "snorkeling":           "snorkeling reef tropical marine shallow water",
    "paragliding":          "paragliding aerial view adventure adrenaline",
    "hot air balloon":      "hot-air-balloon aerial scenic sunrise romantic",
    "birdwatching":         "birdwatching nature eco wetland binoculars quiet",
    "pottery class":        "pottery-class craft hands-on artisan creative",
    "painting class":       "painting-class art creative workshop cultural",
    "sandboarding":         "sandboarding dune adventure fun scenic",
    "mudskipper":           "mud-bath mineral spa wellness therapeutic relax",
    "meditation":           "meditation mindfulness silent retreat wellness spiritual",
    "yoga retreat":         "yoga retreat wellness mindfulness healing nature peaceful",
    "adventure":            "adventure outdoor exploration adrenaline active",
    "relax":                "relaxation spa wellness slow peaceful rest",
    "hiking":               "hiking trail mountain nature outdoor scenic",
    "wildlife":             "wildlife animals safari nature eco observation",
    "motorbike tour":       "motorbike scenic rural road-trip adventure freedom",
    "jeep tour":            "jeep off-road highland rural terrain adventure",
    "mud bath":             "mud-bath mineral wellness spa therapeutic relax",
    "cave swimming":        "cave-swimming underground cool unique adventure",
    "SUP":                  "stand-up-paddleboard water coastal calm balance sport",
}


# ═════════════════════════════════════════════════════════════
# D. ACCOMMODATION & FACILITIES
# ═════════════════════════════════════════════════════════════

ACCOMMODATION_TAGS: dict[str, str] = {
    # ── Stay types ───────────────────────────────────────────
    "khách sạn":            "hotel comfort amenities service city",
    "resort":               "resort luxury pool beachfront amenities service",
    "villa":                "villa private pool exclusive luxury quiet",
    "homestay":             "homestay local authentic community cultural immersive",
    "nhà nghỉ":             "guesthouse budget simple local affordable",
    "hostel":               "hostel budget social backpacker community dorm",
    "bungalow":             "bungalow tropical beach private peaceful",
    "glamping":             "glamping luxury outdoor scenic nature comfort",
    "nhà trên cây":         "treehouse unique nature adventure elevated scenic",
    "căn hộ":               "apartment self-catering city urban flexible",
    "nhà thuyền":           "floating-house water river lake unique local",
    "camping":              "camping outdoor nature wilderness tent",
    "ecolodge":             "ecolodge sustainable nature immersive rustic comfort",
    "boutique hotel":       "boutique-hotel design intimate character local style",
    "capsule hotel":        "capsule-hotel budget efficient modern city",

    # ── Key amenities ────────────────────────────────────────
    "hồ bơi":               "swimming-pool resort luxury outdoor leisure",
    "bãi biển riêng":       "private-beach exclusive resort luxury",
    "spa & wellness":       "spa wellness massage therapy relaxation retreat",
    "nhà hàng":             "restaurant dining food on-site cuisine",
    "xe đưa đón":           "airport-transfer shuttle convenience service",
    "wifi tốt":             "fast-wifi digital-nomad remote-work connectivity",
    "phòng gym":            "gym fitness workout health amenities",
    "trẻ em vui chơi":      "kids-club playground family-friendly safe children",
    "thân thiện với thú cưng": "pet-friendly accommodation travel dog cat",
    "phòng họp":            "meeting-room business conference corporate",

    # ── English aliases ──────────────────────────────────────
    "hotel":                "hotel comfort amenities service city",
    "guesthouse":           "guesthouse budget simple local affordable",
    "villa":                "villa private pool exclusive luxury quiet",
    "homestay":             "homestay local authentic community cultural immersive",
    "treehouse":            "treehouse unique nature adventure elevated",
    "overwater bungalow":   "overwater-bungalow tropical reef luxury romantic",
    "cabin":                "cabin rustic nature retreat woodland cozy",
    "ecolodge":             "ecolodge sustainable nature immersive rustic",
    "private pool":         "private-pool villa luxury exclusive intimate",
    "private beach":        "private-beach resort exclusive luxury scenic",
    "pet friendly":         "pet-friendly accommodation travel dog cat",
    "digital nomad":        "wifi coworking remote-work flexible city café",
    "co-working":           "coworking wifi digital-nomad workspace café",
}


# ═════════════════════════════════════════════════════════════
# E. MOOD & ATMOSPHERE
# ═════════════════════════════════════════════════════════════

ATMOSPHERE_TAGS: dict[str, str] = {
    # ── Tranquil / restful ──────────────────────────────────
    "yên tĩnh":             "quiet peaceful tranquil secluded serene silent",
    "bình yên":             "peaceful calm serene nature gentle retreat",
    "thanh thản":           "tranquil serene mindful calm restorative",
    "cô đọng":              "secluded remote private quiet hidden",
    "ẩn mình":              "hidden-gem off-beaten-path undiscovered quiet local",

    # ── Lively / social ─────────────────────────────────────
    "sôi động":             "vibrant lively energetic social crowd entertainment",
    "vui vẻ":               "fun lively cheerful social activities entertainment",
    "nhộn nhịp":            "bustling lively crowded vibrant social market city",
    "náo nhiệt":            "festive lively loud energetic social party",

    # ── Romantic ────────────────────────────────────────────
    "lãng mạn":             "romantic sunset couple private intimate scenic",
    "thơ mộng":             "dreamy picturesque scenic poetic gentle beautiful",

    # ── Mysterious / dramatic ────────────────────────────────
    "huyền bí":             "mysterious atmospheric misty fog ethereal dramatic",
    "hùng vĩ":              "grand majestic dramatic vast imposing scenic",
    "hoang dã":             "wild untamed remote raw nature rugged",
    "nguyên sinh":          "pristine untouched primary-forest pure remote nature",

    # ── Cozy / warm ─────────────────────────────────────────
    "ấm cúng":              "cozy warm intimate comfortable indoor fireside",
    "thân mật":             "intimate private cozy warm personal",

    # ── Modern / design ─────────────────────────────────────
    "hiện đại":             "modern contemporary urban design sleek",
    "sang trọng":           "luxury premium exclusive upscale refined elegant",
    "tối giản":             "minimalist clean simple calm uncluttered refined",

    # ── Nostalgic / rustic ──────────────────────────────────
    "cổ kính":              "vintage antique old-world nostalgic charm historic",
    "mộc mạc":              "rustic traditional wooden countryside charm authentic",
    "hoài cổ":              "retro nostalgic vintage old-world sentimental charm",

    # ── Visual / aesthetic ──────────────────────────────────
    "đẹp như tranh":        "picturesque scenic beautiful photography-worthy stunning",
    "nhiều màu sắc":        "colorful vibrant photogenic aesthetic visual",
    "instagrammable":       "photogenic scenic viewpoint aesthetic colorful instagram",
    "hidden gem":           "hidden-gem off-beaten-path discovery unique local",

    # ── English equivalents ─────────────────────────────────
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
    "off the beaten path":  "remote off-beaten-path undiscovered unique",
    "hidden gem":           "hidden-gem off-beaten-path discovery unique local",
    "wild":                 "wild untamed remote raw nature rugged",
    "pristine":             "pristine untouched pure remote nature unspoiled",
    "dramatic":             "dramatic grand majestic vast imposing scenic",
    "fun":                  "fun lively entertaining social enjoyable activities",
    "vibrant":              "vibrant lively energetic colorful urban nightlife",
    "adrenaline":           "adrenaline thrilling exciting extreme adventure",
    "relaxation":           "relaxation peaceful calm slow wellness rest",
    "secluded":             "secluded private quiet remote peaceful",
    "nostalgic":            "nostalgic vintage retro old-world sentimental charm",
    "picturesque":          "picturesque scenic beautiful photography-worthy",
    "colorful":             "colorful vibrant visual photography aesthetic",
}


# ═════════════════════════════════════════════════════════════
# F. TRAVEL STYLE & TRIP TYPE
# ═════════════════════════════════════════════════════════════

TRAVEL_STYLE_TAGS: dict[str, str] = {
    # ── Duration ────────────────────────────────────────────
    "cuối tuần":            "weekend short-trip nearby compact quick-getaway",
    "chuyến ngắn":          "short-trip 1-3-days quick getaway nearby compact",
    "chuyến dài ngày":      "long-trip multi-week slow-travel deep-immersion",
    "một ngày":             "day-trip half-day nearby quick visit",

    # ── Distance / reach ────────────────────────────────────
    "gần":                  "nearby short-distance local accessible",
    "xa":                   "far-flung remote long-journey destination",
    "trong nước":           "domestic Vietnam local travel",
    "quốc tế":              "international abroad overseas travel",

    # ── Style ────────────────────────────────────────────────
    "du lịch bụi":          "backpacking budget independent hostel freedom",
    "du lịch sang trọng":   "luxury premium resort fine-dining exclusive",
    "du lịch sinh thái":    "eco-tourism sustainable nature conservation community",
    "du lịch văn hóa":      "cultural heritage history tradition local immersive",
    "du lịch mạo hiểm":     "adventure trekking extreme outdoor adrenaline active",
    "du lịch chữa lành":    "healing wellness retreat slow peaceful rejuvenating",
    "du lịch cộng đồng":    "community-based tourism local authentic village cultural",
    "du lịch công tác":     "business-travel conference meeting corporate hotel",
    "du lịch tình nguyện":  "volunteer-travel community social impact meaningful",
    "road trip":            "road-trip drive scenic freedom flexible self-drive",
    "du lịch moto":         "motorbike-trip scenic road adventure freedom flexible",

    # ── English equivalents ─────────────────────────────────
    "weekend":              "weekend short-trip nearby compact quick-getaway",
    "day trip":             "day-trip nearby half-day quick visit",
    "backpacking":          "backpacking adventure budget travel hostel exploration",
    "luxury travel":        "luxury resort premium upscale fine-dining exclusive",
    "eco travel":           "eco-tourism sustainable nature conservation responsible",
    "adventure travel":     "adventure trekking hiking extreme outdoor adrenaline",
    "cultural trip":        "culture heritage history tradition museum local",
    "wellness retreat":     "wellness spa healing retreat peaceful slow nature",
    "romantic getaway":     "romantic couple sunset intimate scenic honeymoon",
    "family trip":          "family kid-friendly safe educational fun activities",
    "solo travel":          "solo independent flexible self-paced exploration",
    "group travel":         "group social activities flexible variety fun",
    "budget travel":        "budget affordable cheap local backpacker value",
    "slow travel":          "slow-travel immersive local community deep meaningful",
    "road trip":            "road-trip drive scenic freedom flexible",
    "cruise":               "cruise ship sea river sightseeing port luxury",
    "volunteer travel":     "volunteer community social impact meaningful local",
    "workation":            "workation remote-work wifi relaxed balance",
}


# ═════════════════════════════════════════════════════════════
# G. SOCIAL GROUP & PARTY TYPE
# ═════════════════════════════════════════════════════════════

SOCIAL_GROUP_TAGS: dict[str, str] = {
    # ── Solo ────────────────────────────────────────────────
    "một mình":             "solo independent flexible self-paced peaceful discovery",
    "du lịch solo":         "solo independent self-discovery freedom flexible",

    # ── Couples ─────────────────────────────────────────────
    "cặp đôi":              "romantic couple private intimate sunset scenic",
    "vợ chồng":             "couple married romantic private intimate scenic resort",
    "tuần trăng mật":       "honeymoon luxury romantic private resort scenic",
    "hẹn hò":               "date romantic intimate scenic dinner sunset couple",

    # ── Family ──────────────────────────────────────────────
    "gia đình":             "family kid-friendly safe educational activities",
    "gia đình có trẻ em":   "family young-children safe shallow-beach fun activities",
    "gia đình ba thế hệ":   "multigenerational family accessible comfortable gentle",
    "ông bà cháu":          "grandparents grandchildren gentle accessible cultural comfortable",

    # ── Friends ─────────────────────────────────────────────
    "bạn bè":               "friends group social fun adventure flexible activities",
    "nhóm bạn":             "group social activities adventure fun variety",
    "hội bạn thân":         "close-friends group bonding fun activities social",

    # ── Age-specific ────────────────────────────────────────
    "sinh viên":            "budget backpacker social affordable fun hostel young",
    "thanh niên":           "young active social adventure budget vibrant",
    "trung niên":           "middle-aged comfort culture scenic moderate accessible",
    "người lớn tuổi":       "senior accessible gentle scenic comfortable cultural",
    "người cao tuổi":       "elderly accessible comfortable slow-pace gentle scenic",

    # ── Special groups ──────────────────────────────────────
    "công ty":              "corporate team-building conference offsite group",
    "trăng mật":            "honeymoon romantic luxury private scenic couple",
    "LGBTQ+":               "LGBTQ-friendly inclusive welcoming open diverse",

    # ── English equivalents ─────────────────────────────────
    "solo":                 "solo independent flexible self-discovery peaceful",
    "couple":               "romantic couple intimate sunset private scenic",
    "newlyweds":            "honeymoon romantic luxury private resort scenic",
    "family":               "family kid-friendly safe educational comfortable",
    "with kids":            "kid-safe shallow-beach fun educational accessible",
    "friends":              "group social fun nightlife activities adventure",
    "group":                "group variety social activities flexible",
    "elderly":              "accessible comfortable gentle scenic cultural heritage",
    "students":             "budget affordable backpacker social hostel fun",
    "backpackers":          "budget hostel social flexible backpacker",
    "corporate":            "corporate team-building conference offsite group",
    "LGBTQ":                "LGBTQ-friendly inclusive welcoming open diverse",
}


# ═════════════════════════════════════════════════════════════
# H. BUDGET & PRICE TIER
# ═════════════════════════════════════════════════════════════

BUDGET_TAGS: dict[str, str] = {
    "tiết kiệm":            "budget cheap affordable value local street-food hostel",
    "giá rẻ":               "budget cheap affordable value backpacker",
    "tầm trung":            "mid-range moderate comfortable value-for-money",
    "cao cấp":              "luxury premium upscale exclusive fine-dining resort",
    "siêu sang":            "ultra-luxury exclusive VIP private premium 5-star",
    "miễn phí":             "free no-cost public park beach nature",

    "budget":               "budget cheap affordable value hostel street-food",
    "mid-range":            "mid-range moderate comfortable value",
    "luxury":               "luxury premium exclusive upscale resort fine-dining",
    "ultra luxury":         "ultra-luxury VIP private exclusive 5-star premium",
    "free":                 "free no-cost public park accessible",
    "value for money":      "value affordable quality reasonable mid-range",
}


# ═════════════════════════════════════════════════════════════
# I. GEOGRAPHY & REGION
# ═════════════════════════════════════════════════════════════

GEOGRAPHY_TAGS: dict[str, str] = {
    # ── Vietnam macro-regions ────────────────────────────────
    "miền Bắc":             "north-vietnam highland culture heritage cool scenic",
    "miền Trung":           "central-vietnam beach heritage history culture",
    "miền Nam":             "south-vietnam mekong tropical warm vibrant food",
    "Tây Bắc":              "northwest-vietnam mountain ethnic-minority terraced rice",
    "Đông Bắc":             "northeast-vietnam karst limestone border culture",
    "Tây Nguyên":           "central-highlands vietnam plateau coffee waterfall ethnic",
    "đồng bằng sông Cửu Long": "mekong-delta river floating-market tropical flat",

    # ── Vietnam named destinations ───────────────────────────
    "Hà Nội":               "hanoi capital culture heritage old-quarter lake history",
    "Hồ Chí Minh":          "ho-chi-minh-city saigon vibrant modern food nightlife",
    "Đà Nẵng":              "danang beach modern bridge resort coastal",
    "Hội An":               "hoi-an ancient-town lantern heritage tailoring beach",
    "Huế":                  "hue imperial heritage tombs cuisine culture history",
    "Nha Trang":            "nha-trang beach resort diving sea-food city coastal",
    "Phú Quốc":             "phu-quoc island tropical beach resort snorkeling",
    "Sapa":                 "sapa highland terraced-rice ethnic-minority trekking fog",
    "Hạ Long":              "ha-long bay limestone cruise karst iconic scenic",
    "Đà Lạt":               "dalat highland cool flower pine romantic scenic",
    "Mũi Né":               "mui-ne sand-dune coastal fishing-village kite-surf",
    "Cần Thơ":              "can-tho mekong delta floating-market river food",
    "Ninh Bình":            "ninh-binh karst rice-field boat cave scenic quiet",
    "Quy Nhơn":             "quy-nhon beach coastal quiet local seafood",
    "Côn Đảo":              "con-dao island pristine turtle beach national-park",
    "Phong Nha":            "phong-nha cave adventure national-park UNESCO",
    "Mộc Châu":             "moc-chau highland plateau flower tea misty",
    "Bạn Mê Thuột":         "buon-ma-thuot highland coffee ethnic waterfall",
    "Vũng Tàu":             "vung-tau beach weekend city-escape seafood",
    "Long An":              "long-an mekong quiet rural local day-trip",

    # ── Terrain-based ────────────────────────────────────────
    "vùng ven biển":        "coastal beach shoreline seafood scenic breeze",
    "vùng nội địa":         "inland countryside rural farmland quiet nature",
    "vùng đồng bằng":       "delta river flatland agricultural mekong local",
    "vùng cao nguyên":      "highland plateau mountain cool climate scenic",
    "vùng đảo":             "island archipelago tropical sea beach remote",
    "vùng núi":             "mountainous highland trail trek nature remote",

    # ── English aliases ──────────────────────────────────────
    "north vietnam":        "north-vietnam highland culture heritage cool",
    "central vietnam":      "central-vietnam beach heritage culture history",
    "south vietnam":        "south-vietnam mekong tropical vibrant food",
    "northwest vietnam":    "northwest-vietnam mountain ethnic rice-terrace",
    "central highlands":    "central-highlands vietnam plateau coffee ethnic",
    "mekong delta":         "mekong-delta river floating-market tropical flat",
    "ha long bay":          "ha-long bay limestone cruise karst scenic UNESCO",
    "hoi an":               "hoi-an ancient-town lantern heritage tailoring beach",
    "sapa":                 "sapa highland trekking ethnic fog terraced-rice",
    "phu quoc":             "phu-quoc island tropical beach resort snorkeling",
    "da lat":               "dalat highland cool flower pine romantic scenic",
    "phong nha":            "phong-nha cave national-park adventure UNESCO",
    "coastal":              "coastal beach sea ocean shoreline seaside",
    "inland":               "inland countryside rural farmland quiet nature",
    "highland":             "highland mountain cool climate scenic trekking",
    "island":               "island archipelago tropical remote beach sea",
}


# ═════════════════════════════════════════════════════════════
# J. SEASON & WEATHER SUITABILITY
# ═════════════════════════════════════════════════════════════

SEASON_TAGS: dict[str, str] = {
    # ── Vietnamese ───────────────────────────────────────────
    "mùa hè":               "summer beach coastal water-sports sun outdoor",
    "mùa đông":             "winter highland cool cozy indoor retreat warm",
    "mùa xuân":             "spring festival blossom green fresh outdoor mild",
    "mùa thu":              "autumn leaf colorful cool highland peaceful scenic",
    "mùa mưa":              "rainy-season waterfall green cave indoor cozy",
    "mùa khô":              "dry-season beach outdoor activities clear-sky",
    "mùa hoa":              "flower-season blossom colorful photography spring",
    "tháng 1-3":            "cool dry north scenic cultural new-year spring",
    "tháng 4-6":            "hot south beach coastal early-summer",
    "tháng 7-9":            "peak-summer beach resort crowd typhoon central",
    "tháng 10-12":          "cool north peak-season central heritage mild south",

    # ── Weather suitability ──────────────────────────────────
    "thời tiết đẹp":        "clear-sky sunny pleasant outdoor beach scenic",
    "mát mẻ":               "cool comfortable highland mountain outdoor",
    "nắng":                 "sunny warm beach outdoor clear-sky",
    "mưa nhẹ":              "light-rain green lush atmospheric misty",
    "tuyết":                "snow highland winter rare cold scenic",

    # ── English ──────────────────────────────────────────────
    "summer":               "summer beach coastal water-sports sun holiday",
    "winter":               "winter highland cool cozy mountain indoor",
    "spring":               "spring blossom outdoor fresh mild festival",
    "autumn":               "autumn leaf colorful cool scenic highland peaceful",
    "rainy season":         "rainy-season waterfall cave green lush indoor",
    "dry season":           "dry-season beach outdoor clear-sky activities",
    "best in summer":       "summer beach coastal outdoor sun peak-season",
    "best in winter":       "winter cool highland cozy retreat scenic",
    "year-round":           "year-round all-season suitable any-time flexible",
    "avoid monsoon":        "dry-season preference beach clear outdoor",
}


# ═════════════════════════════════════════════════════════════
# K. ACCESSIBILITY & COMFORT
# ═════════════════════════════════════════════════════════════

ACCESSIBILITY_TAGS: dict[str, str] = {
    "dễ đi":                "easy-access paved road short-walk suitable-all",
    "khó đi":               "remote rough-road 4wd required effort rewarding",
    "đường bằng phẳng":     "flat-terrain paved gentle accessible all-ages",
    "leo trèo nhiều":       "strenuous climbing stairs uneven terrain fitness",
    "xe lăn":               "wheelchair-accessible ramp elevator mobility",
    "người cao tuổi phù hợp":"senior-friendly gentle accessible comfortable",
    "gần trung tâm":        "central location walking-distance convenience",
    "xa trung tâm":         "remote rural isolated peaceful far-from-city",
    "có xe buýt":           "public-transport bus accessible affordable",
    "cần xe cá nhân":       "car-required self-drive private-transport",

    "accessible":           "accessible flat easy-access suitable all-ages",
    "wheelchair friendly":  "wheelchair-accessible ramp elevator mobility",
    "easy access":          "easy-access paved road short-walk central",
    "remote":               "remote rural isolated effort required rewarding",
    "central location":     "central walking-distance convenient landmark",
    "car required":         "car-required self-drive private-transport remote",
}


# ═════════════════════════════════════════════════════════════
# L. SUSTAINABILITY & ETHICS
# ═════════════════════════════════════════════════════════════

SUSTAINABILITY_TAGS: dict[str, str] = {
    "du lịch bền vững":     "sustainable responsible eco-friendly low-impact green",
    "thân thiện môi trường":"eco-friendly green sustainable low-carbon nature",
    "du lịch cộng đồng":    "community-based tourism local income authentic cultural",
    "hữu cơ":               "organic farm-to-table natural sustainable food",
    "không nhựa":           "plastic-free eco sustainable responsible beach",
    "bảo tồn":              "conservation wildlife habitat protection eco",
    "năng lượng tái tạo":   "solar renewable energy sustainable eco lodge",

    "sustainable":          "sustainable responsible eco-friendly low-impact",
    "eco-friendly":         "eco-friendly green sustainable low-carbon",
    "responsible tourism":  "responsible ethical local community sustainable",
    "community based":      "community-based local income authentic cultural",
    "carbon offset":        "carbon-offset low-impact sustainable responsible",
    "conservation":         "conservation wildlife habitat eco protection",
    "organic farm":         "organic farm-to-table natural sustainable local food",
    "zero waste":           "zero-waste eco responsible minimal-impact sustainable",
}


# ═════════════════════════════════════════════════════════════
# M. PHOTOGRAPHY & CONTENT CREATION
# ═════════════════════════════════════════════════════════════

PHOTOGRAPHY_TAGS: dict[str, str] = {
    "điểm check-in đẹp":    "scenic viewpoint photogenic instagram aesthetic landmark",
    "cảnh đẹp":             "scenic beautiful landscape stunning photography-worthy",
    "góc sống ảo":          "instagram-worthy aesthetic photogenic colorful unique",
    "drone":                "drone aerial photography scenic landscape cinematic",
    "bình minh đẹp":        "sunrise golden photography scenic dramatic sky",
    "hoàng hôn đẹp":        "sunset golden romantic photography scenic",
    "nhiều màu sắc":        "colorful vibrant photography aesthetic visual",
    "cảnh biển đẹp":        "seascape beach photography scenic coastal beautiful",
    "cảnh núi đẹp":         "mountain-view photography scenic highland dramatic",
    "ánh sáng đẹp":         "golden-hour beautiful-light photography scenic",

    "instagram":            "instagram-worthy photogenic colorful aesthetic scenic",
    "drone photography":    "drone aerial photography scenic landscape cinematic",
    "golden hour":          "golden-hour photography sunrise sunset scenic warm",
    "landscape photography":"landscape scenic nature photography dramatic wide",
    "portrait location":    "portrait colorful vibrant backdrop photography",
    "underwater photography":"underwater dive snorkel reef photography colorful",
    "night photography":    "night-photography stargazing city-lights long-exposure",
    "content creation":     "content-creator photography videography aesthetic scenic",
}


# ═════════════════════════════════════════════════════════════
# N. FOOD & DRINK
# ═════════════════════════════════════════════════════════════

FOOD_TAGS: dict[str, str] = {
    # ── Cuisine types ────────────────────────────────────────
    "ẩm thực địa phương":   "local-cuisine authentic regional food culture flavour",
    "hải sản":              "seafood fresh fish shrimp crab ocean coastal cuisine",
    "món chay":             "vegetarian vegan plant-based healthy local temple",
    "ẩm thực đường phố":    "street-food cheap authentic local vendor night-market",
    "buffet":               "buffet variety dining resort hotel all-you-can-eat",
    "nhà hàng fine dining": "fine-dining gourmet upscale elegant cuisine",
    "nhà hàng view đẹp":    "scenic dining view restaurant romantic atmosphere",
    "cà phê":               "café coffee culture local hang-out cozy",
    "cà phê Highland":      "highland-coffee plantation culture tasting experience",
    "bia hơi":              "beer local street-side social cheap authentic",
    "rượu vang":            "wine tasting vineyard gourmet fine-dining",
    "trà":                  "tea culture highland ceremony calm relaxing",

    # ── Dietary / preference ────────────────────────────────
    "halal":                "halal Muslim-friendly certified food travel",
    "thuần chay":           "vegan plant-based no-animal strict healthy",
    "không gluten":         "gluten-free dietary health accommodation",
    "hữu cơ":               "organic natural farm-to-table healthy sustainable",

    # ── English ──────────────────────────────────────────────
    "seafood":              "seafood fresh fish shrimp crab coastal ocean cuisine",
    "street food":          "street-food cheap authentic local vendor market",
    "vegetarian":           "vegetarian plant-based healthy local temple food",
    "vegan":                "vegan plant-based strict no-animal healthy",
    "fine dining":          "fine-dining gourmet upscale elegant experience",
    "local food":           "local-cuisine authentic regional cultural flavour",
    "coffee culture":       "coffee café culture local hang-out social",
    "wine":                 "wine tasting vineyard gourmet fine-dining",
    "halal":                "halal Muslim-friendly certified food travel",
    "organic food":         "organic natural farm-to-table healthy sustainable",
    "cooking class":        "cooking-class culinary hands-on local food experience",
    "food tour":            "food-tour culinary street market tasting local",
    "night market food":    "night-market street-food vendor local cheap",
    "farm to table":        "farm-to-table organic fresh local sustainable",
}


# ═════════════════════════════════════════════════════════════
# O. WELLNESS & HEALTH
# ═════════════════════════════════════════════════════════════

WELLNESS_TAGS: dict[str, str] = {
    "spa":                  "spa massage body-treatment relaxation wellness",
    "massage":              "massage therapy relaxation wellness muscle-relief",
    "yoga":                 "yoga mindfulness wellness flexibility retreat",
    "thiền định":           "meditation mindfulness silent wellness retreat spiritual",
    "tắm suối khoáng":      "mineral-spring thermal bath wellness relaxation healing",
    "tắm bùn":              "mud-bath mineral spa therapeutic relaxation",
    "tắm lá thuốc":         "herbal-bath traditional wellness healing ethnic local",
    "chữa lành":            "healing restorative wellness retreat peaceful nature",
    "detox":                "detox cleanse wellness healthy retreat nature",
    "chạy bộ":              "running jogging trail outdoor fitness nature",
    "leo núi thể dục":      "fitness hiking outdoor active health nature",
    "bơi biển":             "sea-swimming ocean fitness health outdoor",

    "spa retreat":          "spa retreat wellness relaxation massage therapy",
    "yoga retreat":         "yoga retreat mindfulness wellness nature peaceful",
    "meditation retreat":   "meditation retreat mindfulness silent spiritual wellness",
    "hot spring":           "hot-spring thermal mineral wellness relaxation healing",
    "herbal bath":          "herbal-bath traditional wellness healing local",
    "detox retreat":        "detox cleanse wellness healthy retreat",
    "fitness":              "fitness gym active outdoor health wellness",
    "mental wellness":      "mental-wellness slow-travel peaceful nature mindful",
    "healing":              "healing restorative wellness retreat nature peaceful",
}


# ═════════════════════════════════════════════════════════════
# P. EVENTS & FESTIVALS
# ═════════════════════════════════════════════════════════════

EVENTS_TAGS: dict[str, str] = {
    "Tết Nguyên Đán":       "lunar-new-year Tet celebration family tradition firework",
    "lễ hội hoa":           "flower-festival blossom colorful spring photography",
    "lễ hội đèn lồng":      "lantern-festival Hoi-An colorful cultural night romantic",
    "Tết Trung Thu":        "mid-autumn moon-cake lantern children festival",
    "lễ hội biển":          "beach-festival coastal seafood summer lively music",
    "lễ hội âm nhạc":       "music-festival live outdoor concert crowd fun",
    "lễ hội ẩm thực":       "food-festival culinary tasting local culture crowd",
    "lễ hội đua thuyền":    "boat-race traditional festival river crowd cultural",
    "giải marathon":        "marathon running sport active scenic road",
    "triển lãm":            "exhibition gallery art cultural event",
    "carnival":             "carnival parade colorful festive crowd",

    "lunar new year":       "lunar-new-year celebration tradition family festive",
    "lantern festival":     "lantern-festival colorful cultural night romantic",
    "music festival":       "music-festival live outdoor concert fun crowd",
    "food festival":        "food-festival culinary tasting local culture",
    "beach festival":       "beach-festival coastal summer music lively",
    "art festival":         "art-festival creative exhibition cultural event",
    "marathon":             "marathon running sport active scenic event",
    "new year":             "new-year celebration firework festive crowd city",
    "christmas":            "christmas festive lights winter cozy shopping",
}


# ═════════════════════════════════════════════════════════════
# Q. NIGHTLIFE & ENTERTAINMENT
# ═════════════════════════════════════════════════════════════

NIGHTLIFE_TAGS: dict[str, str] = {
    "bar":                  "bar cocktail nightlife social evening vibrant",
    "club":                 "nightclub dancing electronic late-night party",
    "rooftop bar":          "rooftop-bar city-view cocktail sunset evening",
    "nhạc sống":            "live-music bar jazz blues acoustic evening",
    "karaoke":              "karaoke social fun evening group",
    "xem phim":             "cinema movie entertainment indoor evening",
    "show diễn":            "show performance evening cultural entertainment",
    "rạp xiếc":             "circus performance family show entertainment",
    "casino":               "casino gaming nightlife entertainment hotel",
    "phố đêm":              "night-street entertainment lively bar food evening",
    "bia hơi":              "street-beer local cheap social evening",

    "nightlife":            "nightlife bar club entertainment social vibrant",
    "rooftop":              "rooftop city-view cocktail evening sunset bar",
    "live music":           "live-music bar jazz acoustic concert evening",
    "night tour":           "night-tour city lights walking evening culture",
    "bar hopping":          "bar-hopping nightlife social drinks evening fun",
    "dinner cruise":        "dinner-cruise river evening romantic scenic dining",
    "night market":         "night-market street-food shopping lively evening",
    "cultural show":        "cultural-show performance traditional evening",
    "comedy":               "comedy show entertainment evening fun laugh",
}


# ═════════════════════════════════════════════════════════════
# R. WATER ACTIVITIES (DETAILED)
# ═════════════════════════════════════════════════════════════

WATER_ACTIVITY_TAGS: dict[str, str] = {
    "lặn scuba":            "scuba-diving deep underwater equipment reef marine",
    "lặn freediving":       "freediving breath-hold underwater marine serene",
    "chèo kayak biển":      "sea-kayaking coastal cave island exploration paddle",
    "chèo kayak sông":      "river-kayaking gentle current nature scenery paddle",
    "lướt ván":             "surfing wave sport beach adventure coastal",
    "kite surf":            "kitesurfing wind coastal extreme water sport",
    "chèo SUP biển":        "sea-SUP paddleboard coastal calm balance",
    "đua thuyền":           "boat-racing sport river lake competitive",
    "câu cá biển":          "sea-fishing offshore boat deep-sea local",
    "câu cá hồ":            "lake-fishing tranquil calm nature local",
    "snorkling":            "snorkeling reef marine tropical shallow colorful",
    "bơi sông":             "river-swimming freshwater cool nature local scenic",

    "scuba diving":         "scuba-diving deep reef marine underwater equipment",
    "freediving":           "freediving breath-hold marine serene underwater",
    "sea kayaking":         "sea-kayaking coastal cave island exploration",
    "river kayaking":       "river-kayaking gentle nature scenery paddle",
    "kitesurfing":          "kitesurfing wind coastal extreme water-sport",
    "wakeboarding":         "wakeboarding water speed lake adventure",
    "white water rafting":  "rafting white-water river adventure adrenaline",
    "sailing":              "sailing boat wind sea adventure leisure",
    "jet ski":              "jet-ski speed water thrilling coastal",
    "banana boat":          "banana-boat fun group family coastal water",
    "glass bottom boat":    "glass-bottom-boat reef viewing marine family",
}


# ═════════════════════════════════════════════════════════════
# S. LAND SPORTS & ADVENTURE (DETAILED)
# ═════════════════════════════════════════════════════════════

LAND_SPORT_TAGS: dict[str, str] = {
    "trekking nhiều ngày":  "multi-day-trek wilderness camping mountain trail",
    "leo đỉnh":             "summit-climb peak altitude challenge achievement",
    "leo vách đá tự nhiên": "natural-rock-climbing outdoor sport cliff",
    "leo vách nhân tạo":    "indoor-climbing bouldering sport gym",
    "đạp xe địa hình":      "mountain-biking trail off-road adventure nature",
    "đạp xe đường phẳng":   "road-cycling scenic countryside flat leisure",
    "cưỡi ngựa rừng":       "jungle-horse-riding adventure trail nature scenic",
    "đua xe địa hình":      "off-road-racing ATV buggy adventure adrenaline",
    "trượt cỏ":             "grass-sliding hillside fun nature",
    "đu dây":               "abseiling rappelling cliff adventure outdoor",
    "vượt thác":            "waterfall-abseiling adventure wet outdoor thrill",
    "đi bộ đầm lầy":        "swamp-trekking wetland eco adventure nature",
    "golf":                 "golf course sport leisure outdoor resort",

    "multi-day trek":       "multi-day-trek wilderness camping mountain trail",
    "mountain biking":      "mountain-biking trail off-road adventure",
    "road cycling":         "road-cycling scenic countryside flat leisure",
    "abseiling":            "abseiling rappelling cliff adventure outdoor",
    "ATV":                  "ATV quad-bike off-road adventure adrenaline",
    "golf":                 "golf course sport leisure outdoor resort",
    "trail running":        "trail-running outdoor fitness nature scenic",
    "orienteering":         "orienteering map navigation outdoor team sport",
    "archery":              "archery sport outdoor cultural traditional skill",
    "horseback riding":     "horseback-riding outdoor scenic countryside leisure",
}


# ═════════════════════════════════════════════════════════════
# T. AIR & EXTREME SPORTS
# ═════════════════════════════════════════════════════════════

AIR_SPORT_TAGS: dict[str, str] = {
    "dù lượn":              "paragliding aerial scenic valley view adrenaline",
    "nhảy dù":              "skydiving freefall extreme adrenaline aerial",
    "khinh khí cầu":        "hot-air-balloon aerial sunrise scenic romantic",
    "cáp treo":             "cable-car aerial mountain view scenic comfortable",
    "đu dây cao":           "high-wire via-ferrata cliff adventure height",
    "bungee":               "bungee-jumping extreme adrenaline bridge height",
    "bay cùng chim":        "paramotor motorized aerial view scenic fun",

    "paragliding":          "paragliding aerial scenic valley adrenaline",
    "skydiving":            "skydiving extreme freefall adrenaline aerial",
    "hot air balloon":      "hot-air-balloon aerial scenic romantic sunrise",
    "cable car":            "cable-car aerial mountain scenic comfortable",
    "bungee jumping":       "bungee-jumping extreme adrenaline height bridge",
    "via ferrata":          "via-ferrata cliff climbing helmet harness adventure",
    "hang gliding":         "hang-gliding aerial free-flight scenic adrenaline",
}


# ═════════════════════════════════════════════════════════════
# U. KIDS & FAMILY AMENITIES
# ═════════════════════════════════════════════════════════════

FAMILY_TAGS: dict[str, str] = {
    "thân thiện trẻ em":    "kid-friendly safe fun educational shallow-water",
    "công viên nước":       "water-park slides pool family fun kids splash",
    "công viên giải trí":   "theme-park rides family entertainment fun",
    "khu vui chơi":         "playground kids indoor-play family fun",
    "sở thú":               "zoo animals educational family kids",
    "bãi biển nước nông":   "shallow-beach calm safe kids family wading",
    "bể bơi cho bé":        "kids-pool shallow safe resort family",
    "camp hè":              "summer-camp kids outdoor learning fun",
    "lớp học nấu ăn bé":    "kids-cooking-class family fun local food",
    "phòng trẻ em":         "kids-room baby-cot crib family hotel amenity",
    "ghế em bé":            "highchair restaurant baby family-friendly",
    "trông trẻ":            "babysitting childcare resort service family",

    "kids friendly":        "kid-friendly safe fun shallow-water educational",
    "water park":           "water-park slides splash family fun kids",
    "theme park":           "theme-park rides entertainment family fun",
    "playground":           "playground kids outdoor fun active family",
    "shallow water":        "shallow-water safe calm wading kids beach",
    "kids pool":            "kids-pool shallow safe resort family",
    "babysitting":          "babysitting childcare resort service family",
    "educational":          "educational learning museum cultural kids family",
    "stroller friendly":    "stroller pram accessible flat family",
    "baby facilities":      "baby-facilities cot highchair changing family",
}


# ═════════════════════════════════════════════════════════════
# V. PETS, ANIMALS & WILDLIFE
# ═════════════════════════════════════════════════════════════

ANIMAL_TAGS: dict[str, str] = {
    "thân thiện vật nuôi":  "pet-friendly dog cat travel accommodation",
    "xem voi":              "elephant ethical sanctuary nature wildlife",
    "xem gấu":              "bear sanctuary rescue wildlife ethical",
    "nông trại":            "farm animal feeding rural authentic kids",
    "trang trại cá sấu":    "crocodile farm local attraction unique",
    "khu bảo tồn rùa biển": "sea-turtle conservation eco beach nesting",
    "ngắm cá heo":          "dolphin-watching marine wildlife boat tour",
    "ngắm cá voi":          "whale-watching marine wildlife boat offshore",
    "vườn bướm":            "butterfly-garden nature colorful photography",
    "trang trại ong":       "bee-farm honey local rural authentic",
    "câu lạc bộ đua ngựa":  "horse-racing sport entertainment social",

    "pet friendly":         "pet-friendly dog cat travel accommodation",
    "elephant sanctuary":   "elephant ethical sanctuary wildlife nature",
    "wildlife safari":      "wildlife safari animals nature eco observation",
    "farm visit":           "farm animal rural authentic local family",
    "dolphin watching":     "dolphin marine wildlife boat scenic",
    "whale watching":       "whale marine wildlife boat offshore scenic",
    "turtle conservation":  "sea-turtle conservation eco beach nesting",
    "butterfly garden":     "butterfly garden colorful nature photography",
    "birdwatching":         "birdwatching binoculars wetland eco nature quiet",
    "horse racing":         "horse-racing sport entertainment event",
}


# ═════════════════════════════════════════════════════════════
# W. ROMANCE & COUPLES (DETAILED)
# ═════════════════════════════════════════════════════════════

ROMANCE_TAGS: dict[str, str] = {
    "trăng mật":            "honeymoon luxury romantic private scenic couple",
    "kỷ niệm":              "anniversary romantic couple special scenic",
    "dinner lãng mạn":      "romantic-dinner candlelight scenic intimate",
    "đề xuất hôn nhân":     "proposal scenic viewpoint private romantic luxury",
    "spa đôi":              "couples-spa massage wellness intimate relaxation",
    "phòng view đẹp":       "room-with-view scenic ocean mountain sunrise romantic",
    "biệt thự riêng tư":    "private-villa pool couple exclusive romantic",
    "picnic đôi":           "couples-picnic scenic outdoor nature romantic",
    "ngắm hoàng hôn đôi":   "sunset-couple scenic romantic viewpoint photography",
    "cruise lãng mạn":      "romantic-cruise river sea sunset private couple",

    "honeymoon":            "honeymoon luxury romantic private resort scenic",
    "anniversary":          "anniversary romantic couple special scenic luxury",
    "couples spa":          "couples-spa massage wellness intimate relaxation",
    "romantic dinner":      "romantic-dinner candlelight scenic intimate",
    "proposal location":    "proposal scenic private viewpoint romantic sunset",
    "private villa":        "private-villa pool exclusive couple romantic",
    "sunset cruise":        "sunset-cruise romantic scenic couple sea",
    "couples retreat":      "couples-retreat romantic peaceful private luxury",
    "intimate":             "intimate private romantic couple peaceful scenic",
    "Valentine":            "valentines-day romantic couple special scenic",
}


# ═════════════════════════════════════════════════════════════
# X. EDUCATION & LEARNING
# ═════════════════════════════════════════════════════════════

EDUCATION_TAGS: dict[str, str] = {
    "học lịch sử":          "history-tour museum heritage educational guided",
    "học văn hóa":          "cultural-immersion tradition local workshop community",
    "lớp học nấu ăn":       "cooking-class culinary food culture local hands-on",
    "lớp dệt":              "weaving-class textile craft ethnic traditional",
    "học làm gốm":          "pottery-class craft hands-on artisan creative",
    "học tiếng Việt":       "Vietnamese-language class culture immersive local",
    "tour có hướng dẫn viên":"guided-tour expert knowledge heritage cultural",
    "du lịch học tập":      "educational-travel school group learning cultural",
    "workshop":             "workshop hands-on skill craft learning experience",
    "home-stay học hỏi":    "immersive homestay cultural exchange learning local",

    "cooking class":        "cooking-class culinary food culture local",
    "language class":       "language-class cultural immersion local exchange",
    "history tour":         "history-tour heritage museum educational guided",
    "guided tour":          "guided-tour expert knowledge heritage cultural",
    "cultural workshop":    "cultural-workshop hands-on tradition craft local",
    "pottery":              "pottery craft hands-on artisan creative workshop",
    "weaving":              "weaving textile craft ethnic traditional workshop",
    "educational tour":     "educational-tour school learning cultural heritage",
    "volunteer":            "volunteer community social impact meaningful local",
    "cultural exchange":    "cultural-exchange immersive local community learning",
}


# ═════════════════════════════════════════════════════════════
# MASTER REGISTRY — all sections merged
# ═════════════════════════════════════════════════════════════

ALL_TAGS: dict[str, str] = {
    **NATURE_TAGS,
    **URBAN_TAGS,
    **ACTIVITY_TAGS,
    **ACCOMMODATION_TAGS,
    **ATMOSPHERE_TAGS,
    **TRAVEL_STYLE_TAGS,
    **SOCIAL_GROUP_TAGS,
    **BUDGET_TAGS,
    **GEOGRAPHY_TAGS,
    **SEASON_TAGS,
    **ACCESSIBILITY_TAGS,
    **SUSTAINABILITY_TAGS,
    **PHOTOGRAPHY_TAGS,
    **FOOD_TAGS,
    **WELLNESS_TAGS,
    **EVENTS_TAGS,
    **NIGHTLIFE_TAGS,
    **WATER_ACTIVITY_TAGS,
    **LAND_SPORT_TAGS,
    **AIR_SPORT_TAGS,
    **FAMILY_TAGS,
    **ANIMAL_TAGS,
    **ROMANCE_TAGS,
    **EDUCATION_TAGS,
}