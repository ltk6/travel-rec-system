import google.generativeai as genai
from PIL import Image
import io
# Import key từ file cấu hình chung của nhóm
try:
    from config.settings import GEMINI_API_KEY
except ImportError:
    # Dự phòng nếu file config chưa được push lên
    GEMINI_API_KEY = "YOUR_FALLBACK_KEY"

def process_image(data: dict) -> dict:
    """
    Hàm xử lý ảnh duy nhất (Public API) của Module N2
    Input: {"image": bytes}
    Output: {"image_description": "..."}
    """
    image_bytes = data.get("image")
    if not image_bytes:
        return {"image_description": "Lỗi: Không tìm thấy dữ liệu hình ảnh."}

    # Cấu hình AI
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-2.5-flash')

    try:
        # Xử lý ảnh
        img = Image.open(io.BytesIO(image_bytes))
        if img.mode != 'RGB':
            img = img.convert('RGB')

        prompt = """
        Bạn là chuyên gia phân tích du lịch. Hãy miêu tả bức ảnh này bằng 1 đoạn văn ngắn gọn (2-3 câu).
        Bắt buộc phải có: Loại hình địa điểm, Kiến trúc hoặc Cảnh quan, và Không khí mang lại.
        """
        
        result = model.generate_content([prompt, img])
        
        # Trả về đúng định dạng dict yêu cầu
        return {
            "image_description": result.text.strip()
        }
    except Exception as e:
        return {"image_description": f"Lỗi xử lý AI: {str(e)}"}