import streamlit as st
import httpx

st.title("🧭 Smart Tourism")

text = st.text_area("Bạn muốn đi đâu?")
top_k = st.slider("Top K", 3, 10, 5)

if st.button("Tìm"):
    with st.spinner("Đang tìm..."):
        try:
            res = httpx.post(
                "http://localhost:8000/recommend",
                json={"text": text, "top_k": top_k},
                timeout=20.0 
            ).json()

            st.write("Sở thích của bạn:", ", ".join(res["tags"]))
            for loc in res["results"]:
                st.info(f"📍 {loc['name']} - Score: {loc['score']}")
        except Exception as e:
            st.error(f"Lỗi kết nối Backend: {e}")

