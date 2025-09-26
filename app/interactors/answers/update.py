from uuid import UUID
from app.dto.answers import PartialUpdateAnswerRequest
from app.dto.common import BaseModelResponse
from app.repositories.uow import UnitOfWork
from app.repositories.answers import AnswersRepository

from app.exceptions.app_error import AppError
from app.exceptions.messages import ErrorMessages

class UpdateAnswerPartiallyInteractor:
    
    def __init__(
        self,
        uow: UnitOfWork,
        answers_repo: AnswersRepository,
    ):
        self.uow = uow
        self.answers_repo = answers_repo
        
        
    async def execute(self, id: UUID, request: PartialUpdateAnswerRequest) -> BaseModelResponse:
        answer = await self.answers_repo.get_one(id=id)
        if not answer:
            raise AppError(404, ErrorMessages.ANSWER_NOT_FOUND)
        await self.answers_repo.update(id, request.model_dump(exclude_unset=True))
        await self.uow.commit()
        return BaseModelResponse(id=answer.id)
    