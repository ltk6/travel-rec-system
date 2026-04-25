"""
seed_data.py
============
Dữ liệu thô 20 địa điểm trên toàn Việt Nam.
- Description đã được viết dài và giàu ngữ nghĩa để N1 sinh Vector chuẩn.
- Tags bao gồm:
  + [N1_TAG]: Các tag đã có sẵn trong file maps/tags.py của N1.
  + [New_TAG]: Các tag mới tự thêm vào (đã được note lại ở cuối file để gửi N1).
"""

LOCATIONS = [

    # ── NORTHWEST ─────────────────────────────────────────────
    {
        "location_id": "loc_001",
        "metadata": {
            "name": "Fansipan Sapa",
            "description": (
                "Đỉnh núi cao nhất Đông Dương nằm giữa biển mây trắng bồng bềnh và thảm thực vật rừng nguyên sinh hùng vĩ của vùng Tây Bắc. "
                "Du khách có thể lựa chọn leo bộ qua những cung đường trekking hiểm trở vắt kiệt sức lực để đổi lấy niềm tự hào, hoặc ngồi cáp treo vượt thung lũng Mường Hoa tuyệt đẹp để chạm tay vào nóc nhà Đông Dương ở độ cao 3.143m. "
                "Bao quanh thị trấn là những thửa ruộng bậc thang vàng óng ả vào mùa lúa chín, cùng các bản làng của người H'Mông, người Dao đỏ với trang phục thổ cẩm thêu tay sặc sỡ. "
                "Thưởng thức nồi thắng cố nóng hổi, thịt lợn bản quay hay nhâm nhi ly rượu táo mèo trong cái lạnh cắt da cắt thịt. "
                "Khí hậu quanh năm ôn đới mát mẻ, đặc biệt vào những ngày đông tháng 12 có thể xuất hiện băng giá và tuyết rơi — một trải nghiệm săn tuyết vô cùng kỳ thú và hiếm có tại Việt Nam."
            ),
            "tags": [
                "mountain", "trekking", "adventure", "highland", "nature", "culture", "scenic", "cold", "snow", "ethnic minority culture", # N1 Tags
                "cable-car", "cloud-hunting", "terraced-fields", "local-specialty", "winter-trip" # New Tags
            ],
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
                "Cao nguyên đá vôi địa chất toàn cầu UNESCO mang vẻ đẹp phong trần, gai góc với những khối đá tai mèo xám xịt nhô lên sắc lẹm trải dài đến tận chân trời. "
                "Sự cằn cỗi ấy lại được xoa dịu bởi vẻ đẹp mộng mơ của những thung lũng hoa tam giác mạch hồng tím nở rộ mỗi độ thu về. "
                "Trải nghiệm phượt xe máy đầy kích thích khi vặn ga vượt qua Đèo Mã Pí Lèng — một trong tứ đại đỉnh đèo hiểm trở nhất Việt Nam — nhìn xuống dòng sông Nho Quế xanh ngắt như dải lụa ngọc bích lọt thỏm dưới vực Tu Sản sâu thẳm. "
                "Đừng bỏ lỡ Dinh thự vua Mèo trầm mặc hay hòa mình vào chợ phiên Đồng Văn nhộn nhịp, nơi người dân tộc ríu rít xuống núi trong những bộ váy xòe rực rỡ để trao đổi nậm rượu ngô và bát thắng dền nóng hổi. "
                "Đây là vùng đất hứa của những đôi chân cuồng đi, đam mê nhiếp ảnh và khao khát tự do."
            ),
            "tags": [
                "mountain", "adventure", "motorbiking", "scenic", "remote", "culture", "history", "photography", "vietnamese culture", # N1 Tags
                "geopark", "canyon", "winding-pass", "flower-season", "backpacking", "indigenous" # New Tags
            ],
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
                "Đỉnh núi thiêng tĩnh lặng cao 1.541m vươn mình giữa vùng Đông Bắc, nơi giao thoa của đất trời và mây gió. "
                "Đây là một trong số ít những điểm đến ở Việt Nam mà bạn có thể thực sự chạm tay vào bông tuyết trắng xóa và băng giá phủ kín những cành thông già vào những đợt rét đậm từ tháng 12 đến tháng 2. "
                "Dù không có tuyết, Mẫu Sơn vẫn quyến rũ du khách bằng bầu không khí huyền bí, mây mù bao phủ quanh năm cùng những phế tích biệt thự Pháp cổ kính rêu phong nhuốm màu thời gian. "
                "Du khách đến đây để tìm kiếm sự bình yên, đi dạo trong rừng thông bạt ngàn, tắm lá thuốc người Dao đỏ và nhâm nhi chén rượu Mẫu Sơn trứ danh nấu từ con suối tinh khiết róc rách chảy quanh ngọn núi."
            ),
            "tags": [
                "mountain", "cold", "snow", "nature", "scenic", "unique", "highland", "peaceful", "relaxation trip", # N1 Tags
                "french-villas", "ruins", "foggy", "pine-forest", "local-wine", "mysterious" # New Tags
            ],
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
                "Một kiệt tác vĩ đại của thiên nhiên, Di sản thiên nhiên thế giới UNESCO nơi hơn 1.600 hòn đảo đá vôi khổng lồ mọc lên uy nghi từ mặt nước xanh ngọc bích tĩnh lặng. "
                "Khung cảnh bình minh sương khói hay hoàng hôn nhuộm vàng mặt vịnh tạo nên một bức tranh thủy mặc vô giá. "
                "Trải nghiệm tuyệt vời nhất là thuê một chiếc du thuyền 5 sao ngủ qua đêm trên vịnh, mở cửa sổ phòng đón gió biển và thức dậy giữa bao la sóng nước. "
                "Du khách có thể tự tay chèo thuyền kayak luồn lách qua những hang động bí ẩn, leo núi Titop để ngắm toàn cảnh, hay khám phá Hang Sửng Sốt và Hang Đầu Gỗ lộng lẫy với hệ thống nhũ đá được kiến tạo hàng triệu năm. "
                "Hải sản ở đây vô cùng phong phú, từ mực nhảy, bề bề cho đến hàu nướng mỡ hành, luôn tươi rói vì được đánh bắt trực tiếp từ các làng chài nổi."
            ),
            "tags": [
                "sea", "cruise", "nature", "cave", "adventure", "scenic", "boat cruise", "seafood", "island escape", "luxury travel", # N1 Tags
                "unesco-heritage", "limestone-karst", "sunset-view", "geology", "iconic-landmark" # New Tags
            ],
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
                "Thác nước kỳ vĩ và lớn nhất Đông Nam Á, nằm oai hùng tựa dải lụa trắng vắt ngang đường biên giới Việt – Trung tại tỉnh Cao Bằng. "
                "Nước đổ ầm ầm từ độ cao 30m, đập vào các tầng đá vôi tạo thành ba tầng thác tung bọt trắng xóa, làm mờ ảo cả một khoảng không gian giữa rừng núi xanh thẳm hoang sơ. "
                "Vào mùa mưa lũ (tháng 8 - tháng 9), con thác cuộn trào mạnh mẽ, khoe trọn vẻ đẹp dữ dội nhất. "
                "Du khách có thể thuê bè mảng của người dân địa phương trôi dạt sát ngay dưới chân thác để cảm nhận bụi nước mát lạnh bắn vào mặt và nghe tiếng gầm gào của thiên nhiên. "
                "Kết hợp chuyến đi với việc khám phá Động Ngườm Ngao lấp lánh thạch nhũ và ghé qua những vạt lúa nếp chín vàng cùng vườn hạt dẻ nức tiếng của vùng quê Trùng Khánh thanh bình."
            ),
            "tags": [
                "nature", "waterfall scenic", "scenic", "adventure", "remote", "photography", "cave exploration", # N1 Tags
                "border", "majestic", "rafting", "harvest-season", "rural", "spectacular" # New Tags
            ],
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
                "Được ví như 'Vịnh Hạ Long trên cạn', Tràng An là Di sản thế giới kép UNESCO kết hợp hoàn hảo giữa vẻ đẹp địa chất núi đá vôi nguyên sinh và dấu ấn lịch sử nhân loại. "
                "Hệ thống đầm lầy, sông suối trong vắt nhìn thấu tận rong rêu len lỏi qua hàng trăm hang động tự nhiên mát lạnh. "
                "Hành trình tuyệt nhất là ngồi trên chiếc thuyền nan lững lờ trôi, do những người dân địa phương chèo bằng đôi chân điêu luyện, luồn cúi qua những vòm hang tối om để vỡ òa khi ra đến ánh sáng chói lọi của thung lũng hoa súng bát ngát bên kia núi. "
                "Ngay gần đó là Cố đô Hoa Lư đẫm màu lịch sử — kinh đô đầu tiên của Việt Nam. Đừng quên thử thách đôi chân với 500 bậc đá leo lên Hang Múa để thu trọn toàn cảnh sông Ngô Đồng uốn lượn như dải lụa vàng vào tầm mắt. Một điểm đến cực kỳ yên bình, thanh lọc tâm hồn."
            ),
            "tags": [
                "nature", "quiet", "peaceful", "boat", "heritage", "scenic", "cave", "history", "eco", "river", "cultural trip", # N1 Tags
                "limestone", "temples", "healing", "lotus" # New Tags
            ],
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
                "Vương quốc hang động thiêng liêng và bí ẩn, Vườn quốc gia Di sản thiên nhiên thế giới UNESCO này chứa đựng những kiến tạo địa chất ngoạn mục nhất hành tinh. "
                "Nơi đây sở hữu Hang Sơn Đoòng — hang động lớn nhất thế giới, rộng đến mức chứa được cả một khu rừng nguyên sinh, hệ thống thời tiết riêng và dòng sông ngầm cuồn cuộn bên trong. "
                "Đối với những chuyến đi vừa sức hơn, du khách có thể ngồi thuyền máy dọc dòng sông Son xanh ngắt đi vào Hang Phong Nha huyền ảo, hay thám hiểm Động Thiên Đường lộng lẫy thạch nhũ. "
                "Các hoạt động thể thao mạo hiểm ngoài trời cực kỳ bùng nổ: tắm bùn trong Hang Tối, đu zipline xuyên rừng, chèo kayak và đắm mình trong làn nước lạnh buốt tinh khiết của suối Nước Moọc. "
                "Bao bọc xung quanh là 85% diện tích rừng nguyên sinh rậm rạp bảo tồn vô số động thực vật hoang dã quý hiếm."
            ),
            "tags": [
                "nature", "cave exploration", "adventure travel", "eco", "trekking", "scenic", "wildlife", "national park", "zip line", "kayaking", # N1 Tags
                "mud-bath", "underground-river", "extreme-sports", "unesco" # New Tags
            ],
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
                "Bước qua cánh cổng Ngọ Môn là bạn đã xuyên không về quá khứ, lạc vào Hoàng thành của cố đô triều Nguyễn — triều đại phong kiến cuối cùng trong lịch sử Việt Nam. "
                "Quần thể di tích khổng lồ trải rộng trên 520 ha với hàng trăm cung điện, lầu gác, miếu mạo, thành quách sơn son thiếp vàng oai nghiêm, tĩnh mặc in bóng xuống dòng nước rêu phong của các hồ thái dịch. "
                "Sự tinh hoa của vùng đất này nằm ở nhịp sống chậm rãi và nền ẩm thực cung đình Huế tỉ mỉ, cầu kỳ mà xưa kia chỉ dành riêng cho vua chúa thưởng thức. "
                "Đêm xuống, hãy thuê một chiếc thuyền rồng thả trôi trên dòng sông Hương thơ mộng, thả đèn hoa đăng và lắng nghe những điệu Nhã nhạc cung đình (Di sản phi vật thể UNESCO) day dứt lòng người. "
                "Cách đó không xa là hệ thống lăng tẩm các vị vua Khải Định, Minh Mạng, Tự Đức với kiến trúc phong thủy tuyệt mỹ chìm khuất giữa rừng thông xanh bạt ngàn."
            ),
            "tags": [
                "history", "culture", "heritage", "architecture", "food", "quiet", "cultural trip", "vietnamese culture", "boat cruise", # N1 Tags
                "royal", "imperial", "palace", "traditional-music", "slow-life", "temples" # New Tags
            ],
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
                "Từng là một thương cảng sầm uất bậc nhất Đông Nam Á từ thế kỷ 15, Phố cổ Hội An ngày nay là một bảo tàng sống được UNESCO công nhận, nơi thời gian dường như ngưng đọng. "
                "Du khách sẽ đắm chìm trong vẻ đẹp của những dãy nhà phố tường sơn vàng nghệ rực rỡ, mái ngói âm dương phủ rêu, mang đậm nét giao thoa kiến trúc Hoa - Việt - Nhật, tiêu biểu là biểu tượng Chùa Cầu uốn cong tĩnh lặng. "
                "Khi hoàng hôn buông, Hội An hóa thành một giấc mơ lãng mạn khi hàng ngàn chiếc đèn lồng lụa đủ màu sắc được thắp sáng lung linh, hắt bóng xuống dòng sông Hoài êm ả nơi du khách ngồi thuyền thả hoa đăng cầu bình an. "
                "Đây là thiên đường cho tín đồ mua sắm với các tiệm may đo áo dài, suit lấy liền trong 24 giờ, và các xưởng làm đồ da thủ công. "
                "Ẩm thực đường phố vươn tầm thế giới với tô cao lầu dai giòn, mì Quảng đậm đà, nước mót thảo mộc thanh mát và chiếc bánh mì Phượng lừng danh."
            ),
            "tags": [
                "culture", "heritage", "street food", "romantic getaway", "photography", "history", "shopping", "old town", "vietnamese culture", # N1 Tags
                "lanterns", "tailor", "walking-street", "night-view", "nostalgic" # New Tags
            ],
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
                "Được ví như 'Châu Âu thu nhỏ giữa lòng miền Trung', khu du lịch giải trí đỉnh cao này nằm trên đỉnh núi Chúa ở độ cao 1.487m so với mực nước biển. "
                "Hành trình bắt đầu bằng hệ thống cáp treo đạt nhiều kỷ lục thế giới, lướt qua những tầng mây và tán rừng nguyên sinh rậm rạp. "
                "Bà Nà Hills nổi danh toàn cầu với Cầu Vàng (Golden Bridge) — dải lụa vàng lấp lánh được nâng đỡ bởi hai bàn tay đá rêu phong khổng lồ vươn ra từ sườn núi. "
                "Bên trên là Làng Pháp cổ kính với những tòa lâu đài kiến trúc Gothic, nhà thờ, hầm rượu vang Debay trăm tuổi và những khu vườn hoa Le Jardin D'Amour rực rỡ khoe sắc quanh năm. "
                "Không chỉ có cảnh quan, nơi đây còn sở hữu Sun World Fantasy Park rộng lớn với hàng trăm trò chơi mạo hiểm và cảm giác mạnh. Khí hậu biến chuyển 4 mùa trong một ngày, luôn mát mẻ hơn đồng bằng từ 5–8°C."
            ),
            "tags": [
                "fun", "scenic", "family trip", "cool", "mountain", "photography", "architecture", # N1 Tags
                "amusement-park", "resort", "cable-car", "european-architecture", "landmark", "theme-park" # New Tags
            ],
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
                "Nằm vắt vẻo trên cao nguyên Lâm Viên ở độ cao 1.500m, Đà Lạt mang khí hậu ôn đới se lạnh mờ sương quanh năm, là chốn 'trốn nóng' hoàn hảo của người dân phía Nam. "
                "Thung Lũng Tình Yêu là trái tim lãng mạn của thành phố ngàn hoa, nơi những đồi thông trập trùng ôm lấy hồ Đa Thiện phẳng lặng. "
                "Đến đây vào tháng 11, du khách sẽ choáng ngợp trước những vạt hoa dã quỳ hoang dại nở vàng rực rỡ khắp các triền đồi, đan xen cùng vườn cẩm tú cầu, hoa hồng đỏ thắm và đồi cỏ hồng đẹp như cổ tích. "
                "Trải nghiệm đạp vịt trên mặt hồ, đi xe ngựa dạo quanh thung lũng, hay đơn giản là ngồi nhâm nhi ly cà phê nóng hổi, ăn trái dâu tây ngọt lịm vừa hái tại vườn. "
                "Một điểm đến mang đậm hơi thở bình yên, sự lãng mạn hoài niệm, cực kỳ lý tưởng để các cặp đôi hâm nóng tình cảm hoặc để những tâm hồn cô đơn tìm chốn chữa lành."
            ),
            "tags": [
                "romantic getaway", "photography", "cool", "relax", "nature", "highland", "peaceful", "lake", "relaxation trip", # N1 Tags
                "flower", "couple", "garden", "pine-tree", "coffee", "vintage", "healing", "honeymoon" # New Tags
            ],
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
                "Được mệnh danh là 'Nóc nhà của Đà Lạt', ngọn núi linh thiêng vươn cao 2.169m này là biểu tượng gắn liền với truyền thuyết tình yêu bi thương nhưng thủy chung của chàng K'Lang và nàng Hơ Biang người dân tộc bản địa. "
                "Để chinh phục đỉnh núi, du khách có thể chọn thuê xe jeep chuyên dụng xé gió lao qua những con dốc ngoằn ngoèo, hoặc tự thử thách bản thân bằng những cung đường trekking đi bộ xuyên qua thảm rừng thông nguyên sinh bạt ngàn mát rượi. "
                "Từ đỉnh Rada phóng tầm mắt xuống, toàn cảnh thành phố Đà Lạt, dòng Suối Vàng uốn lượn và những thung lũng sương mù hiện ra như một sa bàn tuyệt mỹ. "
                "Khi ánh chiều buông, hãy xuống chân núi để cùng hòa mình vào không gian văn hóa cồng chiêng Tây Nguyên, uống rượu cần say sưa và nhảy múa quanh đống lửa bập bùng cùng các nam thanh nữ tú người Lạch."
            ),
            "tags": [
                "mountain trek", "nature", "highland", "trekking", "scenic", "culture", "photography", "cool", "adventure travel", "ethnic minority culture", # N1 Tags
                "viewpoint", "jeep-tour", "camping", "cloud-hunting", "sunset" # New Tags
            ],
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
                "Được xướng tên trong câu lạc bộ những vịnh biển đẹp nhất thế giới, Nha Trang là bản hòa ca rực rỡ của biển xanh ngắt, cát trắng mịn màng và ánh nắng nhiệt đới tràn trề rực rỡ. "
                "Sở hữu quần thể hàng chục hòn đảo lớn nhỏ, đây là thủ phủ của các môn thể thao dưới nước. Đặc biệt tại khu bảo tồn biển Hòn Mun, du khách có thể lặn bình dưỡng khí (scuba diving) hay đi bộ dưới đáy biển (seawalk) để tận mắt chiêm ngưỡng rạn san hô lộng lẫy và đàn cá nhiệt đới đủ màu bơi lội tung tăng. "
                "Thành phố còn cung cấp trải nghiệm nghỉ dưỡng độc đáo với dịch vụ tắm bùn khoáng nóng và luân xa thảo dược giúp thư giãn mọi giác quan. "
                "Những ai yêu thích văn hóa có thể ghé thăm Tháp Bà Ponagar nghìn năm tuổi xây bằng gạch nung đỏ rực của người Chăm cổ ven sông Cái. "
                "Và khi đêm về, chợ đêm Nha Trang hay các nhà hàng hải sản ven biển sẽ đánh gục mọi thực khách bằng hàng chục loại tôm hùm, cua ghẹ, ốc biển tươi sống giãy đành đạch với mức giá vô cùng hợp lý."
            ),
            "tags": [
                "beach paradise", "sea", "diving", "family trip", "seafood", "island", "snorkeling", "luxury travel", "nightlife", "history", "sun", # N1 Tags
                "entertainment", "resort", "water-sports", "mud-bath", "swimming", "vacation" # New Tags
            ],
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
                "Thủ phủ resort của Việt Nam mang trong mình một hiện tượng địa lý vô cùng kỳ thú: sự giao thoa hoang dã giữa biển khơi rì rào và những 'tiểu sa mạc' cát mênh mông. "
                "Đồi Cát Bay (cát đỏ) và Bàu Trắng (cát trắng) thay đổi hình dáng theo từng đợt gió, biến nơi đây thành thiên đường cho môn trượt cát hay lái xe môtô địa hình (ATV) băng băng qua những triền dốc dốc đứng. Cảnh bình minh nhuộm đỏ rực cả đồi cát là khoảnh khắc 'sống ảo' không thể bỏ lỡ. "
                "Dọc theo bờ biển là Suối Tiên lội bộ êm ái dưới lòng suối cạn đỏ âu và Hẻm núi đất sét sừng sững. "
                "Với lợi thế gió mạnh và con sóng dài ổn định quanh năm, Mũi Né là điểm đến số một châu Á cho giới đam mê lướt ván diều (Kitesurfing). "
                "Sau những giờ vận động đổ mồ hôi, hãy dạo bước vào làng chài Mũi Né nhộn nhịp mùi tôm cá, thưởng thức hải sản tươi nướng mỡ hành nức mũi và mua về những chai nước mắm Phan Thiết nhỉ cá cơm truyền thống đậm đà."
            ),
            "tags": [
                "beach", "nature", "photography", "adventure travel", "scenic", "seafood", "sun", "desert", # N1 Tags
                "kitesurfing", "sand-dunes", "resort", "off-road", "sunrise", "fishing-village", "sports" # New Tags
            ],
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
                "Nằm êm đềm ở phía Nam Đảo Ngọc Phú Quốc, Bãi Sao luôn lọt top những bãi biển hoang sơ và đẹp nhất Đông Nam Á. "
                "Không mang màu cát vàng như biển miền Trung, cát ở Bãi Sao có màu trắng tinh khôi, hạt mịn tơi như lớp kem sữa, trải dài hình vành trăng khuyết bên bờ đại dương xanh lam trong vắt nhìn thấu đáy. "
                "Sóng biển ở đây quanh năm êm ả, mực nước nông rất an toàn cho trẻ nhỏ. Dưới mặt nước là vương quốc của những chú sao biển đỏ rực rỡ nằm rải rác đùa giỡn với sóng. "
                "Rời bãi biển, du khách có thể trải nghiệm tuyến cáp treo vượt biển Hòn Thơm dài nhất thế giới để nhìn ngắm toàn cảnh các hòn đảo từ trên không, hay khám phá công viên bán hoang dã Safari lớn nhất Việt Nam. "
                "Buổi tối, Chợ đêm Dinh Cậu nhộn nhịp sẽ đánh thức vị giác bằng những quầy hải sản nướng thơm lừng, kẹo chỉ sặc sỡ và hồ tiêu xanh mướt đặc sản."
            ),
            "tags": [
                "beach paradise", "island escape", "relax", "snorkeling", "tropical", "luxury travel", "seafood", "nature", "family trip", # N1 Tags
                "resort", "white-sand", "starfish", "cable-car", "swimming", "sunset", "chill" # New Tags
            ],
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
                "Cách TP.HCM khoảng 230km về phía biển Đông, Côn Đảo từng bị gọi là 'địa ngục trần gian' với hệ thống nhà tù Chuồng Cọp khét tiếng, nhưng nay đã vươn mình trở thành một trong những hòn đảo bí ẩn và quyến rũ nhất hành tinh. "
                "Nơi đây là thánh địa của thiên nhiên hoang dã, không có những tòa nhà cao ốc hay khói bụi còi xe. Vườn quốc gia Côn Đảo sở hữu hệ sinh thái rừng - biển nguyên vẹn tuyệt đối. "
                "Đặc biệt, nếu đến vào mùa hè (tháng 4 - tháng 10) tại Hòn Bảy Cạnh, bạn sẽ được chứng kiến cảnh tượng kỳ diệu khi hàng ngàn cá thể rùa biển quý hiếm bò lên bờ đẻ trứng trong đêm. "
                "Nước biển Côn Đảo xanh ngắt một màu lam ngọc, tầm nhìn khi lặn biển lên tới 20m, bao bọc những rạn san hô cổ đại rực rỡ. "
                "Về đêm, hàng ngàn người dân và du khách tĩnh lặng dâng hương tại Nghĩa trang Hàng Dương và mộ nữ anh hùng Võ Thị Sáu — một trải nghiệm tâm linh sâu sắc, trang nghiêm và vô cùng xúc động."
            ),
            "tags": [
                "beach", "nature", "history", "diving", "wildlife", "peaceful", "eco", "snorkeling", "spiritual", "national park", # N1 Tags
                "remote", "turtle", "prison", "untouched", "serene", "island-hopping" # New Tags
            ],
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
                "Nổi lên giữa biển khơi Quảng Ngãi như một kiệt tác địa chất hiếm có, Lý Sơn thực chất là tàn tích của 5 miệng núi lửa đã tắt từ hàng triệu năm trước. "
                "Thiên nhiên khắc nghiệt cộng với lớp đất nham thạch bazan màu mỡ và cát san hô trắng vụn đã tạo nên 'Vương quốc Tỏi' nức tiếng với những cánh đồng tỏi xanh mướt, xếp lớp bậc thang như những bàn cờ khổng lồ trập trùng ven biển. Tỏi Lý Sơn mang vị thơm dịu đặc trưng không nơi nào có được. "
                "Khung cảnh thiên nhiên tráng lệ với vách đá Hang Câu sừng sững, Cổng Tò Vò uốn cong kỳ vĩ trên nền nước biển trong veo đến mức có thể đứng trên bờ nhìn thấy cá bơi dưới đáy. "
                "Du khách đến đây để cắm trại qua đêm trên miệng núi lửa Thới Lới, lặn ngắm san hô bằng thuyền thúng, ăn vặt món gỏi rong biển giòn sần sật và hòa mình vào cuộc sống chân chất, nồng hậu của người ngư dân bám biển."
            ),
            "tags": [
                "beach", "island", "local", "diving", "nature", "peaceful", "authentic", "camping", "scenic", "off the beaten path", "photography", "seafood", "cliff", # N1 Tags
                "volcanic", "geology", "garlic-fields" # New Tags
            ],
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
                "Chỉ cách trung tâm nhộn nhịp của TP.HCM khoảng 2 giờ lái xe, Vũng Tàu luôn là sự lựa chọn số một cho những chuyến xả hơi cuối tuần ngắn ngày của người dân Đông Nam Bộ. "
                "Bãi Sau (Bãi Thùy Vân) là cung đường biển sầm uất và đẹp nhất thành phố, vươn dài 8km với bãi cát rộng, phẳng lì và sóng biển vỗ rì rào vừa đủ mạnh để thỏa mãn đam mê tắm biển, lướt ván nhè nhẹ. "
                "Chạy dọc theo bờ biển là công viên xanh mát, hàng loạt nhà hàng, quán cà phê đón gió lộng. Bạn có thể chinh phục gần 1.000 bậc thang lên đỉnh Núi Nhỏ để chui vào trong cánh tay của bức Tượng Chúa Kitô Vua khổng lồ, phóng tầm mắt ôm trọn toàn cảnh thành phố biển lộng gió. "
                "Về chiều tối, không gì tuyệt hơn việc tụ tập bạn bè đánh chén một chảo lẩu cá đuối chua cay măng chua sực nức mũi, mua hộp bánh bông lan trứng muối thơm lừng và nhâm nhi vài ly bia ngắm biển đêm rực rỡ ánh đèn."
            ),
            "tags": [
                "beach", "family trip", "seafood", "vibrant", "fun", "swimming", "local cuisine", "lively", "nightlife", "city", "coastal", # N1 Tags
                "short-trip", "weekend", "statue", "foodie", "city-break", "coastal-road" # New Tags
            ],
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
                "Linh hồn của vùng Đồng bằng sông Cửu Long, Di sản văn hóa phi vật thể quốc gia, nơi tái hiện sinh động nhất nền văn minh sông nước miệt vườn đã tồn tại hàng trăm năm. "
                "Để kịp phiên chợ, du khách phải thức dậy từ 4–5 giờ sáng, ngồi trên chiếc vỏ lãi xé dòng nước đục phù sa đi vào trung tâm chợ. "
                "Khung cảnh hiện ra là một đô thị trên sông ồn ào và rực rỡ sắc màu, với hàng trăm chiếc ghe thuyền lớn nhỏ đan xen nhau, chở đầy ắp khóm (dứa), xoài, chôm chôm, dưa hấu. "
                "Mỗi chiếc ghe không có biển hiệu, người dân miền Tây dùng cây sào tre dài cắm trước mũi thuyền, treo lủng lẳng món hàng mình bán lên đó — gọi là 'cây bẹo' — một phương thức marketing thô sơ nhưng cực kỳ thông minh. "
                "Cảm giác trôi bồng bềnh trên sông, gọi vớt một tô hủ tiếu gõ nóng hổi bốc khói, nhấp ngụm cà phê vợt ngọt lịm từ một chiếc xuồng len lỏi tới sát mạn thuyền, và nghe câu hò điệu lý thân thương của bà con nông dân là những ký ức không thể nào phai."
            ),
            "tags": [
                "culture", "river", "food", "local", "boat", "authentic", "market", "photography", "traditional", "vietnamese culture", "delta", # N1 Tags
                "morning", "floating", "mekong-delta", "fruits", "bustling", "early-bird" # New Tags
            ],
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
                "Trái ngược hoàn toàn với dãy resort 5 sao xa hoa lộng lẫy cách đó không xa, Làng chài Mũi Né mang một vẻ đẹp trần trụi, nguyên bản và đậm đặc hơi thở của biển cả. "
                "Ngôi làng tĩnh lặng này đã tồn tại hơn 500 năm. Mỗi sớm mai từ 4-6 giờ, bãi biển bừng tỉnh và hóa thành một bức tranh sơn dầu sống động: hàng trăm chiếc thuyền thúng xanh đỏ rực rỡ lấp ló ngoài khơi nối đuôi nhau mang chiến lợi phẩm cập bờ. "
                "Chợ cá họp ngay trên bãi cát ướt sũng, tiếng trả giá râm ran hòa cùng mùi mặn mòi đặc trưng của tôm, cua, cá, mực tươi rói vừa gỡ lưới. "
                "Du khách đến đây không chỉ để mua hải sản với giá gốc rễ, mà còn để lang thang qua các xưởng làm nước mắm truyền thống, những vỉ phơi cá khô mặn chát dưới nắng gắt. "
                "Vào lúc hoàng hôn, khi triều rút, nơi đây trở nên vắng lặng, là bối cảnh hoàn hảo cho những bức ảnh ngược sáng đầy nghệ thuật về những con người cần mẫn bám biển."
            ),
            "tags": [
                "food", "culture", "local", "authentic", "seafood", "traditional", "photography", "market", "coastal", "village", # N1 Tags
                "fishing", "morning", "sunrise", "raw", "coastal-life", "coracles", "fish-sauce" # New Tags
            ],
            "price_level": 500_000,
            "estimated_duration": 12,
        },
        "geo": {"lat": 10.94, "lng": 108.29},
    },
    {
        "location_id": "loc_021",
        "metadata": {
            "name": "Ruộng bậc thang Mù Cang Chải",
            "description": (
                "Nằm chót vót trên những sườn núi dốc đứng của tỉnh Yên Bái, Mù Cang Chải là một kiệt tác kiến trúc nông nghiệp vĩ đại được khắc tạc bởi đôi bàn tay cần mẫn của đồng bào người H'Mông qua hàng trăm năm. "
                "Cứ mỗi độ thu về (tháng 9 đến tháng 10), toàn bộ thung lũng lột xác hóa thành một biển vàng óng ả rực rỡ. Những thửa ruộng bậc thang thoai thoải tầng tầng lớp lớp nối tiếp nhau vươn lên tận mây xanh, nổi bật nhất là Đồi Mâm Xôi và Đồi Móng Ngựa - thánh địa săn ảnh của mọi nhiếp ảnh gia. "
                "Hành trình đến đây đòi hỏi du khách phải vượt qua đèo Khâu Phạ chênh vênh mây phủ. Nếu là người đam mê cảm giác mạnh, trải nghiệm nhảy dù lượn (paragliding) từ đỉnh đèo bay lơ lửng trên thảm lúa chín vàng chắc chắn sẽ khiến bạn choáng ngợp. "
                "Nơi đây không có những resort xa hoa, thay vào đó là trải nghiệm ngủ homestay nhà sàn gỗ mộc mạc, nhâm nhi chén rượu ngô cay nồng, thưởng thức xôi nếp nương dẻo ngọt ăn cùng thịt lợn bản gác bếp trong tiết trời se lạnh đặc trưng của vùng cao Tây Bắc."
            ),
            "tags": [
                "mountain", "nature", "scenic", "photography", "peaceful", "ethnic minority culture", "culture", "backpacking",
                "terraced-fields", "harvest-season", "autumn-trip", "paragliding", "winding-pass", "rustic", "homestay"
            ],
            "price_level": 2000000,
            "estimated_duration": 48,
        },
        "geo": {"lat": 21.84, "lng": 104.08},
    },
    {
        "location_id": "loc_022",
        "metadata": {
            "name": "Đảo Phú Quý Bình Thuận",
            "description": (
                "Nằm trơ trọi giữa muôn trùng sóng nước cách đất liền Phan Thiết hơn 120km, Đảo Phú Quý (hay còn gọi là Cù Lao Thu) đang là viên ngọc thô rực sáng nhất trên bản đồ du lịch giới trẻ hiện nay nhờ giữ được vẻ đẹp hoang sơ, mộc mạc, chưa bị thương mại hóa tàn phá. "
                "Nước biển tại Vịnh Triều Dương trong vắt đến mức nhìn rõ từng rặng san hô và bầy cá nhỏ bơi lội dưới đáy, cực kỳ lý tưởng cho việc chèo SUP và lặn ống thở (snorkeling). "
                "Dấu ấn địa chất độc đáo của đảo thể hiện rõ nhất qua những vách đá đen tuyền sừng sững tạc hình kỳ dị tại núi Cao Cát, hay dốc phượt lộng gió với phông nền là những trụ tuabin điện gió khổng lồ quay chậm rãi dưới nền trời xanh thẳm. "
                "Trải nghiệm tuyệt vời nhất ở Phú Quý là thuê một chiếc xe máy, chạy rong ruổi trên con đường ven biển không bóng người, đón cơn gió mặn chát của đại dương và dừng chân tại làng chài để thưởng thức bò nóng Phú Quý, cua mặt trăng và nhum biển nướng mỡ hành vừa bắt lên bờ với mức giá rẻ đến ngỡ ngàng."
            ),
            "tags": [
                "island escape", "beach", "untouched", "youth", "trendy", "seafood", "nature", "chill", "snorkeling", "scenic",
                "wind-turbine", "motorbiking", "clear-water", "remote", "stand-up-paddle", "cliff"
            ],
            "price_level": 2500000,
            "estimated_duration": 48,
        },
        "geo": {"lat": 10.51, "lng": 108.93},
    },
    {
        "location_id": "loc_023",
        "metadata": {
            "name": "Thị trấn Măng Đen Kon Tum",
            "description": (
                "Được ví von là 'Đà Lạt thứ hai' nhưng Măng Đen (huyện Kon Plông, Kon Tum) lại mang một âm hưởng hoàn toàn khác biệt: trầm mặc hơn, hoang sơ hơn và vắng lặng hơn rất nhiều. Nằm lọt thỏm giữa đại ngàn Tây Nguyên ở độ cao 1.200m, Măng Đen sở hữu khí hậu se lạnh, sương mù lãng đãng bao phủ quanh năm cùng thảm thực vật rừng thông đỏ nguyên sinh rậm rạp. "
                "Tránh xa khỏi sự ồn ào của phố thị, du khách đến đây để tìm kiếm sự 'chữa lành' thực sự. Bạn có thể tản bộ dưới những tán thông reo vi vu, ghé thăm thác Pa Sỹ cuồn cuộn bọt trắng xóa đổ xuống từ vách đá chênh vênh, hay tĩnh tâm viếng thăm tượng Đức Mẹ Măng Đen linh thiêng nằm lẩn khuất giữa rừng già. "
                "Văn hóa cồng chiêng của đồng bào M'Nông, Xê Đăng vẫn được bảo tồn nguyên vẹn tại các buôn làng. Không thể không nhắc đến nền ẩm thực núi rừng gây thương nhớ: gà nướng măng đen da giòn rụm tẩm ướp rễ cây rừng, ăn kèm ống cơm lam dẻo thơm lừng mùi rơm rạ và lẩu cá tầm măng chua nghi ngút khói giữa đêm đông giá buốt."
            ),
            "tags": [
                "highland", "cool", "pine-forest", "peaceful", "slow-life", "nature", "healing", "local cuisine", "off the beaten path",
                "waterfall", "misty", "ethnic minority culture", "acoustic", "camping", "spiritual"
            ],
            "price_level": 1800000,
            "estimated_duration": 36,
        },
        "geo": {"lat": 14.60, "lng": 108.28},
    },
    {
        "location_id": "loc_024",
        "metadata": {
            "name": "Khu dự trữ sinh quyển Cù Lao Chàm",
            "description": (
                "Chỉ cách phố cổ Hội An khoảng 20 phút lướt sóng bằng cano cao tốc, Cù Lao Chàm là một cụm đảo xanh ngọc bích được UNESCO công nhận là Khu dự trữ sinh quyển thế giới. Nơi đây tiên phong trong phong trào du lịch xanh: nói không với rác thải nhựa và bảo vệ nghiêm ngặt môi trường biển. "
                "Du khách sẽ ngay lập tức bị quyến rũ bởi những bãi biển tuyệt đẹp như Bãi Làng, Bãi Ông với dải cát trắng mịn màng và rặng dừa nghiêng mình soi bóng. Bờ biển nông, nước trong vắt tạo điều kiện hoàn hảo cho các tour lặn ngắm san hô (snorkeling) đa sắc màu và đi bộ dưới đáy biển. "
                "Không chỉ có thiên nhiên, hòn đảo này còn lưu giữ những di tích văn hóa Chăm Pa cổ đại như Giếng cổ Chăm hơn 200 năm tuổi không bao giờ cạn nước, và Chùa Hải Tạng rêu phong tĩnh lặng. "
                "Sau một buổi sáng vẫy vùng dưới nước biển mát lạnh, một bữa tiệc hải sản tươi rói với cua đá (đặc sản hiếm có), ốc vú nàng và rau rừng luộc chấm khoai quẹt sẽ là phần thưởng lấp đầy chiếc bụng đói của bất kỳ du khách nào."
            ),
            "tags": [
                "island", "eco", "green-tourism", "snorkeling", "beach", "unesco", "biosphere", "seafood", "sun", "summer-trip",
                "speed-boat", "coral-reef", "heritage", "authentic", "nature"
            ],
            "price_level": 1500000,
            "estimated_duration": 12,
        },
        "geo": {"lat": 15.96, "lng": 108.51},
    },
    {
        "location_id": "loc_025",
        "metadata": {
            "name": "Khu du lịch Núi Bà Đen Tây Ninh",
            "description": (
                "Sừng sững giữa vùng đồng bằng phì nhiêu, Núi Bà Đen cao 986m được mệnh danh là 'Nóc nhà Đông Nam Bộ'. Từ một ngọn núi hoang sơ, nơi đây nay đã chuyển mình trở thành một quần thể du lịch sinh thái và tâm linh quy mô bậc nhất miền Nam. "
                "Hành trình chinh phục đỉnh núi không còn nhọc nhằn nhờ hệ thống cáp treo hiện đại bậc nhất châu Âu, lướt qua những mảng rừng xanh um tùm. Trên đỉnh núi là một không gian ngoạn mục, rực rỡ cờ hoa, nơi quanh năm mây trắng bay vờn sát mặt đất, mang đến trải nghiệm 'săn mây' chẳng kém gì vùng Tây Bắc. "
                "Điểm nhấn kiến trúc vĩ đại nhất chính là bức tượng Phật Bà Tây Bổ Đà Sơn bằng đồng nguyên khối cao nhất châu Á đứng uy nghiêm giữa mây trời, mang lại cảm giác bình yên và thanh tịnh lạ thường. "
                "Vào các dịp lễ hội rằm tháng Giêng, hàng triệu Phật tử từ khắp nơi đổ về chùa Bà (nằm ở lưng chừng núi) để dâng hương, cầu bình an. Chiều xuống, du khách có thể xuống núi, ghé vào một quán ăn địa phương để thưởng thức món bò tơ Tây Ninh nướng tảng cuốn rau rừng và mua vài bịch bánh tráng phơi sương, muối tôm đậm vị mang về làm quà."
            ),
            "tags": [
                "mountain", "spiritual", "cable-car", "viewpoint", "weekend", "short-trip", "cloud-hunting", "statue", "religious",
                "scenic", "local cuisine", "festival", "architecture", "day-trip"
            ],
            "price_level": 1000000,
            "estimated_duration": 12,
        },
        "geo": {"lat": 11.37, "lng": 106.16},
    }
]
"""
====================================================================
DANH SÁCH NEW TAGS CẦN UPDATE CHO MODULE N1 (maps/tags.py)
====================================================================

1. Nhóm Địa hình & Cảnh quan (Nature & Landscape)
"limestone-karst", "geopark", "canyon", "geology", "underground-river", 
"cave exploration", "coral-reef", "sand-dunes", "white-sand", "starfish", 
"volcanic", "garlic-fields", "waterfall", "cliff", "clear-water", "pine-forest", 
"pine-tree", "lotus", "flower", "garden", "mekong-delta", "biosphere", 
"terraced-fields", "rural", "border"

2. Nhóm Hoạt động & Trải nghiệm (Activities & Experiences)
"cable-car", "cloud-hunting", "backpacking", "motorbiking", "jeep-tour", 
"off-road", "rafting", "kayaking", "extreme-sports", "mud-bath", "swimming", 
"water-sports", "kitesurfing", "paragliding", "stand-up-paddle", "speed-boat", 
"island-hopping", "fishing", "camping", "healing", "slow-life"

3. Nhóm Văn hóa, Kiến trúc & Tâm linh (Culture, Architecture & Spiritual)
"unesco-heritage", "unesco", "royal", "imperial", "palace", "temples", 
"ruins", "french-villas", "european-architecture", "architecture", "statue", 
"landmark", "iconic-landmark", "spiritual", "religious", "prison", 
"traditional-music", "lanterns", "tailor", "walking-street", "indigenous", 
"fishing-village", "coracles", "fish-sauce"

4. Nhóm Ẩm thực & Đặc sản (Food & Specialties)
"local-specialty", "local-wine", "foodie", "fruits", "raw"

5. Nhóm Cảm giác & Đặc điểm thời gian/thời tiết (Vibes & Timing)
"winter-trip", "autumn-trip", "summer-trip", "flower-season", "harvest-season", 
"day-trip", "short-trip", "weekend", "vacation", "honeymoon", "morning", 
"sunrise", "sunset", "sunset-view", "night-view", "early-bird", "bustling", 
"chill", "serene", "untouched", "mysterious", "foggy", "majestic", "spectacular", 
"nostalgic", "vintage", "rustic"

6. Nhóm Tiện ích & Du lịch hiện đại (Modern Tourism)
"resort", "homestay", "amusement-park", "theme-park", "entertainment", 
"green-tourism", "wind-turbine"
"""