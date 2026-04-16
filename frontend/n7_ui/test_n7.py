import streamlit as st
import json

def run_ui():
    st.set_page_config(page_title="Travel Experience Planner", page_icon="✈️", layout="wide")
    st.title("🌍 Travel Experience Planner")
    st.markdown("Hệ thống đề xuất trải nghiệm cá nhân hóa")

    # --- KHU VỰC 1: RÀNG BUỘC (SIDEBAR) ---
    st.sidebar.header("⚙️ Ràng buộc thực tế")
    budget = st.sidebar.number_input("Ngân sách tối đa (USD)", min_value=0, value=300, step=10)
    duration = st.sidebar.number_input("Thời gian dự kiến (Giờ)", min_value=0, value=48, step=1)
    people = st.sidebar.number_input("Số lượng người", min_value=1, value=2, step=1)

    # --- KHU VỰC 2: NHẬP LIỆU (TABS) ---
    tab1, tab2 = st.tabs(["📋 Trắc nghiệm sở thích", "✍️ Hình ảnh & Mô tả"])
    
    user_tags = []

    with tab1:
        st.subheader("Hiểu hơn về chuyến đi của bạn")
        
        q1 = st.radio("1. Bạn thích phong cách cảnh quan nào?", ["Hòa mình vào thiên nhiên", "Khám phá đô thị"])
        if q1 == "Hòa mình vào thiên nhiên":
            user_tags.append("thiên nhiên")
            
        q2 = st.radio("2. Nhịp độ chuyến đi bạn mong muốn?", ["Thư giãn, yên tĩnh", "Sôi động, náo nhiệt"])
        if q2 == "Thư giãn, yên tĩnh":
            user_tags.append("yên tĩnh")
            
        q3 = st.radio("3. Bạn đi cùng ai?", ["Đi cùng người yêu (Couple)", "Đi một mình / Bạn bè"])
        if q3 == "Đi cùng người yêu (Couple)":
            user_tags.append("couple")

    with tab2:
        st.subheader("Chi tiết bổ sung")
        user_text = st.text_area("Bạn có yêu cầu đặc biệt gì không?")
        uploaded_image = st.file_uploader("Tải lên hình ảnh nơi bạn muốn đến", type=["jpg", "png", "jpeg"])

    # --- KHU VỰC 3: ĐÓNG GÓI JSON & HIỂN THỊ ---
    if st.button("🚀 Tìm kiếm lộ trình", use_container_width=True):
        
        image_bytes = b""
        if uploaded_image is not None:
            image_bytes = uploaded_image.getvalue()

        # Cục JSON chuẩn bị gửi cho N8
        payload_to_n8 = {
            "text": user_text,
            "image": image_bytes,
            "tags": user_tags,
            "constraints": {
                "budget": float(budget),
                "duration": float(duration),
                "people": int(people)
            }
        }

        st.success("Hệ thống đang xử lý dữ liệu...")
        
        st.divider()
        st.subheader("🎯 Đề xuất dành cho bạn")
        
        try:
            # Đọc file mẫu để hiển thị
            with open("recommendation_output.json", "r", encoding="utf-8") as f:
                result_data = json.load(f)
            
            recs = result_data.get("recommendations", [])
            for index, rec in enumerate(recs):
                loc = rec["location"]
                
                with st.container():
                    st.markdown(f"### Lựa chọn {index + 1}: {loc['name']} ({loc['country']})")
                    col1, col2 = st.columns([2, 1])
                    
                    with col1:
                        st.info(f"**Lý do đề xuất:** {rec['why_recommended']}")
                        st.write(f"**Đặc trưng:** {', '.join(loc['tags'])}")
                    with col2:
                        st.metric("Tổng chi phí ước tính", f"${rec['estimated_total_cost_usd']}")
                        st.metric("Khoảng cách", f"{loc['distance_km']} km")
                    
                    st.markdown("**Các hoạt động nổi bật:**")
                    for act in rec["top_activities"]:
                        st.markdown(f"- 🏃 **{act['name']}** (Chi phí: ${act['cost_usd']})")
                    
                    st.divider()

        except FileNotFoundError:
            st.error("Không tìm thấy file recommendation_output.json.")

if __name__ == "__main__":
    run_ui()