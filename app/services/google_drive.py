import os
from dotenv import load_dotenv
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# Загружаем переменные окружения из .env
load_dotenv()

# Получаем путь к файлу из переменных окружения
CREDENTIALS_FILE = os.getenv('GOOGLE_SERVICE_ACCOUNT_PATH')

# ID папки Google Drive, куда будут загружаться обработанные видео
FOLDER_ID = os.getenv('GOOGLE_DRIVE_FOLDER_ID')

SCOPES = ['https://www.googleapis.com/auth/drive']

def upload_to_google_drive(file_path):
    """
    Загружает файл на Google Drive через сервисный аккаунт.
    :param file_path: Путь к локальному файлу.
    :return: Ссылка на загруженный файл.
    """
    try:
        # Проверка существования файла
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Файл {file_path} не найден.")

        print(f"Инициализация Google Drive API с использованием учетных данных: {CREDENTIALS_FILE}")

        # Проверка существования файла service_account.json
        if not CREDENTIALS_FILE or not os.path.exists(CREDENTIALS_FILE):
            raise FileNotFoundError(f"Файл учетных данных {CREDENTIALS_FILE} не найден. Проверьте .env.")

        # Аутентификация через сервисный аккаунт
        credentials = service_account.Credentials.from_service_account_file(
            CREDENTIALS_FILE, scopes=SCOPES
        )
        service = build('drive', 'v3', credentials=credentials)

        # Метаданные файла
        file_metadata = {
            'name': os.path.basename(file_path),  # Имя файла на Google Drive
            'parents': [FOLDER_ID]               # Папка для загрузки
        }
        media = MediaFileUpload(file_path, resumable=True)

        print(f"Начало загрузки файла {file_path} на Google Drive в папку с ID {FOLDER_ID}...")

        # Загрузка файла
        uploaded_file = service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id'
        ).execute()

        file_id = uploaded_file.get('id')
        print(f"Файл успешно загружен. ID файла: {file_id}")

        # Настройка доступа "доступно всем по ссылке"
        print("Установка разрешений для файла (доступно всем)...")
        service.permissions().create(
            fileId=file_id,
            body={'type': 'anyone', 'role': 'reader'}
        ).execute()

        # Генерация публичной ссылки
        public_url = f"https://drive.google.com/file/d/{file_id}/view"
        print(f"Публичная ссылка на файл: {public_url}")

        return public_url

    except Exception as e:
        print(f"Ошибка при загрузке файла на Google Drive: {e}")
        raise
