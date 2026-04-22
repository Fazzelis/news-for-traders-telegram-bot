from aiogram import Router, F
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import Message, CallbackQuery
from src.bot.keyboards.inline_keyboard import (
    pagination_news_menu,
    choose_day_keyboard,
    news_menu,
    choose_news_source
)
from src.db.models.user_model import User


class NewsHandler:

    def __init__(self):
        self.router = Router()
        self._register_handlers()

    def _register_handlers(self):
        self.router.message.register(self.open_news, F.text == "📰 Новости")

        self.router.callback_query.register(self.get_paginated_news, F.data.startswith("page:"))
        self.router.callback_query.register(self.back_to_periods, F.data.startswith("back_to_periods:"))
        self.router.callback_query.register(self.exit_from_news, F.data == "exit-from-news")
        self.router.callback_query.register(self.ignore_callback, F.data == "ignore")
        self.router.callback_query.register(self.choose_source, F.data == "choose_source")
        self.router.callback_query.register(self.choose_day, F.data.startswith("choose_day:"))
        self.router.callback_query.register(self.exit_to_news_menu, F.data == "exit-to-news-menu")

    async def open_news(self, message: Message):
        await message.answer(
            text="Получить новости:",
            reply_markup=news_menu()
        )

    async def choose_source(self, callback: CallbackQuery):
        await callback.message.edit_text(
            text="Выберите источник",
            reply_markup=choose_news_source()
        )

    async def choose_day(self, callback: CallbackQuery):
        source = callback.data.split(":")[1]
        await callback.message.edit_text(
            "Выберите за сколько дней отправить новости:",
            reply_markup=choose_day_keyboard(source=source)
        )

    async def get_paginated_news(self, callback: CallbackQuery, user: User, data: dict):
        _, days, page, source = callback.data.split(":")
        days = int(days)
        page = int(page)

        if source == "default":
            source = user.default_news_source

        news_service = data["news_service"]
        result = await news_service.get_n_news_for_n_days(
            days=days,
            page=page,
            limit=user.news_on_page,
            source=source
        )
        news_list = result["news"]
        total_pages = result["total_pages"]

        text = "\n\n\n".join(
            f"Новость:\n\n"
            f"<b>📰 {news.title}</b>\n\n"
            f"📅 Новость опубликована {news.published_at} по МСК\n\n"
            f"🔗 <a href='{news.url}'>{news.source}</a>"
            f""
            for news in news_list
        )

        text += f"\n\n\n📄 Страница {page + 1} из {total_pages}"
        try:
            await callback.message.edit_text(
                text=text,
                parse_mode="HTML",
                reply_markup=pagination_news_menu(page, total_pages, days, source),
                disable_web_page_preview=True
            )
        except TelegramBadRequest:
            await callback.answer("Уже здесь")

    async def back_to_periods(self, callback: CallbackQuery):
        source = callback.data.split(":")[1]
        await callback.message.edit_text(
            text="Выберите за сколько дней отправить новости:",
            reply_markup=choose_day_keyboard(source=source)
        )

    async def exit_from_news(self, callback: CallbackQuery):
        await callback.message.edit_text("Вы вышли из просмотра новостей")

    async def exit_to_news_menu(self, callback: CallbackQuery):
        await callback.message.edit_text(
            text="Получить новости:",
            reply_markup=news_menu()
        )

    async def ignore_callback(self, callback: CallbackQuery):
        await callback.answer()
