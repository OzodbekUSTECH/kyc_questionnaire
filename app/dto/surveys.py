from typing import Optional
from pydantic import BaseModel

from app.dto.common import BaseModelResponse, TimestampResponse
from app.dto.pagination import PaginationRequest
from app.entities.surveys import Survey


class CreateSurveyRequest(BaseModel):
    title: str
    description: Optional[str] = None
    data: dict
    is_active: bool
    
    
class PartialUpdateSurveyRequest(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    data: Optional[dict] = None
    is_active: Optional[bool] = None
    
    
class BaseSurveyResponse(BaseModelResponse):
    title: str
    description: Optional[str] = None
    is_active: bool
    
class SurveyListResponse(BaseSurveyResponse, TimestampResponse):
    pass

class SurveyResponse(SurveyListResponse):
    data: dict
    
    
class GetSurveysParams(PaginationRequest):
    title: Optional[str] = None
    is_active: Optional[bool] = None
    
    class Constants:
        filter_map = {
            "title": lambda value: Survey.title.ilike(f"%{value}%"),
            "is_active": lambda value: Survey.is_active == value,
        }
        
        searchable_fields = [
            Survey.title, Survey.description,
        ]
        
        orderable_fields = {
            "created_at": Survey.created_at,
            "updated_at": Survey.updated_at,
        }