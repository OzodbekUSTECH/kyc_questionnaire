from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Query
from dishka.integrations.fastapi import FromDishka, DishkaRoute

from app.dto.answers import AnswerListResponse, GetAnswersParams
from app.dto.common import BaseModelResponse, BaseResponse
from app.dto.answers import (
    CreateAnswerRequest,
    GetAnswersParams,
    AnswerListResponse,
    AnswerResponse,
    PartialUpdateAnswerRequest,
)
from app.dto.pagination import PaginatedResponse

from app.interactors.answers.create import CreateAnswerInteractor
from app.interactors.answers.delete import DeleteAnswerInteractor
from app.interactors.answers.get import (
    GetAllAnswersInteractor,
    GetAnswerByIdInteractor,
)
from app.interactors.answers.update import (
    UpdateAnswerPartiallyInteractor,
)

router = APIRouter(
    prefix="/answers",
    tags=["Answers"],
    route_class=DishkaRoute,
)


@router.post("/")
async def create_answer(
    request: CreateAnswerRequest,
    create_answer_interactor: FromDishka[CreateAnswerInteractor],
) -> BaseModelResponse:
    return await create_answer_interactor.execute(request)


@router.get("/")
async def get_answers(
    request: Annotated[GetAnswersParams, Query()],
    get_answers_interactor: FromDishka[GetAllAnswersInteractor],
) -> PaginatedResponse[AnswerListResponse]:
    return await get_answers_interactor.execute(request)


@router.get("/{id}")
async def get_answer_by_id(
    id: UUID,
    get_answer_by_id_interactor: FromDishka[
        GetAnswerByIdInteractor
    ],
) -> AnswerResponse:
    return await get_answer_by_id_interactor.execute(id)


@router.patch("/{id}")
async def update_answer(
    id: UUID,
    request: PartialUpdateAnswerRequest,
    update_answer_interactor: FromDishka[
        UpdateAnswerPartiallyInteractor
    ],
) -> BaseModelResponse:
    return await update_answer_interactor.execute(id, request)


@router.delete("/{id}")
async def delete_answer(
    id: UUID,
    delete_answer_interactor: FromDishka[DeleteAnswerInteractor],
) -> BaseResponse:
    return await delete_answer_interactor.execute(id)
