from logging import getLogger
from src.config import settings
from aiogram import Bot, Dispatcher
from src.bot.handlers import *
from aiogram.client.session.aiohttp import AiohttpSession
from src.services.news_service import NewsService
from src.middlewares.user_middleware import UserMiddleware
from src.services.user_service import UserService


class NewsTelegramBot:
    def __init__(self):
        self.logger = getLogger()
        self.session = AiohttpSession(proxy=settings.proxy_url)
        self.bot = Bot(token=settings.bot_token, session=self.session)

        self.user_service = UserService()

        self.dispatcher = Dispatcher()

        self.dispatcher.update.middleware(UserMiddleware(self.user_service))

        self.dispatcher.include_router(start_router)
        self.dispatcher.include_router(news_router)

        self.news_service = NewsService()

    async def start(self):
        self.logger.info(f"Бот запускается...")
        await self.dispatcher.start_polling(
            self.bot,
            data={
                "news_service": self.news_service,
                "user_service": self.user_service
            }
        )
