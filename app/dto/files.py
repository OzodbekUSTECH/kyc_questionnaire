from pydantic import BaseModel


class SavedFileResponse(BaseModel):
    file_name: str
    file_path: str
    file_size: int
    file_type: str
    file_url: str
    