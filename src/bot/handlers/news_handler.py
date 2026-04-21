from aiogram import Router, F
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import Message, CallbackQuery
from src.bot.keyboards.inline_keyboard import (
    news_menu,
    settings_menu, pagination_news_menu
)
from src.db.models.user_model import User


class NewsHandler:

    def __init__(self):
        self.router = Router()
        self._register_handlers()

    def _register_handlers(self):
        self.router.message.register(self.open_news, F.text == "📰 Новости")
        self.router.callback_query.register(self.save_news_on_page, F.data.startswith("news_on_page:"))
        self.router.callback_query.register(self.get_paginated_news, F.data.startswith("page:"))
        self.router.callback_query.register(self.back_to_periods, F.data == "back_to_periods")
        self.router.callback_query.register(self.exit_from_news, F.data == "exit-from-news")
        self.router.callback_query.register(self.ignore_callback, F.data == "ignore")

    async def open_news(self, message: Message):
        await message.answer(
            "Выберите за сколько дней отправить новости:",
            reply_markup=news_menu()
        )

    async def save_news_on_page(self, callback: CallbackQuery, user: User, data: dict):
        news_count = int(callback.data.split(":")[1])
        user_service = data["user_service"]
        await user_service.patch_user_info(user=user, news_on_page=news_count)
        await callback.message.edit_text(
            text="".join(
                "<b>Выбраны следующие настройки:</b>\n"
                f"Источник по умолчанию: {user.default_news_source}\n\n"
                f"Количество новостей на странице: {user.news_on_page}\n\n"
                "Выберите необходимый параметр:"
            ),
            parse_mode="HTML",
            reply_markup=settings_menu()
        )
        await callback.answer(text="Количество новостей на странице обновлено!")

    async def get_paginated_news(self, callback: CallbackQuery, user: User, data: dict):
        info = callback.data.split(":")
        days = int(info[1])
        page = int(info[2])

        news_service = data["news_service"]
        result = await news_service.get_n_news_for_n_days(
            days=days,
            page=page,
            limit=user.news_on_page
        )
        news_list = result["news"]
        total_pages = result["total_pages"]

        text = "\n\n\n".join(
            f"Новость:\n"
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
                reply_markup=pagination_news_menu(page, total_pages, days),
                disable_web_page_preview=True
            )
        except TelegramBadRequest:
            await callback.answer("Уже здесь")

    async def back_to_periods(self, callback: CallbackQuery):
        await callback.message.edit_text(
            text="Выберите за сколько дней отправить новости:",
            reply_markup=news_menu()
        )

    async def exit_from_news(self, callback: CallbackQuery):
        await callback.message.edit_text("Вы вышли из просмотра новостей")

    async def ignore_callback(self, callback: CallbackQuery):
        await callback.answer()
