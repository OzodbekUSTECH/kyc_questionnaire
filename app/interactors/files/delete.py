
from pathlib import Path

from app.dto.common import BaseResponse

class DeleteFileInteractor:
    def __init__(self):
        self.uploads_dir = Path("uploads/documents")

    async def execute(self, file_name: str) -> BaseResponse:
        file_path = self.uploads_dir / file_name
        if file_path.exists() and file_path.is_file():
            file_path.unlink()
        return BaseResponse()