from app.repositories.uow import UnitOfWork
from app.repositories.answers import AnswersRepository
from app.dto.common import BaseModelResponse
from app.dto.answers import CreateAnswerRequest
from app.entities.answers import Answer



class CreateAnswerInteractor:
    
    def __init__(
        self,
        uow: UnitOfWork,
        answers_repo: AnswersRepository,
    ):
        self.uow = uow
        self.answers_repo = answers_repo
        
        
    async def execute(self, request: CreateAnswerRequest) -> BaseModelResponse:
        answer = Answer(**request.model_dump())
        await self.answers_repo.create(answer)
        await self.uow.commit()
        return BaseModelResponse(id=answer.id)
    