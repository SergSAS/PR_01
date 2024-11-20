import cv2
from ultralytics import solutions

MODEL_PATH = './model/best.pt'
CLASSES_TO_COUNT = [0]  # Измените, если нужно

def process_video(video_path: str, output_video_path: str):
    """Обрабатывает видео и возвращает количество объектов IN и OUT."""
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise Exception("Ошибка при чтении видеофайла. Убедитесь, что путь указан верно и файл доступен.")

    w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)

    if w <= 0 or h <= 0:
        raise Exception("Неверные размеры видео. Проверьте исходное видео.")
    if fps <= 0:
        print("FPS не удалось определить, устанавливаю значение 30.")
        fps = 30

    # Определяем кодек и расширение файла
    if output_video_path.endswith('.avi'):
        fourcc = cv2.VideoWriter_fourcc(*"XVID")
    elif output_video_path.endswith('.mp4'):
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    else:
        raise Exception("Неподдерживаемый формат файла. Используйте .avi или .mp4.")

    video_writer = cv2.VideoWriter(output_video_path, fourcc, fps, (w, h))

    center_x = w // 2
    line_points = [(center_x, 0), (center_x, h)]

    counter = solutions.ObjectCounter(
        show=False,
        region=line_points,
        model=MODEL_PATH,
        classes=CLASSES_TO_COUNT
    )

    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            print("Конец видео или кадр не удалось загрузить.")
            break

        processed_frame = counter.count(frame)
        video_writer.write(processed_frame)

    cap.release()
    video_writer.release()
    cv2.destroyAllWindows()

    print(f"Видео успешно обработано и сохранено: {output_video_path}")
    return counter.in_count, counter.out_count
