# =============================================================================
# n5_activity_templates.py
# =============================================================================
# Hardcoded core activities for each of the 25 seed locations.
# These serve as the "ground truth" to prevent LLM hallucinations.
# =============================================================================

ACTIVITY_TEMPLATES = {
    "loc_001": [ # Fansipan Sapa
        {"name": "Chinh phục đỉnh Fansipan bằng cáp treo", "type": "nature"},
        {"name": "Trekking rừng nguyên sinh Hoàng Liên Sơn", "type": "adventure"},
        {"name": "Săn mây và chụp ảnh tại cột cờ đỉnh núi", "type": "nature"},
        {"name": "Khám phá văn hóa bản làng người H'Mông", "type": "culture"},
        {"name": "Thưởng thức thắng cố và rượu táo mèo", "type": "food"}
    ],
    "loc_002": [ # Đồng Văn Hà Giang
        {"name": "Chinh phục đèo Mã Pí Lèng bằng xe máy", "type": "adventure"},
        {"name": "Đi thuyền trên sông Nho Quế xuyên hẻm Tu Sản", "type": "nature"},
        {"name": "Tham quan Dinh thự Vua Mèo", "type": "culture"},
        {"name": "Check-in hoa tam giác mạch tại thung lũng", "type": "nature"},
        {"name": "Trải nghiệm chợ phiên vùng cao Đồng Văn", "type": "culture"}
    ],
    "loc_003": [ # Mẫu Sơn Lạng Sơn
        {"name": "Săn tuyết và băng giá vào mùa đông", "type": "nature"},
        {"name": "Tham quan phế tích biệt thự Pháp cổ", "type": "culture"},
        {"name": "Tắm lá thuốc người Dao đỏ", "type": "relaxation"},
        {"name": "Thưởng thức rượu Mẫu Sơn trứ danh", "type": "food"}
    ],
    "loc_004": [ # Vịnh Hạ Long
        {"name": "Nghỉ đêm trên du thuyền 5 sao giữa vịnh", "type": "relaxation"},
        {"name": "Chèo thuyền kayak qua hang Luồn", "type": "adventure"},
        {"name": "Khám phá Hang Sửng Sốt kỳ vĩ", "type": "nature"},
        {"name": "Leo núi Titop ngắm toàn cảnh vịnh", "type": "nature"},
        {"name": "Thưởng thức hải sản tại làng chài nổi", "type": "food"}
    ],
    "loc_005": [ # Thác Bản Giốc
        {"name": "Đi bè mảng áp sát chân thác Bản Giốc", "type": "nature"},
        {"name": "Khám phá Động Ngườm Ngao lộng lẫy", "type": "nature"},
        {"name": "Tham quan chùa Phật Tích Trúc Lâm Bản Giốc", "type": "culture"},
        {"name": "Thưởng thức hạt dẻ Trùng Khánh", "type": "food"}
    ],
    "loc_006": [ # Tràng An Ninh Bình
        {"name": "Đi thuyền nan khám phá hang động Tràng An", "type": "nature"},
        {"name": "Leo 500 bậc đá lên đỉnh Hang Múa", "type": "adventure"},
        {"name": "Tham quan Cố đô Hoa Lư lịch sử", "type": "culture"},
        {"name": "Thưởng thức cơm cháy và thịt dê núi", "type": "food"}
    ],
    "loc_007": [ # Phong Nha - Kẻ Bàng
        {"name": "Khám phá Hang Sơn Đoòng (hang động lớn nhất TG)", "type": "adventure"},
        {"name": "Đi thuyền máy vào Hang Phong Nha", "type": "nature"},
        {"name": "Tắm bùn và đu zipline tại Hang Tối", "type": "adventure"},
        {"name": "Vui chơi tại suối Nước Moọc trong vắt", "type": "nature"}
    ],
    "loc_008": [ # Đại Nội Huế
        {"name": "Tham quan Hoàng thành Huế lịch sử", "type": "culture"},
        {"name": "Nghe Nhã nhạc cung đình trên sông Hương", "type": "culture"},
        {"name": "Thưởng thức bún bò Huế và cơm hến", "type": "food"},
        {"name": "Thăm quan các lăng tẩm triều Nguyễn", "type": "culture"}
    ],
    "loc_009": [ # Phố Cổ Hội An
        {"name": "Thả đèn hoa đăng trên sông Hoài buổi tối", "type": "culture"},
        {"name": "Học làm lồng lèn truyền thống", "type": "culture"},
        {"name": "Thưởng thức bánh mì Phượng và Cao lầu", "type": "food"},
        {"name": "Khám phá các hội quán Phúc Kiến, Quảng Đông", "type": "culture"}
    ],
    "loc_010": [ # Bà Nà Hills
        {"name": "Check-in Cầu Vàng (Golden Bridge) nổi tiếng", "type": "nature"},
        {"name": "Tham quan Làng Pháp kiến trúc Gothic", "type": "culture"},
        {"name": "Vui chơi tại Fantasy Park", "type": "adventure"},
        {"name": "Trải nghiệm hầm rượu Debay trăm tuổi", "type": "food"}
    ],
    "loc_011": [ # Thung Lũng Tình Yêu Đà Lạt
        {"name": "Đạp vịt trên hồ Đa Thiện lãng mạn", "type": "relaxation"},
        {"name": "Chụp ảnh tại vườn hoa cẩm tú cầu", "type": "nature"},
        {"name": "Trải nghiệm hái dâu tây tại vườn", "type": "food"},
        {"name": "Đi xe ngựa dạo quanh thung lũng", "type": "relaxation"}
    ],
    "loc_012": [ # Đỉnh Langbiang
        {"name": "Đi xe jeep lên đỉnh Rada ngắm toàn cảnh", "type": "adventure"},
        {"name": "Trekking xuyên rừng thông lên đỉnh núi", "type": "adventure"},
        {"name": "Giao lưu văn hóa cồng chiêng Tây Nguyên", "type": "culture"},
        {"name": "Uống rượu cần và ăn thịt nướng", "type": "food"}
    ],
    "loc_013": [ # Vịnh Nha Trang
        {"name": "Lặn biển ngắm san hô tại đảo Hòn Mun", "type": "adventure"},
        {"name": "Tắm bùn khoáng nóng thư giãn", "type": "relaxation"},
        {"name": "Vui chơi tại VinWonders Nha Trang", "type": "adventure"},
        {"name": "Thưởng thức hải sản tươi sống bến tàu", "type": "food"}
    ],
    "loc_014": [ # Mũi Né Phan Thiết
        {"name": "Trượt cát và lái mô tô ATV tại Đồi Cát Trắng", "type": "adventure"},
        {"name": "Lướt ván diều (kitesurfing) trên biển", "type": "adventure"},
        {"name": "Tham quan Suối Tiên (Fairy Stream)", "type": "nature"},
        {"name": "Ăn hải sản tại làng chài Mũi Né", "type": "food"}
    ],
    "loc_015": [ # Bãi Sao Phú Quốc
        {"name": "Thư giãn trên bãi cát trắng mịn Bãi Sao", "type": "relaxation"},
        {"name": "Lặn ống thở ngắm sao biển đỏ", "type": "nature"},
        {"name": "Đi cáp treo Hòn Thơm vượt biển", "type": "nature"},
        {"name": "Thưởng thức gỏi cá trích đặc sản", "type": "food"}
    ],
    "loc_016": [ # Côn Đảo
        {"name": "Tham quan Nhà tù Côn Đảo (Chuồng Cọp)", "type": "culture"},
        {"name": "Xem rùa đẻ trứng tại Hòn Bảy Cạnh", "type": "nature"},
        {"name": "Lặn biển ngắm san hô nguyên sơ", "type": "adventure"},
        {"name": "Viếng mộ anh hùng Võ Thị Sáu về đêm", "type": "culture"}
    ],
    "loc_017": [ # Đảo Lý Sơn
        {"name": "Check-in Cổng Tò Vò lúc hoàng hôn", "type": "nature"},
        {"name": "Tham quan cánh đồng tỏi bạt ngàn", "type": "culture"},
        {"name": "Leo núi lửa Thới Lới ngắm biển", "type": "nature"},
        {"name": "Thưởng thức gỏi rong biển Lý Sơn", "type": "food"}
    ],
    "loc_018": [ # Bãi Sau Vũng Tàu
        {"name": "Tắm biển và thư giãn tại Bãi Sau", "type": "relaxation"},
        {"name": "Leo núi Nhỏ tham quan Tượng Chúa Kitô Vua", "type": "culture"},
        {"name": "Thưởng thức lẩu cá đuối trứ danh", "type": "food"},
        {"name": "Ăn bánh khọt Cô Ba Vũng Tàu", "type": "food"}
    ],
    "loc_019": [ # Chợ Nổi Cái Răng
        {"name": "Đi thuyền khám phá chợ nổi lúc sáng sớm", "type": "culture"},
        {"name": "Thưởng thức hủ tiếu ngay trên ghe", "type": "food"},
        {"name": "Tham quan lò làm hủ tiếu truyền thống", "type": "culture"},
        {"name": "Ghé thăm vườn trái cây miệt vườn", "type": "nature"}
    ],
    "loc_020": [ # Làng Chài Mũi Né
        {"name": "Đón bình minh và xem cảnh gỡ lưới", "type": "culture"},
        {"name": "Mua hải sản tươi sống trực tiếp từ ngư dân", "type": "food"},
        {"name": "Tham quan xưởng làm nước mắm truyền thống", "type": "culture"},
        {"name": "Chụp ảnh thúng chai bên bờ biển", "type": "nature"}
    ],
    "loc_021": [ # Mù Cang Chải
        {"name": "Ngắm ruộng bậc thang mùa lúa chín", "type": "nature"},
        {"name": "Nhảy dù lượn trên đèo Khâu Phạ", "type": "adventure"},
        {"name": "Khám phá bản Lìm Mông yên bình", "type": "culture"},
        {"name": "Ăn xôi nếp nương và gà đồi", "type": "food"}
    ],
    "loc_022": [ # Đảo Phú Quý
        {"name": "Check-in dốc Phượt ven biển", "type": "nature"},
        {"name": "Chèo SUP tại Vịnh Triều Dương", "type": "adventure"},
        {"name": "Tham quan cột cờ chủ quyền đảo Phú Quý", "type": "culture"},
        {"name": "Thưởng thức bò nóng Phú Quý", "type": "food"}
    ],
    "loc_023": [ # Măng Đen
        {"name": "Đi dạo dưới rừng thông đỏ Măng Đen", "type": "nature"},
        {"name": "Tham quan thác Pa Sỹ hùng vĩ", "type": "nature"},
        {"name": "Viếng tượng Đức Mẹ Măng Đen", "type": "culture"},
        {"name": "Thưởng thức cơm lam và gà nướng", "type": "food"}
    ],
    "loc_024": [ # Cù Lao Chàm
        {"name": "Lặn ngắm san hô (snorkeling) tại bãi Xếp", "type": "adventure"},
        {"name": "Khám phá Giếng cổ Chăm hơn 200 tuổi", "type": "culture"},
        {"name": "Thưởng thức cua đá đặc sản", "type": "food"},
        {"name": "Đi cano cao tốc tham quan các đảo", "type": "adventure"}
    ],
    "loc_025": [ # Núi Bà Đen
        {"name": "Đi cáp treo lên đỉnh núi Bà Đen", "type": "nature"},
        {"name": "Viếng tượng Phật Bà Tây Bổ Đà Sơn", "type": "culture"},
        {"name": "Săn mây trên đỉnh núi cao nhất Nam Bộ", "type": "nature"},
        {"name": "Tham quan hệ thống chùa Bà linh thiêng", "type": "culture"}
    ]
}
