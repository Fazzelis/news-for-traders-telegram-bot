from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timedelta, UTC
from src.db.models.news_model import News
from sqlalchemy import select, func


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
    ) -> News:
        db_news = News(
            url=url,
            source=source,
            title=title,
            published_at=published_at,
            description=description
        )
        self.db.add(db_news)
        await self.db.flush()
        return db_news

    async def exist(self, url: str) -> News | None:
        result = await self.db.execute(
            select(News)
            .where(News.url == url)
        )

        return result.one_or_none()

    async def get_all(self) -> List[News]:
        result = await self.db.execute(select(News))
        news = result.scalars().all()
        return list(news)

    async def get_n_news_for_n_days(self, days: int, offset: int, limit: int, source: str) -> List[News]:
        start_date = datetime.now(UTC) - timedelta(days=days)
        if source == "all":
            result = await self.db.execute(
                select(News)
                .where(News.published_at >= start_date)
                .order_by(News.published_at.asc())
                .limit(limit)
                .offset(offset)
            )
        else:
            result = await self.db.execute(
                select(News)
                .where(News.published_at >= start_date)
                .where(News.source == source)
                .order_by(News.published_at.asc())
                .limit(limit)
                .offset(offset)
            )

        news = result.scalars().all()
        return list(news)

    async def get_count_news_for_n_days(self, days: int, source: str) -> int:
        start_date = datetime.now(UTC) - timedelta(days=days)
        if source == "all":
            result = await self.db.execute(
                select(func.count(News.id))
                .where(News.published_at >= start_date)
            )
        else:
            result = await self.db.execute(
                select(func.count(News.id))
                .where(News.published_at >= start_date)
                .where(News.source == source)
            )
        return result.scalar()
