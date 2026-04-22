"""
maps/context.py
===============
Maps structural and situational context signals into normalized English
travel intent keywords for BGE-M3 embedding.

These signals are extracted from short, free-form user input and expanded
into lightweight semantic hints that guide retrieval. They do NOT enforce
hard constraints (e.g. exact duration or distance), but instead provide
soft bias toward travel style, proximity, and budget.

The goal is to enrich sparse queries with consistent, embedding-friendly
tokens such as "travel", "experience", and "activities", improving
semantic matching against destination data.

─────────────────────────────────────────────────────────────
SECTION INDEX
─────────────────────────────────────────────────────────────
  A. SEASON & WEATHER   — climate, timing, seasonal context
  B. SOCIAL GROUP       — travel companions and group dynamics
  C. TRIP DURATION      — low-weight trip length intent (short vs long)
  D. TRIP DISTANCE      — low-weight proximity intent (nearby vs far)
  E. BUDGET LEVEL       — price sensitivity (budget to luxury)
  F. PACE & STYLE       — travel style, flexibility, activity level

"""

# ═════════════════════════════════════════════════════════════
# A. SEASON & WEATHER
# ═════════════════════════════════════════════════════════════
SEASON_WEATHER: dict[str, str] = {
    # Vietnamese — seasons
    "mùa hè":       "summer beach coastal travel swimming water activities sun outdoor relaxation",
    "mùa đông":     "winter mountain highland travel cool weather cozy indoor retreat scenic nature",
    "mùa xuân":     "spring blossom festival travel fresh air outdoor walking cultural experience",
    "mùa thu":      "autumn scenic landscape colorful leaves mountain highland peaceful travel photography",
    "mùa khô":      "dry season beach outdoor travel activities sun clear sky coastal exploration",
    "lễ hội":       "festival cultural travel celebration local tradition event experience",

    # Vietnamese — weather
    "nắng":         "sunny weather beach outdoor travel activities sightseeing clear sky",
    "mưa":          "rainy weather indoor cafe relaxation waterfall cave nature lush scenery travel",
    "nóng":         "hot weather cooling beach water swimming highland escape travel",
    "lạnh":         "cold weather warm indoor cozy mountain retreat scenic travel",
    "hanh":         "dry weather beach outdoor travel clear sky activities sunshine",
    "oi":           "humid hot weather coastal breeze beach water highland cooling travel",
    "sương":        "misty weather highland mountain foggy atmospheric scenic travel photography",
    "gió":          "windy coastal beach open space fresh air outdoor travel scenic",
    "bão":          "storm weather indoor shelter safe travel cave highland dramatic scenery",
    "tuyết":        "snow winter mountain highland scenic travel cold weather cozy retreat",
    "sấm":          "thunder storm indoor cozy shelter travel dramatic cave highland",

    # Vietnamese — weather feel
    "mát mẻ":       "cool weather highland mountain fresh air forest nature travel relaxation",
    "trời đẹp":     "beautiful weather sunny outdoor travel scenic beach picnic clear sky",
    "dễ chịu":      "pleasant weather outdoor travel gentle walking nature relaxation",

    # Vietnamese — timing / occasion
    "cuối tuần":    "weekend short trip nearby travel quick getaway relaxation",
    "nghỉ hè":      "summer holiday beach travel outdoor water activities coastal relaxation",
    "nghỉ đông":    "winter holiday mountain highland cozy indoor retreat travel",
    "nghỉ lễ":      "holiday travel short trip festive celebration getaway",
    "cuối năm":     "year end holiday travel festive celebration cultural experience",
    "đầu năm":      "new year festival travel cultural fresh start celebration",
    "tết":          "tet festival vietnam cultural travel tradition food celebration experience",
    "mùa cưới":     "wedding season romantic couple travel luxury resort private scenic",
    "dịp đặc biệt": "special occasion celebration travel luxury experience milestone",

    # English — seasons
    "summer":       "summer beach travel coastal swimming water activities sun outdoor",
    "winter":       "winter mountain highland travel cool weather cozy indoor retreat",
    "spring":       "spring blossom outdoor travel fresh air festival nature experience",
    "autumn":       "autumn leaf colorful scenic mountain highland peaceful travel",
    "fall":         "fall leaf colorful scenic mountain highland peaceful travel",
    "monsoon":      "monsoon rainy season waterfall lush nature indoor cozy cave travel",

    # English — weather
    "hot":          "hot weather cooling beach water swimming highland travel",
    "cold":         "cold weather warm indoor cozy mountain scenic travel",
    "sunny":        "sunny weather beach outdoor travel picnic sightseeing clear sky",
    "foggy":        "foggy misty highland mountain atmospheric scenic travel",
    "cool":         "cool weather highland mountain fresh air forest travel",
    "windy":        "windy coastal beach open outdoor fresh air travel",
    "mild":         "mild weather outdoor travel walking nature relaxation",
    "humid":        "humid weather coastal breeze beach outdoor shade travel",
    "overcast":     "overcast sky highland moody atmospheric scenic travel",
    "misty":        "misty foggy highland mountain atmospheric scenic travel",
    "warm":         "warm weather beach tropical coastal outdoor travel",
    "freezing":     "freezing cold mountain highland cozy indoor retreat travel",
    "stormy":       "storm weather indoor shelter cave highland travel",
    "clear":        "clear sky sunny outdoor travel scenic beach nature",
    "dry":          "dry weather beach outdoor travel clear sky activities",
    "wet":          "wet rainy waterfall cave lush nature indoor travel",
    "snowy":        "snowy winter mountain highland scenic cozy travel",
    "tropical":     "tropical beach coastal warm weather water activities travel",
    "breezy":       "breezy coastal beach fresh air outdoor travel scenic",

    # English — timing
    "weekend":      "weekend short trip nearby travel quick getaway",
    "off-peak":     "off peak travel quiet uncrowded peaceful affordable hidden gem",
    "holiday":      "holiday travel festive getaway short trip celebration",
    "seasonal":     "seasonal travel timed festival cultural nature experience",
    "low season":   "low season travel affordable quiet uncrowded hidden gem",
    "high season":  "high season travel popular resort well serviced facilities",

    # Vietnamese synonyms
    "nhiệt độ cao": "hot weather cooling beach water coastal highland travel",
    "khí hậu mát":  "cool climate highland mountain fresh air forest travel",
    "trời rét":     "cold weather warm indoor cozy mountain travel",
    "ẩm thấp":      "humid wet weather indoor cave waterfall lush travel",
    "trời trong":   "clear sky sunny outdoor travel scenic beach",
    "mùa ẩm":       "wet season rainy waterfall cave lush nature travel",
    "dịp lễ":       "holiday travel festive celebration short trip getaway",

    # English synonyms
    "balmy":        "warm mild weather beach tropical outdoor pleasant travel",
    "pleasant":     "pleasant mild weather outdoor travel nature relaxation",
    "scorching":    "extreme heat cooling beach water highland travel",
    "chilly":       "chilly cold weather warm indoor mountain travel",
    "crisp":        "crisp cool weather mountain fresh air outdoor travel",
    "muggy":        "muggy humid weather coastal beach shade travel",
    "grey":         "grey overcast sky moody atmospheric highland travel",
    "hazy":         "hazy misty weather highland atmospheric scenic travel",
    "rainy":        "rainy weather indoor waterfall cave lush travel",
    "drizzly":      "light rain indoor cafe cave relaxed travel",
    "blizzard":     "snow storm mountain highland indoor cozy travel",
}
# ═════════════════════════════════════════════════════════════
# B. SOCIAL GROUP
# ═════════════════════════════════════════════════════════════
SOCIAL_GROUP: dict[str, str] = {
    # Vietnamese
    "một mình":     "solo travel independent flexible self discovery peaceful exploration",
    "cặp đôi":      "couple travel romantic private intimate scenic experience relaxation",
    "vợ chồng":     "couple travel romantic private resort intimate scenic relaxation",
    "gia đình":     "family travel kid friendly safe activities education bonding experience",
    "trẻ em":       "family travel kids safe fun activities shallow beach education",
    "trẻ nhỏ":      "family travel young children safe fun accessible activities",
    "bạn bè":       "group travel friends social fun nightlife activities adventure",
    "nhóm bạn":     "group travel social activities adventure fun exploration",
    "bạn thân":     "friends travel close bonding relaxed fun flexible experience",
    "sinh viên":    "student travel budget backpacker social hostel affordable fun",
    "người già":    "senior travel accessible gentle comfortable scenic cultural experience",
    "ông bà":       "senior travel accessible comfortable gentle heritage cultural experience",
    "đồng nghiệp":  "team travel group team building activities social bonding",
    "công ty":      "company travel team building organized group activities social",
    "ba mẹ":        "family travel parents comfortable gentle scenic cultural bonding",
    "hai người":    "couple travel romantic private intimate scenic experience",
    "nhóm nhỏ":     "small group travel flexible intimate activities adventure experience",
    "nhóm lớn":     "large group travel organized resort activities social experience",
    "nhiều thế hệ": "multi generation family travel accessible comfortable bonding cultural",
    "hội bạn":      "friends group travel social fun lively adventure exploration",
    "anh em":       "siblings travel social fun adventure bonding flexible",
    "chị em":       "friends travel social wellness fun relaxed flexible experience",
    "người thân":   "family travel comfortable gentle scenic cultural bonding",
    "cả nhà":       "family travel all inclusive comfortable activities bonding experience",

    # English
    "solo":         "solo travel independent flexible self discovery peaceful exploration",
    "alone":        "solo travel independent flexible self paced peaceful experience",
    "couple":       "couple travel romantic intimate private scenic experience",
    "family":       "family travel kid friendly safe comfortable activities bonding",
    "friends":      "group travel social fun nightlife activities adventure",
    "group":        "group travel social activities flexible variety experience",
    "newlyweds":    "honeymoon couple travel romantic luxury private resort experience",
    "students":     "student travel budget backpacker social hostel affordable fun",
    "backpackers":  "backpacker travel budget hostel social flexible exploration",
    "colleagues":   "team travel group team building social activities",
    "elderly":      "senior travel accessible comfortable gentle cultural heritage experience",
    "seniors":      "senior travel accessible comfortable gentle cultural heritage",
    "kids":         "kids travel safe fun activities shallow beach educational",
    "teenagers":    "teen travel active fun social outdoor adventure",
    "retirees":     "retiree travel comfortable accessible scenic cultural experience",
    "siblings":     "siblings travel social fun adventure bonding flexible",
    "coworkers":    "team travel organized group activities social bonding",
    "parents":      "family travel parents comfortable gentle scenic cultural",

    # Vietnamese synonyms
    "hai vợ chồng":  "couple travel romantic private intimate resort scenic",
    "cả gia đình":   "family travel all inclusive comfortable activities bonding",
    "cả nhóm":      "group travel social activities flexible organized experience",
    "cặp đôi trẻ":   "young couple travel romantic scenic private experience",
    "nhóm cười":    "group travel celebration social festive fun activities",
    "hưu trí":      "retiree travel comfortable accessible gentle cultural experience",
    "thanh niên":   "young adult travel active social fun budget adventure",
    "thiếu nhi":     "kids travel safe fun educational activities accessible",
    "sĩ quan":      "team travel organized group activities structured",
    "người cao tuổi":"senior travel accessible gentle comfortable cultural experience",

    # English synonyms
    "pairs":        "couple travel romantic private intimate scenic experience",
    "duo":          "couple travel romantic private scenic experience",
    "trio":         "small group travel social fun flexible experience",
    "squad":        "group travel social fun adventure activities",
    "crew":         "group travel social activities adventure fun",
    "party":        "group travel social activities organized fun",
    "mates":        "group travel friends social fun adventure",
    "clan":         "family travel comfortable activities bonding experience",
    "pack":         "group travel outdoor adventure social flexible",
    "lovebirds":    "couple travel romantic intimate private resort experience",
}
# ═════════════════════════════════════════════════════════════
# C. TRIP DURATION (LOW WEIGHT)
# ═════════════════════════════════════════════════════════════
TRIP_DURATION: dict[str, str] = {
    # Vietnamese
    "một ngày":     "short trip travel",
    "hai ngày":     "short trip travel",
    "ba ngày":      "short trip travel",
    "bốn ngày":     "short trip travel",
    "năm ngày":     "short trip travel",
    "một tuần":     "long travel",
    "hai tuần":     "long travel",
    "dài ngày":     "long travel",
    "ngắn ngày":    "short trip travel",
    "vài ngày":     "short trip travel",
    "cả tháng":     "long travel",

    # English
    "overnight":    "short trip travel",
    "fortnight":    "long travel",
    "monthly":      "long travel",
    "short":        "short trip travel",
    "long":         "long travel",
    "extended":     "long travel",
    "quick trip":   "short trip travel",

    # Vietnamese synonyms
    "một buổi":     "short trip travel",
    "vài giờ":      "short trip travel",
    "nửa ngày":     "short trip travel",
    "sáu ngày":     "long travel",
    "ba tuần":      "long travel",
    "cả năm":       "long travel",

    # English synonyms
    "day trip":     "short trip travel",
    "half-day":     "short trip travel",
    "3 days":       "short trip travel",
    "4 days":       "short trip travel",
    "5 days":       "short trip travel",
    "one week":     "long travel",
    "two weeks":    "long travel",
    "a month":      "long travel",
    "all summer":   "long travel",
    "gap year":     "long travel",
}

# ═════════════════════════════════════════════════════════════
# D. TRIP DISTANCE (LOW WEIGHT)
# ═════════════════════════════════════════════════════════════
TRIP_DISTANCE: dict[str, str] = {
    # Vietnamese
    "gần":          "nearby travel",
    "gần nhà":      "nearby travel",
    "trong nước":   "domestic travel",
    "quốc tế":      "international travel",
    "xa":           "far travel",
    "nước ngoài":   "international travel",
    "trong vùng":   "nearby travel",
    "khắp nơi":     "anywhere travel",

    # English
    "nearby":       "nearby travel",
    "domestic":     "domestic travel",
    "international":"international travel",
    "overseas":     "international travel",
    "abroad":       "international travel",
    "far":          "far travel",
    "regional":     "nearby travel",
    "cross-country":"domestic travel",
    "worldwide":    "international travel",

    # Vietnamese synonyms
    "rất gần":      "nearby travel",
    "cách xa":      "far travel",
    "khu vực":      "nearby travel",
    "quốc nội":     "domestic travel",
    "xứ người":     "international travel",
    "khắp chốn":    "anywhere travel",
    "thành phố lớn":"urban travel",

    # English synonyms
    "local area":   "nearby travel",
    "close by":     "nearby travel",
    "far away":     "far travel",
    "foreign":      "international travel",
    "far off":      "far travel",
    "intercontinental":"international travel",
    "trans-national":"international travel",
}

# ═════════════════════════════════════════════════════════════
# E. BUDGET LEVEL (HIGH IMPACT)
# ═════════════════════════════════════════════════════════════
BUDGET_LEVEL: dict[str, str] = {
    # Vietnamese
    "tiết kiệm":    "budget travel cheap affordable hostel backpacker",
    "bình dân":     "mid range travel affordable comfortable",
    "trung bình":   "mid range travel balanced comfortable",
    "sang trọng":   "luxury travel premium resort exclusive",
    "vừa túi":      "budget travel affordable comfortable",
    "vừa ví":       "budget travel affordable comfortable",
    "cao cấp":      "luxury travel premium exclusive resort",
    "tằn tiện":     "budget travel cheap minimal backpacker",
    "phóng khoáng": "luxury travel premium high end",
    "không giới hạn":"luxury travel unlimited premium",
    "giá rẻ":       "budget travel cheap affordable",
    "hạng sang":    "luxury travel premium exclusive",
    "tiêu xài":     "luxury travel splurge premium",

    # English
    "budget":       "budget travel cheap affordable hostel",
    "affordable":   "mid range travel affordable comfortable",
    "moderate":     "mid range travel balanced",
    "upscale":      "premium travel quality comfortable",
    "luxury":       "luxury travel premium exclusive resort",
    "splurge":      "luxury travel premium high end",
    "premium":      "premium travel luxury quality",
    "cheap":        "budget travel cheap minimal",
    "free":         "budget travel low cost",
    "expensive":    "luxury travel premium exclusive",
    "frugal":       "budget travel minimal cheap",
    "lavish":       "luxury travel premium resort",
    "economical":   "budget travel affordable value",
    "mid-budget":   "mid range travel balanced comfortable",

    # Vietnamese synonyms
    "không tốn":     "budget travel cheap minimal",
    "rẻ":            "budget travel cheap",
    "phù hợp":       "mid range travel affordable",
    "không gioi hạn":"luxury travel unlimited",
    "xịt túi":       "budget travel very cheap",
    "vừa phải":      "mid range travel balanced",
    "dồng đều":      "mid range travel balanced",

    # English synonyms
    "inexpensive":   "budget travel affordable",
    "wallet-friendly":"budget travel affordable",
    "cost-effective":"budget travel value",
    "high-end":      "luxury travel premium",
    "pricey":        "luxury travel expensive",
    "bargain":       "budget travel cheap",
    "thrifty":       "budget travel minimal",
    "extravagant":   "luxury travel premium",
    "reasonable":    "mid range travel affordable",
    "blowout":       "luxury travel splurge",
}

# ═════════════════════════════════════════════════════════════
# F. PACE & STYLE (HIGH IMPACT)
# ═════════════════════════════════════════════════════════════
PACE: dict[str, str] = {
    # Vietnamese
    "chậm rãi":     "slow travel relaxed peaceful gentle experience scenic exploration",
    "thư thả":      "leisure travel slow relaxed comfortable experience scenic",
    "thoải mái":    "relaxed travel flexible comfortable no rush experience",
    "năng động":    "active travel energetic activities adventure exploration",
    "tự do":        "flexible travel spontaneous independent exploration free roam",
    "kế hoạch":     "planned travel structured itinerary organized experience",
    "linh hoạt":    "flexible travel adaptable spontaneous semi structured",
    "tự túc":       "independent travel self guided flexible exploration",
    "chill":        "relaxed travel slow peaceful no rush experience",
    "vội vã":       "fast paced travel packed activities efficient exploration",
    "tự lái":       "self drive travel road trip flexible independent scenic",
    "theo tour":    "guided travel organized tour structured itinerary",
    "phượt":        "backpacker travel flexible independent road trip adventure",
    "hướng dẫn":    "guided travel organized tour cultural sightseeing",

    # English
    "leisurely":    "slow travel relaxed scenic gentle experience",
    "relaxed":      "relaxed travel slow comfortable scenic experience",
    "packed":       "packed travel activities efficient exploration",
    "spontaneous":  "spontaneous travel flexible exploration adventure",
    "structured":   "structured travel planned organized itinerary",
    "guided":       "guided travel organized tour itinerary",
    "flexible":     "flexible travel adaptable spontaneous",
    "independent":  "independent travel self guided exploration",
    "organized":    "organized travel planned itinerary",
    "unplanned":    "spontaneous travel flexible open exploration",
    "self-drive":   "self drive travel road trip flexible exploration",
    "backpacking":  "backpacker travel budget flexible exploration",
    "fly-in":       "resort travel organized comfortable guided",
    "road trip":    "road trip travel scenic drive flexible exploration",
    "packaged":     "package tour travel organized all inclusive",

    # Vietnamese synonyms
    "không vội":     "slow travel relaxed no rush peaceful experience",
    "cần thời gian": "slow travel immersive relaxed exploration experience",
    "tự đi":        "independent travel flexible self guided exploration",
    "thích nghi":    "flexible travel adaptable spontaneous",
    "có người dẫn":  "guided travel organized tour itinerary",
    "tự đặt lịch":  "self planned travel independent flexible",
    "theo tiêu chuẩn":"organized travel planned structured itinerary",
    "phượt":         "backpacker travel flexible independent adventure",

    # English synonyms
    "unhurried":    "slow travel peaceful gentle exploration",
    "easygoing":    "relaxed travel flexible comfortable",
    "whirlwind":    "fast travel packed activities efficient",
    "impromptu":    "spontaneous travel flexible exploration",
    "regimented":   "structured travel planned organized",
    "escorted":     "guided travel organized tour",
    "free form":    "flexible travel spontaneous exploration",
    "self-planned": "independent travel flexible self guided",
    "methodical":   "organized travel planned structured",
    "freewheeling": "flexible travel spontaneous adventure",
}

ALL_CONTEXT: dict[str, str] = {
    **SEASON_WEATHER,
    **SOCIAL_GROUP,
    **TRIP_DURATION,
    **TRIP_DISTANCE,
    **BUDGET_LEVEL,
    **PACE,
}