from datetime import datetime
from typing import Optional
from uuid import UUID

from sqlalchemy import ForeignKey, func, text
from app.entities.base import Base
from app.entities.mixins.id_mixin import IdMixin
from app.entities.mixins.timestamp_mixin import TimestampMixin

from sqlalchemy.orm import Mapped, column_property, mapped_column, relationship

from app.utils.enums import AnswerStatus
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.entities.surveys import Survey



class Answer(Base, IdMixin, TimestampMixin):
    __tablename__ = "answers"
    
    survey_id: Mapped[UUID] = mapped_column(ForeignKey("surveys.id"))
    
    data: Mapped[dict] = mapped_column(default=dict, server_default="{}") # ответы
    uploads: Mapped[dict] = mapped_column(default=dict, server_default="{}") # загруженные файлы
    
    status: Mapped[AnswerStatus] = mapped_column(default=AnswerStatus.IN_PROGRESS)
    submitted_at: Mapped[Optional[datetime]]
    
    upload_files_quantity: Mapped[int] = column_property(0)
    total_files_quantity: Mapped[int] = column_property(0)  # Будет заполняться через with_expression
    
    survey: Mapped["Survey"] = relationship()
    
    
    
    
    