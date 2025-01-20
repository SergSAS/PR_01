# Project Ultralytics

## Описание
Проект для обработки видео с использованием моделей Ultralytics YOLO. Система позволяет загружать видео, обрабатывать их с помощью моделей компьютерного зрения и получать результаты анализа.

## Основные возможности
- Загрузка видео через веб-интерфейс
- Обработка видео с помощью YOLO
- API для интеграции
- Сохранение результатов обработки

## Быстрый старт

### Установка через Docker

1. Клонировать репозиторий: 

bash
git clone https://github.com/your-username/project-ultralytics.git
cd project-ultralytics

2. Настроить окружение:
bash
cp .env.example .env


3. Запустить с помощью Docker:

bash
docker-compose up -d

### Локальная установка

1. Создать виртуальное окружение:
bash
python -m venv venv
source venv/bin/activate # Linux/Mac
venv\Scripts\activate # Windows  


2. Установить зависимости:

bash
pip install -r requirements.txt


3. Запустить приложение:

bash
python -m app.main


## Структура проекта

project-ultralytics/
├── app/ # Основной код приложения
├── model/ # Модели и логика обработки
├── static/ # Статические файлы
├── uploaded_videos/ # Загруженные видео
├── processed_videos/ # Обработанные видео
└── docs/ # Документация


## API Endpoints

### POST /api/v1/videos/upload
Загрузка видео для обработки

### GET /api/v1/videos/{video_id}
Получение статуса обработки видео

## Конфигурация
Основные настройки находятся в файле `.env`. Пример конфигурации можно найти в `.env.example`.

## Требования
- Python 3.9+
- Docker 20.10+ (для Docker установки)
- NVIDIA GPU (опционально)

## Документация
Полная документация доступна в директории [docs](docs/).

## Лицензия
MIT License

## Контакты
При возникновении вопросов обращайтесь в раздел Issues.

