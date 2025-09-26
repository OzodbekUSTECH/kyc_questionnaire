from app.dto.common import BaseModelResponse
from app.dto.surveys import CreateSurveyRequest
from app.entities.surveys import Survey
from app.repositories.surveys import SurveysRepository
from app.repositories.uow import UnitOfWork

class CreateSurveyInteractor:
    
    def __init__(
        self,
        uow: UnitOfWork,
        surveys_repo: SurveysRepository,
    ):
        self.uow = uow
        self.surveys_repo = surveys_repo
        
        
    async def execute(self, request: CreateSurveyRequest) -> BaseModelResponse:
        survey = Survey(**request.model_dump())
        await self.surveys_repo.create(survey)
        await self.uow.commit()
        return BaseModelResponse(id=survey.id)
    
    
    
    
    