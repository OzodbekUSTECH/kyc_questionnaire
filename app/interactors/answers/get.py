


from uuid import UUID

from sqlalchemy.orm import joinedload
from app.dto.answers import AnswerListResponse, AnswerResponse, GetAnswersParams
from app.dto.pagination import PaginatedResponse
from app.entities.answers import Answer
from app.repositories.answers import AnswersRepository
from app.exceptions.app_error import AppError
from app.exceptions.messages import ErrorMessages


class GetAllAnswersInteractor:
    
    def __init__(
        self,
        answers_repo: AnswersRepository,
    ):
        self.answers_repo = answers_repo
        
        
    async def execute(self, request: GetAnswersParams) -> PaginatedResponse[AnswerListResponse]:
        
        answers, total = await self.answers_repo.get_all_and_count(
            request,
            options=[
                joinedload(Answer.survey),
            ],
        )
        return PaginatedResponse(
            items=[AnswerListResponse.model_validate(answer) for answer in answers],
            total=total,
            page=request.page,
            size=request.size,
        )
        
        
class GetAnswerByIdInteractor:
    
    def __init__(
        self,
        answers_repo: AnswersRepository,
    ):
        self.answers_repo = answers_repo
        
        
    async def execute(self, id: UUID) -> AnswerResponse:
        answer = await self.answers_repo.get_one(
            id=id, 
            options=[
                joinedload(Answer.survey),
            ]
        )
        if not answer:
            raise AppError(404, ErrorMessages.ANSWER_NOT_FOUND)
        return AnswerResponse.model_validate(answer)
        