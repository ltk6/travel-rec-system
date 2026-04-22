"""
maps/emotions.py
================
Maps emotional states and mental vibes to travel experience keywords.
Translates "how the user feels" into "what kind of trip they need".

This mapping allows the preprocessor to capture subtle sentiment from 
user-written text and convert it into high-value embedding dimensions.

─────────────────────────────────────────────────────────────
SECTION INDEX
─────────────────────────────────────────────────────────────
  A. EXHAUSTION & STRESS — restorative, slow, spa, nature
  B. BOREDOM & STAGNATION — stimulating, adventure, variety
  C. SADNESS & LONELINESS — uplifting, social, healing, scenic
  D. ROMANCE & INTIMACY   — couple, sunset, private, luxury
  E. CURIOSITY & LEARNING — cultural, heritage, educational
  F. EXCITEMENT & THRILL — adrenaline, extreme, active
  G. NOSTALGIA & HERITAGE — vintage, traditional, old-town
  H. SOCIAL FATIGUE       — solo, secluded, off-grid, quiet

IMPLEMENTATION NOTES
──────────────────────────────────────────────────────────────────────────
  • Keys are prioritized by specificity (long phrases before short).
  • Substring clashes are strictly forbidden to ensure deterministic mapping.
  • Emotional values are biased toward positive/solution-oriented travel.
──────────────────────────────────────────────────────────────────────────
"""

# ═════════════════════════════════════════════════════════════
# A. EXHAUSTION & STRESS
# ═════════════════════════════════════════════════════════════
EXHAUSTION_STRESS: dict[str, str] = {
    # ── Vietnamese ──────────────────────────────────────────
    "mệt mỏi":      "relaxation travel spa resort rest wellness recovery experience",
    "kiệt sức":     "deep rest travel wellness spa secluded resort recovery",
    "kiệt lực":     "deep rest travel resort spa wellness recovery nature",
    "uể oải":       "light travel nature walking gentle activities fresh air",
    "căng thẳng":   "relaxation travel nature peaceful meditation wellness retreat",
    "lo lắng":      "calm travel nature serene meditation mindfulness peaceful",
    "áp lực":       "escape travel nature secluded quiet retreat stress relief",
    "stress":       "relaxation travel nature wellness meditation peaceful",
    "bồn chồn":     "calm travel quiet nature walking meditation",
    "quá tải":      "escape travel off grid nature quiet secluded retreat",
    "mất ngủ":      "calm travel serene nature spa rest wellness retreat",
    "đau đầu":      "quiet travel nature fresh air spa wellness peaceful",
    "chán việc":    "escape travel adventure outdoor discovery new experience",
    "cần nghỉ":     "relaxation travel rest resort peaceful slow experience",
    "cần đổi gió":  "new experience travel discovery outdoor fresh exploration",
    "muốn thoát":   "escape travel remote nature secluded off grid retreat",
    "quá sức":      "recovery travel rest nature wellness spa gentle experience",
    "áp lực cao":   "escape travel secluded nature retreat mindfulness peaceful",
    "không ngủ":    "calm travel quiet nature spa rest wellness retreat",
    "thiếu ngủ":    "rest travel peaceful quiet nature spa recovery",
    "cạn sức":      "deep rest travel wellness resort recovery nature spa",
    "muốn nghỉ":    "resort travel beach quiet peaceful rest nature",
    "thư giãn":     "relaxation travel spa wellness peaceful resort experience",
    "nghỉ ngơi":    "rest travel resort peaceful nature quiet experience",
    "đầu nặng":     "fresh air travel outdoor nature scenic quiet spa",
    "người mệt":    "spa resort travel rest wellness slow experience nature",
    "tâm lý nặng":  "meditation travel retreat nature quiet mindfulness peaceful",

    # ── English ──────────────────────────────────────────
    "exhausted":    "spa travel wellness resort secluded rest recovery",
    "burned out":   "deep rest travel wellness retreat nature slow experience",
    "burnt out":    "spa travel wellness nature secluded recovery",
    "feeling tired":"relaxation travel resort beach quiet rest",
    "drained":      "nature travel retreat wellness calm recovery",
    "stressed":     "relaxation travel spa nature retreat peaceful wellness meditation",
    "anxious":      "calm travel serene nature meditation mindfulness peaceful",
    "overwhelmed":  "escape travel secluded quiet nature off grid retreat",
    "tense":        "spa travel wellness relaxation peaceful",
    "on edge":      "peaceful travel nature quiet retreat mindfulness",
    "fatigued":     "rest travel resort quiet beach gentle wellness",
    "worn out":     "recovery travel rest resort peaceful nature",
    "overworked":   "escape travel retreat wellness nature rest spa",
    "need a break": "short trip travel getaway nature rest peaceful",
    "need rest":    "spa travel resort quiet beach wellness",
    "recharge":     "nature travel retreat spa wellness peaceful recovery",
    "no energy":    "slow travel peaceful resort rest gentle nature",
    "run down":     "wellness spa travel recovery resort rest quiet",
    "mental fatigue":"meditation travel retreat nature quiet mindfulness spa",
    "frazzled":     "spa travel retreat quiet nature peaceful rest wellness",
    "depleted":     "deep rest travel resort nature wellness recovery spa",
    "weary":        "slow travel peaceful resort spa quiet nature",
    "wrecked":      "deep rest travel secluded spa wellness recovery nature",
    "burnout":      "deep rest travel wellness nature secluded retreat spa",
    "spent":        "rest travel resort spa quiet nature recovery",
    "numb":         "nature travel scenic peaceful uplifting wellness retreat",
    "disconnected": "community travel local social scenic peaceful experience",

    # ── Synonyms ──────────────────────────────────────────
    "kiệt quệ":     "deep rest travel wellness spa secluded recovery nature",
    "hao mòn":      "rest travel recovery wellness resort nature",
    "suy nhược":    "gentle travel wellness spa recovery rest nature",
    "ngộp thở":     "escape travel open nature fresh air outdoor peaceful",
    "mệt đuối":     "deep rest travel spa wellness secluded resort recovery",
    "mệt trí":      "meditation travel retreat nature quiet mindfulness peaceful",
    "muốn yên":     "quiet travel peaceful nature secluded retreat spa",
    "cần xa":       "escape travel remote nature secluded off grid retreat",
    "thoát ly":     "escape travel adventure outdoor discovery new experience",
    "xuống dốc":    "recovery travel rest nature wellness resort spa",
    "lethargic":    "slow travel peaceful resort spa rest nature",
    "sluggish":     "rest travel gentle nature quiet spa wellness",
    "fried":        "deep rest travel secluded spa wellness recovery nature",
    "zapped":       "rest travel recovery wellness resort spa nature",
    "wiped out":    "deep rest travel spa secluded recovery resort wellness",
    "worn thin":    "escape travel retreat nature rest wellness",
    "need vacation":"resort travel beach peaceful rest nature getaway",
    "lifeless":     "nature travel scenic uplifting vibrant recovery",
    "at capacity":  "escape travel secluded nature off grid quiet retreat",
    "hollow":       "nature travel scenic community uplifting peaceful",
}

# ═════════════════════════════════════════════════════════════
# B. BOREDOM & STAGNATION
# ═════════════════════════════════════════════════════════════
BOREDOM: dict[str, str] = {
    # ── Vietnamese ──────────────────────────────────────────
    "nhàm chán":         "entertainment travel activities nightlife adventure variety stimulating experience",
    "buồn tẻ":           "vibrant travel lively entertainment variety unique experience",
    "tẻ nhạt":           "stimulating travel discovery adventure entertainment variety",
    "mới mẻ":            "new experience travel discovery unique adventure stimulating",
    "tìm kiếm":          "exploration travel discovery adventure outdoor cultural experience",
    "kích thích":        "adventure travel adrenaline outdoor stimulating activities sport",
    "phiêu lưu":         "adventure travel outdoor trekking discovery bold exploration",
    "thiếu hứng":        "vibrant travel discovery adventure lively stimulating colorful",
    "muốn đi":           "travel getaway adventure outdoor new discovery experience",
    "thay đổi":          "new experience travel discovery vibrant stimulating variety",
    "vô vị":             "vibrant travel colorful lively stimulating entertainment",
    "thiếu cảm xúc":     "vibrant travel adventure new experience colorful stimulating",
    "muốn trải":         "new experience travel cultural authentic local immersive",
    "lặp lại":           "discovery travel unique variety new experience change",

    # ── English ──────────────────────────────────────────
    "bored":             "entertainment travel activities nightlife adventure variety stimulating experience",
    "stagnant":          "new experience travel discovery stimulating vibrant",
    "monotonous":        "variety travel unique discovery adventure stimulating",
    "dull":              "vibrant travel colorful lively entertainment adventure",
    "restless":          "adventure travel outdoor active discovery exploration new",
    "stuck in a rut":    "new experience travel offbeat discovery unique adventure",
    "adventure":         "adventure travel trekking outdoor adrenaline sport exploration",
    "excitement":        "adventure travel adrenaline vibrant lively entertainment sport",
    "craving new":       "unique travel discovery new experience offbeat hidden gem",
    "to explore":        "exploration travel discovery outdoor cultural adventure new",
    "uninspired":        "scenic travel beautiful art cultural discovery vibrant",
    "flat":              "vibrant travel lively colorful energetic stimulating activities",
    "listless":          "vibrant travel outdoor active discovery new experience",
    "jaded":             "unique travel hidden gem offbeat authentic discovery",
    "idle":              "active travel outdoor adventure discovery sport variety",
    "going nowhere":     "new experience travel discovery adventure change stimulating",
    "need change":       "new experience travel discovery stimulating change variety",
    "purposeless":       "meaningful travel cultural nature discovery community authentic",
    "unexcited":         "adventure travel vibrant stimulating colorful lively outdoor",

    # ── Synonyms ──────────────────────────────────────────
    "ngán ngẩm":         "new experience travel discovery unique adventure variety stimulating",
    "thờ ơ":             "vibrant travel lively colorful stimulating adventure discovery",
    "vô cảm":            "uplifting travel vibrant scenic colorful stimulating new experience",
    "thiếu động lực":    "adventure travel outdoor discovery stimulating variety active",
    "không hứng":        "vibrant travel discovery lively entertainment stimulating colorful",
    "cần vui":           "fun travel lively cheerful social entertainment activities",
    "trơ trọi":          "vibrant travel colorful lively stimulating social entertainment",
    "đơn điệu":          "variety travel unique discovery adventure stimulating lively",
    "thiếu cảm hứng":    "scenic travel cultural art discovery vibrant stimulating",
    "apathetic":         "vibrant travel lively outdoor active discovery new experience",
    "disengaged":        "adventure travel outdoor stimulating discovery cultural new",
    "unmotivated":       "adventure travel discovery outdoor stimulating variety active",
    "tedious":           "vibrant travel unique discovery adventure variety stimulating",
    "stale":             "fresh travel new experience discovery offbeat unique",
    "in a funk":         "uplifting travel vibrant colorful lively adventure outdoor",
    "no spark":          "vibrant travel colorful adventure lively stimulating outdoor",
    "same old":          "new experience travel offbeat discovery unique hidden gem",
    "repetitive":        "variety travel discovery adventure unique stimulating new",
}
# ═════════════════════════════════════════════════════════════
# C. SADNESS & LONELINESS
# ═════════════════════════════════════════════════════════════
SADNESS: dict[str, str] = {
    # ── Vietnamese ──────────────────────────────────────────
    "đang buồn":    "uplifting travel scenic colorful cheerful vibrant experience",
    "cô đơn":       "social travel community lively festival crowd people watching",
    "trống rỗng":   "vibrant travel lively social cultural discovery experience",
    "chán nản":     "new experience travel discovery adventure vibrant stimulating",
    "nặng nề":      "light travel cheerful colorful scenic uplifting",
    "nhớ nhà":      "cozy travel warm local community comfort familiar",
    "đau khổ":      "healing travel scenic peaceful beautiful gentle nature",
    "lạc lối":      "discovery travel self exploration solo nature peaceful",
    "chữa lành":    "healing travel wellness spa nature peaceful scenic retreat",
    "quên đi":      "adventure travel stimulating vibrant discovery new experience",
    "kết nối":      "community travel local social festival people cultural",
    "thiếu bạn":    "social travel community lively festival crowd friends",
    "xa nhà":       "cozy travel warm local community comfort familiar",
    "cảm thấy lạc": "discovery travel nature solo peaceful scenic mindfulness",
    "muốn vui":     "fun travel lively cheerful uplifting social festival",
    "nước mắt":     "healing travel peaceful scenic beautiful gentle nature",
    "chán đời":     "discovery travel nature vibrant uplifting adventure scenic",
    "cần chia sẻ":  "social travel community local people cultural authentic",
    "mất phương":   "discovery travel self exploration nature solo peaceful scenic",

    # ── English ──────────────────────────────────────────
    "feeling sad":  "uplifting travel scenic beautiful colorful cheerful",
    "lonely":       "social travel community festival crowd lively people watching",
    "empty":        "vibrant travel lively social cultural stimulating experience",
    "down":         "cheerful travel colorful vibrant warm social",
    "heartbroken":  "scenic travel peaceful healing nature beautiful",
    "melancholy":   "scenic travel beautiful gentle nature peaceful artistic",
    "homesick":     "cozy travel warm community local familiar comfort",
    "grieving":     "peaceful travel healing nature serene quiet gentle",
    "lost":         "self discovery travel solo nature peaceful scenic exploration",
    "healing":      "wellness travel spa nature peaceful scenic healing retreat",
    "feeling low":  "uplifting travel cheerful scenic colorful vibrant entertainment",
    "connection":   "social travel community local festival people culture",
    "heartache":    "scenic travel peaceful healing nature beautiful gentle",
    "miserable":    "uplifting travel colorful vibrant cheerful scenic festival",
    "hopeless":     "inspiring travel scenic beautiful nature vibrant uplifting",
    "depressed":    "uplifting travel nature vibrant cheerful scenic community",
    "isolated":     "social travel community festival local people lively",
    "abandoned":    "cozy travel warm community local social friendly",
    "missing home": "cozy travel familiar warm local community comfort",
    "need comfort": "cozy travel warm local community familiar gentle scenic",

    # ── Synonyms ──────────────────────────────────────────
    "tổn thương":   "healing travel scenic peaceful beautiful gentle nature",
    "thất vọng":    "uplifting travel scenic colorful cheerful vibrant new experience",
    "u uất":        "scenic travel peaceful healing nature uplifting beautiful",
    "bi quan":      "uplifting travel inspiring scenic beautiful vibrant colorful",
    "ủ rũ":         "uplifting travel cheerful colorful vibrant lively scenic",
    "cô quạnh":     "social travel community lively festival local people",
    "chìm đắm":     "uplifting travel vibrant scenic colorful healing nature",
    "tâm trạng xấu":"uplifting travel cheerful vibrant colorful scenic festival",
    "sorrowful":    "scenic travel peaceful healing beautiful nature gentle",
    "tearful":      "healing travel scenic peaceful nature beautiful gentle",
    "desolate":     "community travel social local festival lively people",
    "forlorn":      "warm cozy travel local community comfort familiar",
    "aching":       "scenic travel peaceful healing nature beautiful gentle",
    "broken":       "healing travel wellness spa nature peaceful scenic",
    "gloomy":       "uplifting travel colorful scenic vibrant cheerful outdoor",
    "unhappy":      "uplifting travel scenic cheerful colorful vibrant festival",
    "hurt":         "healing travel peaceful scenic nature beautiful gentle",
    "wounded":      "healing travel nature scenic peaceful beautiful wellness",
}
# ═════════════════════════════════════════════════════════════
# D. ROMANCE & INTIMACY
# ═════════════════════════════════════════════════════════════
ROMANCE: dict[str, str] = {
    # ── Vietnamese ──────────────────────────────────────────
    "lãng mạn":     "romantic travel sunset couple candlelight scenic private intimate experience",
    "kỷ niệm":      "romantic travel special anniversary couple scenic experience",
    "trăng mật":    "honeymoon travel luxury romantic private resort scenic experience",
    "tình cảm":     "romantic travel intimate scenic private couple",
    "gần nhau":     "intimate travel couple romantic scenic private quiet",
    "ngày cưới":    "anniversary travel romantic luxury scenic private couple resort",
    "cầu hôn":      "scenic travel viewpoint private romantic sunset luxury experience",
    "mới cưới":     "honeymoon travel luxury romantic private resort scenic",
    "gắn kết":      "romantic travel intimate private scenic couple quiet",
    "người yêu":    "romantic travel couple scenic private intimate sunset",
    "tình yêu":     "romantic travel couple scenic intimate private sunset",
    "yêu nhau":     "romantic travel private scenic couple intimate luxury",
    "đêm lãng mạn": "romantic travel candlelight sunset scenic private couple experience",
    "tâm sự":       "intimate travel private quiet scenic couple peaceful",
    "bên nhau":     "couple travel intimate private scenic romantic peaceful",
    "hẹn hò":       "romantic travel date scenic private couple intimate experience",
    "vợ chồng mới": "honeymoon travel romantic luxury private resort scenic",
    "tặng quà":     "romantic travel special luxury scenic private couple",
    "surprise trip": "romantic travel special scenic private couple luxury experience",

    # ── English ──────────────────────────────────────────
    "romantic":     "romantic travel sunset couple private intimate scenic experience",
    "anniversary":  "romantic travel special scenic luxury private couple",
    "honeymoon":    "honeymoon travel luxury romantic private resort scenic",
    "proposal":     "scenic travel viewpoint private romantic sunset luxury experience",
    "valentine":    "romantic travel couple scenic private luxury sunset",
    "date":         "romantic travel scenic intimate private couple dinner experience",
    "in love":      "romantic travel scenic intimate private couple sunset",
    "newlywed":     "honeymoon travel luxury romantic private resort beach scenic",
    "rekindling":   "romantic travel intimate private scenic couple quiet resort",
    "quality time": "romantic travel private scenic couple intimate quiet peaceful",
    "together":     "couple travel intimate private scenic romantic quiet",
    "just us":      "private travel couple intimate scenic romantic secluded",
    "soulmate":     "romantic travel scenic luxury private couple intimate",
    "sweetheart":   "romantic travel intimate private couple scenic sunset",
    "newly engaged": "romantic travel scenic viewpoint private couple luxury",
    "elopement":    "intimate travel private romantic scenic couple secluded",

    # ── Synonyms ──────────────────────────────────────────
    "tình nhân":    "romantic travel couple scenic private intimate sunset",
    "cùng nhau":    "couple travel intimate private scenic romantic peaceful",
    "ngọt ngào":    "romantic travel intimate private scenic couple gentle",
    "ấm áp":        "romantic travel intimate warm cozy couple private scenic",
    "yêu thương":   "romantic travel couple intimate scenic private beautiful",
    "bất ngờ":      "romantic travel special scenic private couple luxury",
    "tình nhớ":     "romantic travel scenic beautiful intimate couple private",
    "hẹn ước":      "romantic travel couple scenic private intimate promise",
    "romance":      "romantic travel scenic couple private intimate beautiful",
    "affectionate": "romantic travel intimate couple private scenic warm",
    "passionate":   "romantic travel couple intimate scenic private vibrant",
    "intimate":     "intimate travel private couple romantic scenic quiet",
    "tender":       "romantic travel intimate gentle couple private scenic",
    "devoted":      "romantic travel couple private scenic intimate resort",
    "smitten":      "romantic travel scenic couple intimate private sunset",
    "lovesick":     "romantic travel couple scenic private intimate beautiful",
    "adoring":      "romantic travel intimate couple private scenic warm",
    "committed":    "romantic travel couple private scenic intimate resort",
}

# ═════════════════════════════════════════════════════════════
# E. CURIOSITY & LEARNING
# ═════════════════════════════════════════════════════════════
CURIOSITY: dict[str, str] = {
    # ── Vietnamese ──────────────────────────────────────────
    "tò mò":        "discovery exploration cultural local authentic learning",
    "muốn học":     "educational cultural heritage museum workshop local",
    "hiểu thêm":    "cultural heritage history museum local authentic",
    "trải nghiệm":  "new-experience cultural authentic local immersive",
    "khám phá":     "exploration discovery adventure outdoor cultural new",
    "tìm hiểu":     "discovery cultural learning heritage educational",
    "ham học":      "educational cultural museum workshop heritage tour",
    "yêu văn hóa":  "cultural heritage local tradition festival community",
    "tìm sử":       "history heritage monument museum ancient educational",
    "yêu nghệ":     "art gallery museum creative cultural exhibition",
    "đam mê đọc":   "literary heritage cultural intellectual book local",
    "muốn hiểu":    "cultural heritage history museum local learning",
    "thích mới":    "new-experience discovery cultural authentic diverse",
    "học hỏi":      "educational heritage cultural museum workshop local",
    "cởi mở":       "diverse cultural authentic open-minded discovery",
    "tìm bản thân": "self-discovery solo nature peaceful scenic exploration",
    # ── English ──────────────────────────────────────────
    "curious":      "discovery exploration cultural local learning new-experience",
    "intellectual": "museum heritage cultural art history educational",
    "to discover":     "discovery off-beaten-path hidden-gem new experience",
    "learner":      "educational cultural workshop heritage immersive",
    "inspiration":  "scenic cultural discovery art heritage beautiful",
    "open-minded":  "discovery cultural new-experience diverse authentic",
    "exploration":  "exploration discovery outdoor adventure cultural new",
    "cultures":      "cultural heritage local tradition festival community",
    "histories":      "history heritage monument museum ancient educational",
    "arts":          "art gallery museum creative cultural exhibition",
    "knowledge":    "educational cultural museum heritage learning workshop",
    "learning":     "educational cultural heritage museum workshop immersive",
    "research":     "heritage museum cultural educational discovery authentic",
    "mindful":      "mindfulness meditation nature peaceful scenic retreat",
    "growth":       "educational cultural discovery heritage authentic new",
    # ── Synonyms ──────────────────────────────────────────
    "say mê":       "passionate cultural art discovery heritage immersive",
    "thắc mắc":     "discovery exploration cultural local learning curious",
    "tìm tòi":      "exploration discovery adventure outdoor cultural new",
    "muốn biết":    "discovery cultural heritage educational learning authentic",
    "ham tìm":      "exploration discovery cultural adventure outdoor new",
    "tư duy":       "intellectual cultural heritage educational discovery mindful",
    "tiếp thu":     "educational cultural heritage workshop immersive learning",
    "nghiên cứu":   "heritage museum cultural educational discovery authentic",
    "thích học":    "educational cultural heritage museum workshop local",
    "inquisitive":  "discovery exploration cultural local learning curious",
    "studious":     "educational cultural heritage museum workshop immersive",
    "thoughtful":   "mindful cultural scenic nature peaceful discovery",
    "enlightened":  "cultural heritage educational discovery authentic local",
    "seeking":      "exploration discovery cultural adventure outdoor new",
    "investigative":"discovery exploration heritage educational authentic local",
    "bookish":      "heritage cultural educational museum literary authentic",
    "academic":     "educational heritage museum cultural scholarly discovery",
    "philosophical":"mindful peaceful nature reflection cultural discovery",
    "wondering":    "discovery scenic exploration curious cultural new",
}

# ═════════════════════════════════════════════════════════════
# F. EXCITEMENT & THRILL
# ═════════════════════════════════════════════════════════════
EXCITEMENT: dict[str, str] = {
    # ── Vietnamese ──────────────────────────────────────────
    "hứng khởi":    "adventure outdoor adrenaline sport active lively",
    "mạo hiểm":     "adventure adrenaline outdoor extreme sport trekking",
    "thử thách":    "challenge sport outdoor adventure adrenaline extreme",
    "năng lượng":   "active outdoor adventure sport lively energetic",
    "cảm giác mạnh":"adrenaline extreme sport adventure outdoor thrilling",
    "sẵn sàng":     "flexible outdoor adventure active discovery sport",
    "muốn thử":     "new-experience adventure outdoor active sport",
    "bứt phá":      "extreme outdoor adrenaline challenge sport adventure",
    "mạnh mẽ":      "active outdoor sport adventure energetic challenge",
    "tràn đầy":     "vibrant energetic active outdoor sport adventure",
    "quyết tâm":    "challenge outdoor sport adventure bold active",
    "bùng cháy":    "adrenaline vibrant energetic active sport outdoor",
    "cao hứng":     "adventure outdoor adrenaline active energetic sport",
    "đam mê":       "passionate adventure outdoor sport active discovery",
    "phấn khích":   "adventure lively active outdoor sport energetic",
    # ── English ──────────────────────────────────────────
    "so excited":   "adventure lively active outdoor sport adrenaline",
    "pumped":       "adrenaline adventure outdoor sport active energetic",
    "thrill-seeking":"adrenaline extreme sport adventure outdoor thrilling",
    "energetic":    "active outdoor sport adventure lively energetic",
    "bold":         "adventure outdoor bold exploration off-beaten-path",
    "push limits":  "extreme sport adventure adrenaline challenge outdoor",
    "feel alive":   "adventure outdoor active adrenaline scenic stimulating",
    "ready":        "flexible outdoor adventure active discovery",
    "adrenaline":   "adrenaline extreme sport adventure outdoor thrilling",
    "daring":       "adventure bold outdoor extreme adrenaline sport",
    "fearless":     "adventure bold extreme outdoor adrenaline sport",
    "wild":         "adventure wild outdoor remote extreme nature",
    "fired up":     "active outdoor energetic adventure sport adrenaline",
    "go-getter":    "active outdoor adventure flexible sport discovery",
    "hyped":        "lively vibrant energetic outdoor adventure sport",
    "unstoppable":  "active outdoor bold adventure sport adrenaline",
    # ── Synonyms ──────────────────────────────────────────
    "nhiệt huyết":  "passionate active outdoor adventure sport energetic",
    "xung phong":   "bold active outdoor adventure sport adrenaline",
    "thách thức":   "challenge sport outdoor adventure adrenaline extreme",
    "gan lì":       "bold outdoor adventure extreme tenacious sport",
    "chinh phục":   "adventure outdoor summit challenge adrenaline sport",
    "bùng nổ":      "adrenaline vibrant energetic outdoor sport adventure",
    "hừng hực":     "energetic active outdoor adrenaline sport adventure",
    "lì lợm":       "tenacious outdoor adventure bold sport challenge",
    "không sợ":     "fearless bold outdoor adventure adrenaline sport",
    "raring":       "active outdoor adventure sport discovery flexible",
}

# ═════════════════════════════════════════════════════════════
# G. NOSTALGIA & HERITAGE
# ═════════════════════════════════════════════════════════════
NOSTALGIA: dict[str, str] = {
    # ── Vietnamese ──────────────────────────────────────────
    "hoài cổ":      "heritage historic vintage traditional old-town atmosphere",
    "quá khứ":      "heritage nostalgia historic traditional old-town museum",
    "về nguồn":     "cultural roots heritage traditional local authentic",
    "bản sắc":      "cultural identity heritage local authentic traditional",
    "truyền thống": "traditional heritage cultural local craft festival",
    "cổ xưa":       "heritage ancient historic traditional atmosphere vintage",
    "nhớ xưa":      "nostalgic heritage vintage traditional old-town scenic",
    "tìm gốc":      "cultural roots heritage local authentic community",
    "hương xưa":    "heritage vintage nostalgic atmospheric old-town scenic",
    "thời xưa":     "historic vintage traditional heritage atmosphere cultural",
    "di sản":       "heritage historic ancient monument museum cultural",
    "cội nguồn":    "cultural roots heritage local authentic traditional",
    "ký ức":        "nostalgic heritage scenic beautiful peaceful traditional",
    "xưa cũ":       "vintage heritage atmospheric traditional old-town historic",
    # ── English ──────────────────────────────────────────
    "nostalgic":    "heritage nostalgia vintage traditional historic atmosphere",
    "sentimental":  "heritage nostalgic scenic beautiful peaceful traditional",
    "old soul":     "heritage historic traditional atmospheric vintage old-town",
    "old towns":    "old-town heritage cobblestone charming historic atmospheric",
    "roots trip":   "cultural roots heritage local authentic community",
    "vintage":      "vintage heritage atmospheric old-town traditional charm",
    "historical":   "historical heritage monument ancient museum educational",
    "timeless":     "heritage scenic beautiful traditional cultural peaceful",
    "classic":      "classic heritage traditional scenic cultural historic",
    "antique":      "heritage vintage antique old-town atmospheric traditional",
    "ancient":      "ancient heritage historic monument museum cultural",
    "ancestral":    "cultural roots heritage local authentic traditional",
    "preserved":    "heritage conservation historic traditional authentic cultural",
    # ── Synonyms ──────────────────────────────────────────
    "thương nhớ":   "nostalgic scenic beautiful peaceful gentle heritage",
    "cổ điển":      "heritage classic traditional atmospheric vintage cultural",
    "nhớ lại":      "nostalgic heritage scenic beautiful traditional peaceful",
    "hoài niệm":    "nostalgic heritage scenic beautiful traditional atmospheric",
    "dân gian":     "folk-culture heritage traditional local authentic craft",
    "lịch sử":      "history heritage monument ancient museum educational",
    "tiền nhân":    "ancestral heritage cultural roots traditional authentic",
    "văn vật":      "cultural-artifact heritage museum traditional authentic historic",
    "nhớ quê":      "nostalgic rural countryside local familiar cozy heritage",
    "reminiscing":  "nostalgic heritage scenic traditional beautiful peaceful",
    "wistful":      "nostalgic scenic beautiful peaceful traditional heritage",
    "retro":        "vintage heritage atmospheric old-town traditional charm",
    "bygone":       "heritage historic traditional atmospheric vintage old-town",
    "olden":        "heritage historic traditional old-town atmospheric vintage",
    "storied":      "heritage historic scenic cultural traditional beautiful",
    "legendary":    "heritage scenic historic iconic cultural traditional",
    "old-world":    "heritage traditional atmospheric vintage charming old-town",
    "classic":      "heritage classic traditional scenic cultural historic",
}

# ═════════════════════════════════════════════════════════════
# H. SOCIAL FATIGUE
# ═════════════════════════════════════════════════════════════
SOCIAL_FATIGUE: dict[str, str] = {
    # ── Vietnamese ──────────────────────────────────────────
    "mệt xã hội":   "solo quiet secluded nature peaceful off-grid retreat",
    "cần không gian":"spacious open nature quiet secluded peaceful",
    "né đám đông":  "secluded quiet off-beaten-path peaceful remote nature",
    "ngại tiếp xúc":"solo quiet peaceful secluded nature gentle",
    "cần yên tĩnh": "quiet peaceful tranquil secluded nature retreat",
    "suy nghĩ":     "solo peaceful quiet nature meditation reflection",
    "muốn riêng":   "private secluded solo quiet nature off-grid",
    "cần nghỉ xã hội":"retreat quiet nature secluded solo off-grid",
    "tránh đám đông":"remote peaceful off-beaten-path secluded quiet nature",
    "nội tâm":      "solo introspective peaceful nature quiet reflection",
    "thích yên":    "quiet peaceful tranquil secluded nature gentle",
    "không muốn gặp":"secluded remote quiet nature solo off-grid",
    "cần tĩnh tâm": "meditation retreat peaceful nature quiet mindfulness",
    # English
    "introverted":  "solo quiet secluded nature peaceful gentle off-grid",
    "need space":   "open spacious nature quiet secluded peaceful",
    "avoid crowds": "secluded quiet off-beaten-path remote peaceful hidden-gem",
    "alone time":   "solo quiet secluded nature peaceful reflection",
    "quiet retreat":"retreat quiet peaceful nature secluded wellness meditation",
    "need quiet":   "quiet peaceful tranquil secluded nature serene",
    "need solitude":"solo secluded quiet nature peaceful retreat meditation",
    "contemplative":"peaceful quiet scenic nature meditation reflection solo",
    "withdrawn":    "solo quiet peaceful secluded nature gentle retreat",
    "reclusive":    "solo secluded quiet off-grid nature peaceful",
    "antisocial":   "solo remote secluded quiet nature off-grid",
    "private":      "private secluded solo quiet nature exclusive",
    "self-reliant": "solo independent flexible discovery nature peaceful",
    "off-grid":     "off-grid remote secluded nature quiet peaceful",
    # Vietnamese synonyms
    "hướng nội":    "solo quiet secluded nature peaceful introspective",
    "cần riêng":    "private secluded solo quiet nature off-grid",
    "muốn vắng":    "secluded remote quiet nature peaceful off-grid",
    "ghét ồn":      "quiet peaceful secluded nature tranquil off-grid",
    "cần im lặng":  "quiet silent peaceful nature secluded retreat",
    "sợ đám đông":  "secluded remote quiet nature peaceful off-grid",
    "muốn tĩnh":    "peaceful tranquil quiet nature secluded meditation",
    "thích vắng":   "secluded quiet remote nature peaceful off-grid",
    "tránh ồn":     "quiet peaceful nature secluded tranquil off-grid",
    # English synonyms
    "reserved":     "solo quiet secluded nature peaceful gentle",
    "hermit":       "remote secluded off-grid quiet nature solo",
    "homebody":     "cozy local familiar comfortable quiet peaceful",
    "shy":          "solo quiet gentle peaceful secluded nature",
    "recluse":      "remote secluded solo quiet nature off-grid",
    "quiet time":   "peaceful quiet nature secluded retreat gentle",
    "me time":      "solo quiet nature peaceful reflection secluded",
    "off radar":    "remote secluded off-grid quiet nature peaceful",
    "low-key":      "quiet peaceful gentle secluded nature relaxed",
    "detached":     "solo quiet secluded nature peaceful off-grid",
}

ALL_EMOTIONS: dict[str, str] = {
    **EXHAUSTION_STRESS,
    **BOREDOM,
    **SADNESS,
    **ROMANCE,
    **CURIOSITY,
    **EXCITEMENT,
    **NOSTALGIA,
    **SOCIAL_FATIGUE,
}