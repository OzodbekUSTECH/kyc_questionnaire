


from uuid import UUID
from app.repositories.surveys import SurveysRepository
from app.dto.common import BaseResponse
from app.repositories.uow import UnitOfWork
from app.exceptions.app_error import AppError
from app.exceptions.messages import ErrorMessages


class DeleteSurveyInteractor:
    
    def __init__(
        self,
        uow: UnitOfWork,
        surveys_repo: SurveysRepository,
    ):
        self.uow = uow
        self.surveys_repo = surveys_repo
        
        
    async def execute(self, id: UUID) -> BaseResponse:
        survey = await self.surveys_repo.get_one(id=id)
        if not survey:
            raise AppError(404, ErrorMessages.SURVEY_NOT_FOUND)
        
        await self.surveys_repo.soft_delete(survey.id)
        await self.uow.commit()
        return BaseResponse(success=True)
        
        
        
        