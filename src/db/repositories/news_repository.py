from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timedelta, UTC
from src.db.models.news_model import News
from sqlalchemy import select, func
from sqlalchemy.dialects.postgresql import insert


class NewsRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def post(
            self,
            source: str,
            title: str,
            url: str,
            published_at: datetime,
            description: str
    ):
        stmt = insert(News).values(
            url=url,
            source=source,
            title=title,
            published_at=published_at,
            description=description
        ).on_conflict_do_nothing(index_elements=['url'])
        await self.db.execute(stmt)

    async def get_all(self) -> List[News]:
        result = await self.db.execute(select(News))
        news = result.scalars().all()
        return list(news)

    async def get_n_news_for_n_days(self, days: int, offset: int, limit: int) -> List[News]:
        start_date = datetime.now(UTC) - timedelta(days=days)
        result = await self.db.execute(
            select(News)
            .where(News.published_at >= start_date)
            .order_by(News.published_at.asc())
            .limit(limit)
            .offset(offset)
        )

        news = result.scalars().all()
        return list(news)

    async def get_count_news_for_n_days(self, days: int) -> int:
        start_date = datetime.now(UTC) - timedelta(days=days)
        result = await self.db.execute(
            select(func.count(News.id))
            .where(News.published_at >= start_date)
        )
        return result.scalar()
