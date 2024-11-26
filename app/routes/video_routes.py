from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse
from datetime import datetime
import os
import shutil
from app.services.video_processing import process_video
from app.config.settings import settings
from app.services.google_drive import upload_to_google_drive
from app.models.response_models import ProcessedVideoResponse  # Импортируем модель

router = APIRouter()

# Убедимся, что папки существуют
os.makedirs(settings.UPLOAD_FOLDER, exist_ok=True)
os.makedirs(settings.OUTPUT_FOLDER, exist_ok=True)


@router.post("/process_video/", response_model=ProcessedVideoResponse)
async def upload_and_process_video(file: UploadFile = File(...)):
    """
    Эндпоинт для обработки видео: подсчет объектов IN/OUT и сохранение результата на Google Drive.
    """
    try:
        # Сохраняем загруженный файл
        upload_path = os.path.join(settings.UPLOAD_FOLDER, file.filename)
        with open(upload_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Обрабатываем видео
        output_filename = f"processed_{datetime.now().strftime('%Y%m%d%H%M%S')}.mp4"
        output_path = os.path.join(settings.OUTPUT_FOLDER, output_filename)
        in_count, out_count = process_video(upload_path, output_path)

        # Загрузка обработанного видео на Google Drive
        google_drive_link = upload_to_google_drive(output_path)

        # Очистка папок после успешной обработки
        clear_folder(settings.UPLOAD_FOLDER)
        clear_folder(settings.OUTPUT_FOLDER)

        # Возвращаем данные пользователю через Pydantic-модель
        return ProcessedVideoResponse(
            message="Видео обработано успешно",
            in_count=in_count,
            out_count=out_count,
            processed_video_link=google_drive_link
        )
    except Exception as e:
        # Если возникает ошибка, возвращаем JSON-ответ с деталями
        return JSONResponse(content={"error": str(e)}, status_code=500)


def clear_folder(folder_path: str):
    """
    Удаляет все файлы и папки внутри указанной папки.
    :param folder_path: Путь к папке, которую нужно очистить.
    """
    print(f"Очистка папки: {folder_path}")
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                print(f"Удаление файла: {file_path}")
                os.unlink(file_path)  # Удаляет файл или символическую ссылку
            elif os.path.isdir(file_path):
                print(f"Удаление папки: {file_path}")
                shutil.rmtree(file_path)  # Удаляет папку и её содержимое
        except Exception as e:
            print(f"Ошибка при удалении {file_path}: {e}")
