from datetime import datetime

from pydantic import BaseModel, Field


class Record(BaseModel):
    id: int | None = None  # id автоматически генерируется в БД
    text: str
    created_date: datetime | None = Field(default_factory=datetime.now)
    rubrics: str


class SearchResponse(BaseModel):
    query: str
    response: list[Record]
