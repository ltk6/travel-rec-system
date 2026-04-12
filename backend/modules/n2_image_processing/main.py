from fastapi import FastAPI, UploadFile, File, HTTPException
from .processor import process_image_logic # Import hàm từ file cùng thư mục

app = FastAPI(title="Tourism N2 Module API")

# API Key nên để ở đây hoặc dùng file .env
MY_API_KEY = "DÁN_API_KEY_MỚI_CỦA_ÔNG_VÀO_ĐÂY"

@app.post("/api/v1/process-image")
async def api_process_image(file: UploadFile = File(...)):
    if file.content_type is None or not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Vui lòng tải lên file ảnh hợp lệ!")

    try:
        # Đọc dữ liệu nhị phân của ảnh
        image_data = await file.read()
        
        # Gọi hàm xử lý từ file processor.py
        description = process_image_logic(image_data, MY_API_KEY)
        
        return {
            "image_decription": description
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))