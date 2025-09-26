
from fastapi import UploadFile
from pathlib import Path
import aiofiles
import uuid
from datetime import datetime

from app.dto.files import SavedFileResponse


class SaveFileInteractor:
    def __init__(self):
        # uploads/ в корне проекта
        self.uploads_dir = Path("uploads/documents")
        self.uploads_dir.mkdir(parents=True, exist_ok=True)  # создаём если нет

    async def execute(self, file: UploadFile) -> SavedFileResponse:
        # Генерируем уникальное имя файла
        file_extension = Path(file.filename).suffix
        unique_filename = f"{uuid.uuid4()}{file_extension}"
        file_path = self.uploads_dir / unique_filename

        # читаем файл кусками и сохраняем
        async with aiofiles.open(file_path, "wb") as f:
            while chunk := await file.read(1024 * 1024):  # читаем по 1 МБ
                await f.write(chunk)

        # берём размер и MIME-тип
        file_size = file_path.stat().st_size
        file_type = file.content_type

        return SavedFileResponse(
            file_name=file.filename,
            file_path=str(file_path),
            file_size=file_size,
            file_type=file_type,
            file_url=f"/uploads/documents/{unique_filename}",  # можно отдавать как статику
        )