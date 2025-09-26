from datetime import datetime
from pydantic import BaseModel
from uuid import UUID
from app.dto.common import BaseModelResponse, TimestampResponse
from app.dto.pagination import PaginationRequest
from app.dto.surveys import BaseSurveyResponse, SurveyResponse
from app.entities.answers import Answer
from app.utils.enums import AnswerStatus
from typing import Optional



class CreateAnswerRequest(BaseModel):
    survey_id: UUID
    data: dict
    uploads: dict
    status: AnswerStatus = AnswerStatus.IN_PROGRESS
    
    
class PartialUpdateAnswerRequest(BaseModel):
    data: Optional[dict] = None
    uploads: Optional[dict] = None
    status: Optional[AnswerStatus] = None
    
class BaseAnswerResponse(BaseModelResponse):
    survey: SurveyResponse
    status: AnswerStatus
    submitted_at: Optional[datetime] = None
    uploads: Optional[dict] = None
    upload_files_quantity: int = 0
    total_files_quantity: int = 0
    
    def model_post_init(self, __context) -> None:
        """Вычисляем количество файлов после инициализации модели"""
        # Подсчитываем загруженные файлы
        if self.uploads:
            total_uploaded = 0
            for section_uploads in self.uploads.values():
                if isinstance(section_uploads, dict):
                    for upload_list in section_uploads.values():
                        if isinstance(upload_list, list):
                            total_uploaded += len(upload_list)
            self.upload_files_quantity = total_uploaded
        
        # Подсчитываем общее количество полей для загрузки
        if self.survey and hasattr(self.survey, 'data') and self.survey.data:
            total_upload_fields = 0
            survey_data = self.survey.data
            if isinstance(survey_data, dict) and 'sections' in survey_data:
                for section in survey_data['sections']:
                    if isinstance(section, dict) and 'uploads' in section:
                        uploads = section['uploads']
                        if isinstance(uploads, list):
                            total_upload_fields += len(uploads)
            self.total_files_quantity = total_upload_fields
    
    
class AnswerListResponse(BaseAnswerResponse, TimestampResponse):
    pass
    
class AnswerResponse(AnswerListResponse):
    data: dict
    uploads: dict 
    
    
class GetAnswersParams(PaginationRequest):
    survey_id: Optional[UUID] = None
    status: Optional[AnswerStatus] = None
    
    class Constants:
        filter_map = {
            "survey_id": lambda value: Answer.survey_id == value,
            "status": lambda value: Answer.status == value,
        }
    

    
    