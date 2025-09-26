from uuid import UUID
from app.dto.surveys import GetSurveysParams, SurveyListResponse, SurveyResponse
from app.dto.pagination import PaginatedResponse
from app.repositories.surveys import SurveysRepository
from app.exceptions.app_error import AppError
from app.exceptions.messages import ErrorMessages

class GetAllSurveysInteractor:
    
    def __init__(
        self,
        surveys_repo: SurveysRepository,
    ):
        self.surveys_repo = surveys_repo
        
        
    async def execute(self, request: GetSurveysParams) -> PaginatedResponse[SurveyListResponse]:
        surveys, total = await self.surveys_repo.get_all_and_count(request)
        return PaginatedResponse(
            items=[SurveyListResponse.model_validate(survey) for survey in surveys],
            total=total,
            page=request.page,
            size=request.size,
        )
        
    
class GetSurveyByIdInteractor:
    
    def __init__(
        self,
        surveys_repo: SurveysRepository,
    ):
        self.surveys_repo = surveys_repo
        
        
    async def execute(self, id: UUID) -> SurveyResponse:
        survey = await self.surveys_repo.get_one(id=id)
        if not survey:
            raise AppError(404, ErrorMessages.SURVEY_NOT_FOUND)
        return SurveyResponse.model_validate(survey)
        
        
        