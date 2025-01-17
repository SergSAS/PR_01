from ultralytics import YOLO
from datetime import datetime
import os
from PIL import Image

MODEL_PATH = "./model/best.pt"  # Укажите путь к вашей модели
model = YOLO(MODEL_PATH)

def process_image(image_path, output_folder):
    """
    Обрабатывает изображение с помощью YOLO и сохраняет результат с корректными цветами.
    """
    try:
        # Выполнение инференса
        results = model(image_path)

        # Проверка результатов
        if not results:
            raise ValueError("Результаты детекции отсутствуют.")

        # Получение количества объектов
        num_objects = len(results[0].boxes) if results[0].boxes else 0

        # Убедимся, что выходная папка существует
        os.makedirs(output_folder, exist_ok=True)

        # Генерация имени файла
        output_filename = f"processed_{datetime.now().strftime('%Y%m%d%H%M%S')}.jpg"
        output_path = os.path.join(output_folder, output_filename)

        # Получение изображения с аннотациями
        annotated_image = results[0].plot()  # Возвращает RGB-изображение

        # Сохранение изображения через PIL для корректной обработки цветов
        image = Image.fromarray(annotated_image)  # Конвертация массива в изображение
        image.save(output_path)  # Сохранение без искажений цветов

        # Логирование
        print(f"Обнаружено объектов: {num_objects}. Результат сохранён в: {output_path}")

        return num_objects, output_path
    except Exception as e:
        print(f"Ошибка при обработке изображения: {str(e)}")
        raise RuntimeError(f"Ошибка при обработке изображения: {str(e)}")
