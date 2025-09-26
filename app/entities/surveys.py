from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column
from app.entities.base import Base
from app.entities.mixins.id_mixin import IdMixin
from app.entities.mixins.timestamp_mixin import TimestampMixin

class Survey(Base, IdMixin, TimestampMixin):
    __tablename__ = "surveys"
    
    title: Mapped[str]
    description: Mapped[Optional[str]]
    
    # хранит структуру (steps, fields, repeaters, uploads)
    data: Mapped[dict] = mapped_column(default=dict, server_default="{}")  
    
    is_active: Mapped[bool] = mapped_column(default=True, server_default="true")
    
    
    
    