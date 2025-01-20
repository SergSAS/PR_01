FROM python:3.9-slim

WORKDIR /app

# Установка системных зависимостей
RUN apt-get update && apt-get install -y \
    ffmpeg \
    libsm6 \
    libxext6 \
    && rm -rf /var/lib/apt/lists/*

# Копирование и установка зависимостей Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копирование кода приложения
COPY . .

# Создание необходимых директорий
RUN mkdir -p uploaded_videos processed_videos logs

# Установка переменных окружения
ENV PYTHONUNBUFFERED=1
ENV APP_ENV=production

# Запуск приложения
CMD ["python", "-m", "app.main"] 