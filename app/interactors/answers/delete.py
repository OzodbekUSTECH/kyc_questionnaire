


from uuid import UUID
from app.dto.common import BaseModelResponse
from app.repositories.answers import AnswersRepository
from app.repositories.uow import UnitOfWork
from app.exceptions.app_error import AppError
from app.exceptions.messages import ErrorMessages

class DeleteAnswerInteractor:
    
    def __init__(
        self,
        uow: UnitOfWork,
        answers_repo: AnswersRepository,
    ):
        self.uow = uow
        self.answers_repo = answers_repo
        
        
    async def execute(self, id: UUID) -> BaseModelResponse:
        answer = await self.answers_repo.get_one(id=id)
        if not answer:
            raise AppError(404, ErrorMessages.ANSWER_NOT_FOUND)
        await self.answers_repo.delete(id)
        await self.uow.commit()
        return BaseModelResponse(id=answer.id)
        