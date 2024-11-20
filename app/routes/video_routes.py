from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse
from datetime import datetime
import os
import shutil
from app.services.video_processing import process_video

router = APIRouter()

# Папки для хранения видео
UPLOAD_FOLDER = "./uploaded_videos"
OUTPUT_FOLDER = "./processed_videos"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@router.post("/process_video/")
async def upload_and_process_video(file: UploadFile = File(...)):
    """
    Загружает видео, обрабатывает его и возвращает количество объектов IN/OUT.
    """
    try:
        # Сохраняем загруженный файл
        upload_path = os.path.join(UPLOAD_FOLDER, file.filename)
        with open(upload_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Генерируем уникальное имя для обработанного видео
        output_filename = f"processed_{datetime.now().strftime('%Y%m%d%H%M%S')}.mp4"
        output_path = os.path.join(OUTPUT_FOLDER, output_filename)

        # Подсчет объектов
        in_count, out_count = process_video(upload_path, output_path)

        # Возвращаем результаты
        return JSONResponse(content={
            "message": "Видео обработано успешно",
            "in_count": in_count,
            "out_count": out_count,
            "processed_video_path": output_path
        })
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
