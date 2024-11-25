from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from app.routes.video_routes import router as video_router

app = FastAPI()

# Подключение маршрутов
app.include_router(video_router)

# Подключение папки для обработки видео
app.mount("/processed_videos", StaticFiles(directory="./processed_videos"), name="processed_videos")

# Подключение папки для статических файлов
app.mount("/static", StaticFiles(directory="./static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def get_interface():
    with open("static/index.html", "r", encoding="utf-8") as f:
        html_content = f.read()
    return HTMLResponse(content=html_content)

