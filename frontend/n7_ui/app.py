import streamlit as st
import requests

def run_ui():
    st.set_page_config(page_title="Travel Experience Planner", page_icon="✈️", layout="wide")
    st.title("🌍 Travel Experience Planner")
    st.markdown("Hệ thống đề xuất trải nghiệm cá nhân hóa")

    # --- KHU VỰC 1: RÀNG BUỘC (SIDEBAR) ---
    st.sidebar.header("⚙️ Ràng buộc thực tế")
    budget = st.sidebar.number_input("Ngân sách tối đa (VNĐ)", min_value=0, value=5000000, step=100000)
    duration = st.sidebar.number_input("Thời gian dự kiến (Giờ)", min_value=1, value=48, step=1)
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
        user_text = st.text_area("Bạn có yêu cầu đặc biệt gì không?", placeholder="VD: Muốn đi nơi mát mẻ...")
        image_url_input = st.text_input("Đường dẫn (URL) hình ảnh nơi bạn muốn đến (Nếu có)", placeholder="https://example.com/anh.jpg")

    # --- KHU VỰC 3: GỌI API N8 & HIỂN THỊ ---
    if st.button("🚀 Tìm kiếm lộ trình", use_container_width=True):
        
        # 1. Gom JSON đúng Schema "RecommendRequest" của N8
        payload_to_n8 = {
            "preferences": {
                "text": user_text,
                "image_url": image_url_input if image_url_input.strip() != "" else None,
                "tags": user_tags
            },
            "constraints": {
                "budget": float(budget),
                "duration": int(duration),
                "people": int(people)
            }
        }

        # 2. Gọi API N8
        # N8 đang chạy mặc định ở port 8000
        N8_API_URL = "http://localhost:8000/api/v1/recommend"

        with st.spinner("Đang gửi dữ liệu đến N8 và phân tích lộ trình..."):
            try:
                response = requests.post(N8_API_URL, json=payload_to_n8)
                
                # N8 báo thành công
                if response.status_code == 200:
                    result_data = response.json()
                    
                    st.success(f"Hệ thống phân tích thành công trong {result_data.get('processing_time_ms', 0)}ms!")
                    st.divider()
                    st.subheader("🎯 Đề xuất dành cho bạn")
                    
                    # 3. Phân tách cục JSON Output chuẩn của N8
                    recs = result_data.get("data", {}).get("recommendations", [])
                    
                    if not recs:
                        st.warning("Hệ thống không tìm thấy lộ trình phù hợp với tiêu chí của bạn.")
                    
                    for index, rec in enumerate(recs):
                        loc = rec.get("location", {})
                        itinerary = rec.get("itinerary", {})
                        
                        with st.container():
                            st.markdown(f"### Lựa chọn {index + 1}: {loc.get('name', 'Chưa có tên')}")
                            col1, col2 = st.columns(2)
                            
                            with col1:
                                st.write(f"**Độ phù hợp (Match Score):** {loc.get('match_score', 0) * 100:.1f}%")
                            with col2:
                                st.metric("Tổng chi phí ước tính", f"{itinerary.get('total_cost', 0):,} VNĐ")
                                st.metric("Tổng thời gian hoạt động", f"{itinerary.get('total_duration', 0)} phút")
                            
                            st.markdown("**Các hoạt động nổi bật (N5 & N6 đề xuất):**")
                            activities = itinerary.get("activities", [])
                            if not activities:
                                st.write("- (Không có hoạt động nào được đề xuất)")
                            else:
                                for act in activities:
                                    st.markdown(f"- 🏃 **{act.get('name')}** (Chi phí: {act.get('cost', 0):,} VNĐ | Thời gian: {act.get('duration', 0)} phút)")
                                    if act.get('reason_summary'):
                                        st.caption(f"  *Lý do: {act.get('reason_summary')}*")
                            
                            st.divider()

                # N8 báo lỗi (Ví dụ: 422, 503, 400)
                else:
                    error_detail = response.json().get("detail", {})
                    st.error(f"Lỗi từ hệ thống (Mã {response.status_code}):")
                    st.json(error_detail)

            except requests.exceptions.ConnectionError:
                st.error("🚨 Lỗi: Không thể kết nối tới N8!")

if __name__ == "__main__":
    run_ui()