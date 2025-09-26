from dataclasses import dataclass
from typing import Optional, Type
from sqlalchemy import ClauseElement
from sqlalchemy.orm import DeclarativeBase



@dataclass
class JoinConfig:
    target: Type[DeclarativeBase]  # модель для join
    on_clause: Optional[ClauseElement] = None
    isouter: bool = False  # внешний или внутренний join
    full: bool = False  # полный внешний join (редко)
