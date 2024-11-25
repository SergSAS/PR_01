import cv2
from ultralytics import solutions
from app.config.settings import settings

def process_video(video_path: str, output_video_path: str):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise Exception("Ошибка при чтении видеофайла.")

    w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)

    if w <= 0 or h <= 0:
        raise Exception("Неверные размеры видео.")
    if fps <= 0:
        fps = 30

    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    video_writer = cv2.VideoWriter(output_video_path, fourcc, fps, (w, h))

    center_x = w // 2
    line_points = [(center_x, 0), (center_x, h)]

    counter = solutions.ObjectCounter(
        show=False,
        region=line_points,
        model=settings.MODEL_PATH,
        classes=settings.CLASSES_TO_COUNT
    )

    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            break
        processed_frame = counter.count(frame)
        video_writer.write(processed_frame)

    cap.release()
    video_writer.release()
    cv2.destroyAllWindows()

    return counter.in_count, counter.out_count
