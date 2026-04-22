import asyncio
from logging import getLogger
from src.config import settings
from aiogram import Bot, Dispatcher
from aiogram.client.session.aiohttp import AiohttpSession
from src.services.news_service import NewsService
from src.services.user_service import UserService
from src.services.subscription_service import SubscriptionService
from src.middlewares.user_middleware import UserMiddleware
from src.bot.handlers import *
from src.parsers import *


class NewsTelegramBot:
    def __init__(self):
        self.logger = getLogger()
        self.session = AiohttpSession(proxy=settings.proxy_url)
        self.bot = Bot(token=settings.bot_token, session=self.session)

        self.user_service = UserService()

        self.dispatcher = Dispatcher()

        self.dispatcher.update.middleware(UserMiddleware(self.user_service))

        self.settings_handler = SettingsHandler()
        self.news_handler = NewsHandler()
        self.help_handler = HelpHandler()
        self.subscription_handler = SubscriptionHandler()

        self.dispatcher.include_router(self.settings_handler.router)
        self.dispatcher.include_router(self.news_handler.router)
        self.dispatcher.include_router(self.help_handler.router)
        self.dispatcher.include_router(self.subscription_handler.router)
        parsers = [KommersantParser(), BloombergParser(), InterfaxParser(), TheGuardianParser()]
        self.news_service = NewsService(parsers=parsers)
        self.subscription_service = SubscriptionService()
        asyncio.create_task(self._save_and_send_new_news())

    async def start(self):
        self.logger.info(f"Бот запускается...")
        await self.dispatcher.start_polling(
            self.bot,
            data={
                "news_service": self.news_service,
                "user_service": self.user_service,
                "subscription_service": self.subscription_service
            }
        )

    async def _save_and_send_new_news(self):
        self.logger.info("Получение новых новостей...")
        while True:
            try:
                self.logger.info("Сохранение новостей...")
                added_news = await self.news_service.save_new_news()
                self.logger.info(f"Сохранено {len(added_news)} новостей")
                subs = await self.subscription_service.get_all_subs_on_source()
                for news in added_news:
                    if news.source == "kommersant":
                        for subscription in subs["kommersant_subs"]:
                            await self.bot.send_message(
                                chat_id=subscription.user.telegram_id,
                                text=
                                f"Рассылка:\n\n"
                                f"<b>📰 {news.title}</b>\n\n"
                                f"📅 Новость опубликована {news.formatted_published_at} по МСК\n\n"
                                f"🔗 <a href='{news.url}'>{news.source}</a>\n\n"
                                f"Чтобы отказаться от рассылки, откройте меню, выберите 'Подписки' и отпишитесь от нужных источников",
                                parse_mode="HTML",
                                disable_web_page_preview=True
                            )
                            await asyncio.sleep(0.5)
                    elif news.source == "bloomberg":
                        for subscription in subs["bloomberg_subs"]:
                            await self.bot.send_message(
                                chat_id=subscription.user.telegram_id,
                                text=
                                f"Рассылка:\n\n"
                                f"<b>📰 {news.title}</b>\n\n"
                                f"📅 Новость опубликована {news.formatted_published_at} по МСК\n\n"
                                f"🔗 <a href='{news.url}'>{news.source}</a>\n\n"
                                f"Чтобы отказаться от рассылки, откройте меню, выберите 'Подписки' и отпишитесь от нужных источников",
                                parse_mode="HTML",
                                disable_web_page_preview=True
                            )
                            await asyncio.sleep(0.5)
                    elif news.source == "interfax":
                        for subscription in subs["interfax_subs"]:
                            await self.bot.send_message(
                                chat_id=subscription.user.telegram_id,
                                text=
                                f"Рассылка:\n\n"
                                f"<b>📰 {news.title}</b>\n\n"
                                f"📅 Новость опубликована {news.formatted_published_at} по МСК\n\n"
                                f"🔗 <a href='{news.url}'>{news.source}</a>\n\n"
                                f"Чтобы отказаться от рассылки, откройте меню, выберите 'Подписки' и отпишитесь от нужных источников",
                                parse_mode="HTML",
                                disable_web_page_preview=True
                            )
                            await asyncio.sleep(0.5)
                    elif news.source == "theguardian":
                        for subscription in subs["theguardian_subs"]:
                            await self.bot.send_message(
                                chat_id=subscription.user.telegram_id,
                                text=
                                f"Рассылка:\n\n"
                                f"<b>📰 {news.title}</b>\n\n"
                                f"📅 Новость опубликована {news.formatted_published_at} по МСК\n\n"
                                f"🔗 <a href='{news.url}'>{news.source}</a>\n\n"
                                f"Чтобы отказаться от рассылки, откройте меню, выберите 'Подписки' и отпишитесь от нужных источников",
                                parse_mode="HTML",
                                disable_web_page_preview=True
                            )
                            await asyncio.sleep(0.5)
            except Exception as e:
                self.logger.error(f"Ошибка сохранения новостей: {e}")
            self.logger.info(f"Ожидание {settings.save_new_news_delay} минут")
            await asyncio.sleep(settings.save_new_news_delay * 60)
