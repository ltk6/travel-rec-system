"""
seed_data.py
============
Raw location data — 20 locations spread across Vietnam, North to South.
No vectors here. Run embed_locations.py to generate vectors via N1.

Each location's description is written to maximise embedding quality:
  - full sentences capturing the *feeling* of the place, not just facts
  - mix of Vietnamese and travel-domain English keywords in tags
  - enough semantic content that cosine similarity against user queries
    will produce meaningful rankings in N4
"""

LOCATIONS = [

    # ── NORTHWEST ─────────────────────────────────────────────
    {
        "location_id": "loc_001",
        "metadata": {
            "name": "Fansipan Sapa",
            "description": (
                "Đỉnh núi cao nhất Đông Dương nằm giữa mây trắng bồng bềnh và rừng nguyên sinh Tây Bắc. "
                "Du khách có thể leo bộ qua những cung đường trekking thử thách hoặc lên cáp treo hiện đại "
                "để chinh phục nóc nhà Đông Dương ở độ cao 3.143m. Xung quanh là ruộng bậc thang vàng óng "
                "mùa lúa chín, làng bản H'Mông và Dao đỏ với trang phục thêu tay rực rỡ. "
                "Khí hậu mát mẻ quanh năm, mùa đông có tuyết rơi — hiện tượng hiếm có tại Việt Nam."
            ),
            "tags": ["mountain", "trekking", "adventure", "highland", "nature", "culture", "scenic", "cold"],
            "price_level": 3_500_000,
            "estimated_duration": 48,
        },
        "geo": {"lat": 22.30, "lng": 103.77},
    },
    {
        "location_id": "loc_002",
        "metadata": {
            "name": "Đồng Văn Hà Giang",
            "description": (
                "Cao nguyên đá vôi địa chất toàn cầu UNESCO với những khối đá tai mèo xám xịt trải dài "
                "vô tận, xen lẫn những thửa ruộng hoa tam giác mạch tím mộng mơ mùa thu. "
                "Đèo Mã Pí Lèng — một trong tứ đại đỉnh đèo của Việt Nam — vắt ngang vực Tu Sản sâu thẳm "
                "bên dòng sông Nho Quế xanh ngắt. Chợ phiên Đồng Văn với người dân tộc xuống núi "
                "trong bộ trang phục truyền thống. Thiên đường của những tay phượt xe máy yêu cung đường hiểm trở."
            ),
            "tags": ["mountain", "adventure", "motorbiking", "scenic", "remote", "culture", "history", "photography"],
            "price_level": 3_000_000,
            "estimated_duration": 72,
        },
        "geo": {"lat": 23.23, "lng": 105.25},
    },
    {
        "location_id": "loc_003",
        "metadata": {
            "name": "Mẫu Sơn Lạng Sơn",
            "description": (
                "Đỉnh núi cao 1.541m ở vùng Đông Bắc — một trong số ít nơi ở Việt Nam có tuyết rơi "
                "vào mùa đông tháng 12 đến tháng 2, tạo ra cảnh sắc trắng xóa hiếm thấy ở xứ nhiệt đới. "
                "Mây mù bao phủ gần như quanh năm tạo không khí huyền bí và mát mẻ. "
                "Rừng thông bạt ngàn, suối nguồn trong vắt, rượu Mẫu Sơn từ thảo dược núi rừng nổi tiếng. "
                "Điểm đến độc đáo cho những ai muốn ngắm tuyết mà không cần ra nước ngoài."
            ),
            "tags": ["mountain", "cold", "snow", "nature", "scenic", "unique", "highland", "peaceful"],
            "price_level": 1_000_000,
            "estimated_duration": 24,
        },
        "geo": {"lat": 21.85, "lng": 106.91},
    },

    # ── NORTHEAST / NORTH ─────────────────────────────────────
    {
        "location_id": "loc_004",
        "metadata": {
            "name": "Vịnh Hạ Long",
            "description": (
                "Di sản thiên nhiên thế giới UNESCO với hơn 1.600 hòn đảo đá vôi nhô lên từ mặt vịnh "
                "xanh ngọc bích trong ánh bình minh sương khói huyền ảo. "
                "Trải nghiệm du thuyền qua đêm, chèo kayak vào những hang động ẩn sâu trong lòng núi đá, "
                "tắm biển tại những bãi cát nhỏ hoang sơ. "
                "Hang Sửng Sốt và Hang Đầu Gỗ với nhũ đá muôn hình thù kỳ diệu. "
                "Hải sản tươi sống được đánh bắt ngay trên vịnh."
            ),
            "tags": ["sea", "cruise", "nature", "cave", "adventure", "scenic", "boat", "seafood"],
            "price_level": 5_000_000,
            "estimated_duration": 48,
        },
        "geo": {"lat": 20.91, "lng": 107.18},
    },
    {
        "location_id": "loc_005",
        "metadata": {
            "name": "Thác Bản Giốc",
            "description": (
                "Thác nước lớn nhất Đông Nam Á nằm trên biên giới Việt–Trung tại Cao Bằng, "
                "đổ xuống từ độ cao 30m thành ba tầng thác trắng xóa giữa núi rừng xanh thẳm. "
                "Mùa nước lũ tháng 8–9 hùng vĩ nhất, bụi nước mù mịt cả một vùng. "
                "Ngồi bè mảng trôi sát chân thác nghe tiếng gầm của nước là trải nghiệm không thể quên. "
                "Động Ngườm Ngao gần đó với nhũ đá kỳ vĩ và làng Trùng Khánh yên bình."
            ),
            "tags": ["nature", "waterfall", "scenic", "adventure", "remote", "photography"],
            "price_level": 2_000_000,
            "estimated_duration": 24,
        },
        "geo": {"lat": 22.85, "lng": 106.72},
    },

    # ── NORTH CENTRAL ─────────────────────────────────────────
    {
        "location_id": "loc_006",
        "metadata": {
            "name": "Tràng An Ninh Bình",
            "description": (
                "Di sản thế giới kép UNESCO — vùng đất ngập nước với hệ thống sông suối len lỏi qua "
                "hàng trăm hang động giữa rừng núi đá vôi nguyên sinh. "
                "Ngồi thuyền nan do người dân chèo bằng chân, luồn qua hang tối để ra ánh sáng rực rỡ phía bên kia. "
                "Cố đô Hoa Lư — kinh đô đầu tiên của quốc gia phong kiến Việt Nam — nằm cách đó vài kilômét. "
                "Núi Mua với 500 bậc thang nhìn toàn cảnh Tràng An tuyệt đẹp. Yên bình, không ồn ào."
            ),
            "tags": ["nature", "quiet", "peaceful", "boat", "heritage", "scenic", "cave", "history"],
            "price_level": 1_800_000,
            "estimated_duration": 24,
        },
        "geo": {"lat": 20.25, "lng": 105.91},
    },
    {
        "location_id": "loc_007",
        "metadata": {
            "name": "Phong Nha - Kẻ Bàng",
            "description": (
                "Vườn quốc gia di sản thiên nhiên thế giới UNESCO chứa hệ thống hang động lớn nhất thế giới "
                "— hang Sơn Đoòng dài hơn 9km với rừng và sông ngầm bên trong lòng núi. "
                "Hang Phong Nha tham quan bằng thuyền trên dòng sông ngầm huyền bí. "
                "Rừng nguyên sinh bao phủ 85% diện tích với nhiều loài động thực vật quý hiếm. "
                "Zipline xuyên rừng và tắm suối Moọc trong vắt là những hoạt động không thể bỏ lỡ."
            ),
            "tags": ["nature", "cave", "adventure", "eco", "trekking", "scenic", "wildlife"],
            "price_level": 2_500_000,
            "estimated_duration": 48,
        },
        "geo": {"lat": 17.48, "lng": 106.27},
    },

    # ── CENTRAL ───────────────────────────────────────────────
    {
        "location_id": "loc_008",
        "metadata": {
            "name": "Đại Nội Huế",
            "description": (
                "Hoàng thành cố đô triều Nguyễn — triều đại phong kiến cuối cùng của Việt Nam — "
                "với hệ thống cung điện, lầu gác, thành quách hoành tráng trên diện tích 520 ha. "
                "Ẩm thực cung đình Huế tinh tế chỉ dành cho vua chúa xưa. "
                "Nhã nhạc cung đình UNESCO vang lên trên những chuyến thuyền rồng dạo sông Hương đêm khuya. "
                "Lăng tẩm các vua Khải Định, Minh Mạng, Tự Đức uy nghiêm giữa rừng thông xanh."
            ),
            "tags": ["history", "culture", "heritage", "architecture", "food", "quiet", "royal"],
            "price_level": 1_200_000,
            "estimated_duration": 36,
        },
        "geo": {"lat": 16.46, "lng": 107.57},
    },
    {
        "location_id": "loc_009",
        "metadata": {
            "name": "Phố Cổ Hội An",
            "description": (
                "Thương cảng cổ thịnh vượng từ thế kỷ 15 được UNESCO công nhận di sản thế giới — "
                "những ngôi nhà phố Hoa-Việt-Nhật sơn vàng nghệ với đèn lồng đủ màu lung linh "
                "phản chiếu xuống dòng sông Hoài mỗi tối rằm thả đèn. "
                "Tiệm may áo dài, áo vest chỉ trong 24 giờ. Cao lầu, mì Quảng, bánh mì Phượng đặc trưng. "
                "Lý tưởng cho cặp đôi, nhiếp ảnh và yêu văn hóa bản địa."
            ),
            "tags": ["culture", "heritage", "food", "romantic", "photography", "history", "shopping", "beach"],
            "price_level": 2_000_000,
            "estimated_duration": 36,
        },
        "geo": {"lat": 15.88, "lng": 108.33},
    },
    {
        "location_id": "loc_010",
        "metadata": {
            "name": "Bà Nà Hills Đà Nẵng",
            "description": (
                "Khu du lịch trên đỉnh núi Chúa cao 1.487m với cáp treo đạt nhiều kỷ lục Guinness. "
                "Cầu Vàng với hai bàn tay đá khổng lồ đỡ lấy nhịp cầu — biểu tượng du lịch Việt Nam. "
                "Làng Pháp cổ kính với kiến trúc Gothic và vườn hoa rực rỡ. "
                "Sun World Fantasy Park với hàng chục trò chơi giải trí. "
                "Nhiệt độ mát hơn đồng bằng 5–8°C, mây mù bao phủ tạo cảnh thành phố trên mây."
            ),
            "tags": ["entertainment", "photography", "fun", "scenic", "family", "amusement", "cool"],
            "price_level": 4_500_000,
            "estimated_duration": 12,
        },
        "geo": {"lat": 15.99, "lng": 107.98},
    },

    # ── CENTRAL HIGHLANDS ─────────────────────────────────────
    {
        "location_id": "loc_011",
        "metadata": {
            "name": "Thung Lũng Tình Yêu Đà Lạt",
            "description": (
                "Thành phố ngàn hoa nằm trên cao nguyên 1.500m với khí hậu ôn đới mát mẻ quanh năm. "
                "Thung Lũng Tình Yêu bao phủ hoa dã quỳ vàng rực mỗi tháng 11, "
                "hồ Than Thở mờ sương buổi sáng, vườn hoa thành phố với hoa hồng và hoa cẩm tú cầu đủ màu. "
                "Cà phê Đà Lạt nổi tiếng cả nước, dâu tây ngọt lịm. "
                "Lý tưởng cho cặp đôi, chụp ảnh và thoát khỏi cái nóng oi ả đồng bằng."
            ),
            "tags": ["romantic", "flower", "photography", "cool", "relax", "couple", "nature", "highland"],
            "price_level": 1_500_000,
            "estimated_duration": 36,
        },
        "geo": {"lat": 11.97, "lng": 108.45},
    },
    {
        "location_id": "loc_012",
        "metadata": {
            "name": "Đỉnh Langbiang Đà Lạt",
            "description": (
                "Ngọn núi linh thiêng cao 2.169m của người Lạch bản địa, đặt tên theo truyền thuyết "
                "tình yêu bi thương giữa chàng K'Lang và nàng Hơ Biang. "
                "Từ đỉnh núi nhìn xuống toàn bộ Đà Lạt ẩn trong sương trắng và rừng thông bạt ngàn. "
                "Leo bộ qua rừng thông nguyên sinh hoặc đi xe jeep địa hình lên đỉnh. "
                "Mùa hoa dã quỳ tháng 11, sườn núi vàng rực. Văn hóa cồng chiêng Tây Nguyên dưới chân núi."
            ),
            "tags": ["mountain", "nature", "highland", "trekking", "scenic", "culture", "photography", "cool"],
            "price_level": 800_000,
            "estimated_duration": 12,
        },
        "geo": {"lat": 12.04, "lng": 108.42},
    },

    # ── SOUTH CENTRAL COAST ───────────────────────────────────
    {
        "location_id": "loc_013",
        "metadata": {
            "name": "Vịnh Nha Trang",
            "description": (
                "Vịnh biển đẹp nhất Việt Nam với nước biển xanh trong, cát trắng mịn và quần thể đảo "
                "lý tưởng cho lặn ngắm san hô tại Hòn Mun — khu bảo tồn biển phong phú nhất cả nước. "
                "Tháp Chăm Po Nagar nghìn năm tuổi bên bờ sông Cái. "
                "Khu tắm bùn khoáng nóng thư giãn toàn thân. "
                "Chợ đêm hải sản Nha Trang nhộn nhịp với tôm hùm, mực, ghẹ tươi sống."
            ),
            "tags": ["beach", "sea", "diving", "family", "entertainment", "seafood", "resort", "island"],
            "price_level": 3_000_000,
            "estimated_duration": 48,
        },
        "geo": {"lat": 12.21, "lng": 109.24},
    },
    {
        "location_id": "loc_014",
        "metadata": {
            "name": "Mũi Né Phan Thiết",
            "description": (
                "Thiên đường của những đồi cát đỏ và cát trắng kỳ lạ — hai hệ sinh thái hoàn toàn "
                "trái ngược tồn tại song song chỉ cách nhau vài kilômét. "
                "Mỗi buổi sáng sớm, mặt trời mọc nhuộm đỏ toàn bộ đồi cát là cảnh tượng khó tìm thấy ở đâu khác. "
                "Thiên đường của môn kitesurfing nhờ gió mạnh ổn định quanh năm. "
                "Hải sản tươi và nước mắm Phan Thiết nổi tiếng."
            ),
            "tags": ["beach", "nature", "photography", "adventure", "kitesurfing", "sand-dunes", "scenic"],
            "price_level": 2_200_000,
            "estimated_duration": 36,
        },
        "geo": {"lat": 10.94, "lng": 108.30},
    },

    # ── ISLANDS ───────────────────────────────────────────────
    {
        "location_id": "loc_015",
        "metadata": {
            "name": "Bãi Sao Phú Quốc",
            "description": (
                "Hòn đảo ngọc ở vùng biển Tây Nam với bãi Bãi Sao được bầu chọn là bãi biển đẹp nhất "
                "Đông Nam Á — cát trắng mịn như nhung, nước biển xanh ngọc trong đến thấy đáy, sóng êm ả. "
                "Lặn ngắm san hô tại Hòn Thơm, tham quan nhà thùng nước mắm Phú Quốc, Safari Phú Quốc. "
                "Cáp treo Hòn Thơm vượt biển dài nhất thế giới. "
                "Chợ đêm Dinh Cậu với hải sản và ẩm thực miền Nam phong phú."
            ),
            "tags": ["beach", "island", "resort", "relax", "snorkeling", "tropical", "luxury", "seafood"],
            "price_level": 4_000_000,
            "estimated_duration": 48,
        },
        "geo": {"lat": 10.06, "lng": 104.03},
    },
    {
        "location_id": "loc_016",
        "metadata": {
            "name": "Côn Đảo",
            "description": (
                "Quần đảo hoang sơ cách TP.HCM 230km, thiên nhiên còn gần như nguyên vẹn với vườn quốc gia "
                "bảo tồn rùa biển — mỗi mùa hè, hàng nghìn rùa mẹ lên bãi đẻ trứng là cảnh tượng hiếm có. "
                "Nước biển trong vắt nhất Việt Nam với tầm nhìn dưới nước lên đến 20m, san hô còn nguyên vẹn. "
                "Nghĩa địa Hàng Dương — điểm thăm viếng lịch sử xúc động. "
                "Ít khách, không ồn ào, thích hợp cho ai muốn tìm sự yên tĩnh giữa thiên nhiên hoang dã."
            ),
            "tags": ["beach", "nature", "history", "diving", "wildlife", "peaceful", "remote", "eco"],
            "price_level": 6_000_000,
            "estimated_duration": 72,
        },
        "geo": {"lat": 8.68, "lng": 106.60},
    },
    {
        "location_id": "loc_017",
        "metadata": {
            "name": "Đảo Lý Sơn",
            "description": (
                "Hòn đảo núi lửa giữa biển Quảng Ngãi — 'Vương quốc tỏi' với những cánh đồng tỏi xanh mướt "
                "phủ trên nền đất đen núi lửa màu mỡ. Miệng núi lửa Giếng Tiền đã tắt từ hàng triệu năm "
                "trước giờ là đầm nước ngọt trong lòng đảo. "
                "Nước biển xanh trong, san hô phong phú phù hợp lặn ngắm. "
                "Ít du khách, không khí yên bình và gần gũi với người dân ngư nghiệp bản địa."
            ),
            "tags": ["beach", "island", "local", "diving", "nature", "peaceful", "authentic", "volcanic"],
            "price_level": 2_500_000,
            "estimated_duration": 36,
        },
        "geo": {"lat": 15.38, "lng": 109.11},
    },

    # ── SOUTH ─────────────────────────────────────────────────
    {
        "location_id": "loc_018",
        "metadata": {
            "name": "Bãi Sau Vũng Tàu",
            "description": (
                "Bãi biển gần TP.HCM nhất, chỉ 2 giờ xe — điểm xả hơi cuối tuần lý tưởng cho người Sài Gòn. "
                "Bãi Sau dài 8km với sóng vừa phải phù hợp cho tắm biển và thể thao nước. "
                "Hải sản tươi sống giá rẻ — cua, ghẹ, nghêu, ốc. "
                "Tượng Chúa Kitô trên đỉnh núi Nhỏ nhìn ra toàn bộ vịnh. "
                "Không khí biển tươi mát, thích hợp cho gia đình và chuyến đi ngắn ngày."
            ),
            "tags": ["beach", "family", "short-trip", "seafood", "vibrant", "weekend", "fun"],
            "price_level": 1_500_000,
            "estimated_duration": 24,
        },
        "geo": {"lat": 10.34, "lng": 107.08},
    },
    {
        "location_id": "loc_019",
        "metadata": {
            "name": "Chợ Nổi Cái Răng Cần Thơ",
            "description": (
                "Trái tim văn hóa sông nước Đồng bằng sông Cửu Long — chợ họp lúc 4–5 giờ sáng trên sông "
                "với hàng trăm ghe thuyền chất đầy nông sản trái cây miền Nam. "
                "Mỗi thuyền treo cây sào với hàng hóa bày trên ngọn làm biển hiệu — 'bẹo hàng' độc đáo "
                "chỉ có ở miền Tây. Bánh cống, bún mắm, lẩu mắm — ẩm thực đặc trưng Nam Bộ. "
                "Lý tưởng cho những ai muốn khám phá văn hóa sông nước đích thực."
            ),
            "tags": ["culture", "river", "food", "local", "boat", "authentic", "morning", "market"],
            "price_level": 700_000,
            "estimated_duration": 12,
        },
        "geo": {"lat": 9.99, "lng": 105.74},
    },
    {
        "location_id": "loc_020",
        "metadata": {
            "name": "Làng Chài Mũi Né",
            "description": (
                "Làng đánh cá truyền thống tồn tại hơn 500 năm ngay cạnh khu resort hiện đại của Mũi Né — "
                "sự đối lập kỳ lạ giữa cuộc sống ngư dân bình dị và resort 5 sao. "
                "Mỗi sáng sớm 4–6 giờ, ghe thuyền đánh cá trở về bến với đầy ắp cá, mực, tôm — "
                "chợ cá bốc mùi tanh đặc trưng biển nhưng đầy màu sắc và sống động. "
                "Nước mắm Phan Thiết ủ theo phương pháp truyền thống. Trải nghiệm văn hóa đánh bắt biển đích thực."
            ),
            "tags": ["food", "culture", "local", "authentic", "fishing", "seafood", "morning", "traditional"],
            "price_level": 500_000,
            "estimated_duration": 12,
        },
        "geo": {"lat": 10.94, "lng": 108.29},
    },
]