from sqlalchemy.ext.asyncio import AsyncSession

from app.entities import Survey
from app.repositories.base import BaseRepository


class SurveysRepository(BaseRepository[Survey]):

    def __init__(self, session: AsyncSession):
        super().__init__(session, entity=Survey)
