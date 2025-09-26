from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Query
from dishka.integrations.fastapi import FromDishka, DishkaRoute

from app.dto.common import BaseModelResponse, BaseResponse
from app.dto.surveys import (
    CreateSurveyRequest,
    GetSurveysParams,
    SurveyListResponse,
    SurveyResponse,
    PartialUpdateSurveyRequest,
)
from app.dto.pagination import PaginatedResponse

from app.interactors.surveys.create import CreateSurveyInteractor
from app.interactors.surveys.delete import DeleteSurveyInteractor
from app.interactors.surveys.get import (
    GetAllSurveysInteractor,
    GetSurveyByIdInteractor,
)
from app.interactors.surveys.update import (
    UpdateSurveyPartiallyInteractor,
)

router = APIRouter(
    prefix="/surveys",
    tags=["Surveys"],
    route_class=DishkaRoute,
)


@router.post("/")
async def create_survey(
    request: CreateSurveyRequest,
    create_survey_interactor: FromDishka[CreateSurveyInteractor],
) -> BaseModelResponse:
    return await create_survey_interactor.execute(request)


@router.get("/")
async def get_surveys(
    request: Annotated[GetSurveysParams, Query()],
    get_surveys_interactor: FromDishka[GetAllSurveysInteractor],
) -> PaginatedResponse[SurveyListResponse]:
    return await get_surveys_interactor.execute(request)


@router.get("/{id}")
async def get_survey_by_id(
    id: UUID,
    get_survey_by_id_interactor: FromDishka[
        GetSurveyByIdInteractor
    ],
) -> SurveyResponse:
    return await get_survey_by_id_interactor.execute(id)


@router.patch("/{id}")
async def update_survey(
    id: UUID,
    request: PartialUpdateSurveyRequest,
    update_survey_interactor: FromDishka[
        UpdateSurveyPartiallyInteractor
    ],
) -> BaseModelResponse:
    return await update_survey_interactor.execute(id, request)


@router.delete("/{id}")
async def delete_survey(
    id: UUID,
    delete_survey_interactor: FromDishka[DeleteSurveyInteractor],
) -> BaseResponse:
    return await delete_survey_interactor.execute(id)
