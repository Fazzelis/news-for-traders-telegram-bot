from typing import Optional
from pydantic import BaseModel


class NewsResponse(BaseModel):
    url: str
    source: str
    title: str
    description: str
    published_at: str


class NewsItem(BaseModel):
    source: str
    title: str
    url: str
    published_at: Optional[str] = None
    description: str
