import google.generativeai as genai
from PIL import Image
import io

# Nhớ dùng API Key mới của ông nhé
def process_image(image_bytes: bytes, api_key: str):
    """
    Hàm xử lý logic: Nhận bytes ảnh, gọi Gemini và trả về mô tả.
    """
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-2.5-flash')
    
    img = Image.open(io.BytesIO(image_bytes))
    if img.mode != 'RGB':
        img = img.convert('RGB')
    
    prompt = """
    Bạn là chuyên gia phân tích du lịch. Hãy miêu tả bức ảnh này bằng 1 đoạn văn ngắn gọn (2-3 câu).
    Bắt buộc phải có: Loại hình địa điểm, Kiến trúc hoặc Cảnh quan, và Không khí mang lại.
    """
    
    result = model.generate_content([prompt, img])
    return result.text.strip()