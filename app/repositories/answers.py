from sqlalchemy.ext.asyncio import AsyncSession

from app.entities import Answer
from app.repositories.base import BaseRepository


class AnswersRepository(BaseRepository[Answer]):

    def __init__(self, session: AsyncSession):
        super().__init__(session, entity=Answer)
