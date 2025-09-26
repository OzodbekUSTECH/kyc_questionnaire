



from uuid import UUID
from app.dto.common import BaseModelResponse
from app.dto.surveys import PartialUpdateSurveyRequest
from app.repositories.surveys import SurveysRepository
from app.exceptions.app_error import AppError
from app.exceptions.messages import ErrorMessages
from app.repositories.uow import UnitOfWork


class UpdateSurveyPartiallyInteractor:
    
    def __init__(
        self,
        uow: UnitOfWork,
        surveys_repo: SurveysRepository,
    ):
        self.uow = uow
        self.surveys_repo = surveys_repo
        
        
    async def execute(self, id: UUID, request: PartialUpdateSurveyRequest) -> BaseModelResponse:
        
        survey = await self.surveys_repo.get_one(id=id)
        if not survey:
            raise AppError(404, ErrorMessages.SURVEY_NOT_FOUND)
        await self.surveys_repo.update(id, request.model_dump(exclude_unset=True))
        await self.uow.commit()
        return BaseModelResponse(id=survey.id)
    
        
        
        