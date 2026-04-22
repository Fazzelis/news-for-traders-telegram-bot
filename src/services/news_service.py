import email.utils
import math
from typing import List, Dict, Any
from src.db.models import News
from src.parsers.abstract_parser import Parser
from src.utils.uow import UnitOfWork
from logging import getLogger
from src.schemas.news_schema import NewsResponse
from datetime import timezone, timedelta


class NewsService:
    def __init__(self, parsers: List[Parser] = None):
        self.parsers = parsers
        self.logger = getLogger()

    async def save_new_news(self) -> list[News]:
        uow = UnitOfWork()
        news_list = []
        added_news = []
        async with uow.start():
            for parser in self.parsers:
                result = await parser.get_all_news()
                news_list += result

            for news in news_list:
                optional_news = await uow.news.exist(url=news.url)
                if not optional_news:
                    added_news.append(await uow.news.post(
                        source=news.source,
                        title=news.title,
                        url=news.url,
                        published_at=email.utils.parsedate_to_datetime(news.published_at),
                        description=news.description
                    ))
        self.logger.info(f"Посты успешно добавлены")
        return added_news

    async def get_n_news_for_n_days(self, days: int, page: int, limit: int, source: str) -> Dict[str, Any]:
        uow = UnitOfWork()
        offset = page * limit
        async with uow.start():
            news_list = await uow.news.get_n_news_for_n_days(
                days=days,
                limit=limit,
                offset=offset,
                source=source
            )
            total_news = await uow.news.get_count_news_for_n_days(days=days, source=source)
        total_pages = max(1, math.ceil(total_news / limit))
        moscow_timezone = timezone(timedelta(hours=3))
        return {
            "news": [
                NewsResponse(
                    url=news.url,
                    source=news.source,
                    title=news.title,
                    description=news.description,
                    published_at=news.published_at.astimezone(moscow_timezone).strftime("%d.%m.%Y в %H:%M")
                )
                for news in news_list
            ],
            "total_pages": total_pages
        }
