from aiogram import Router, F
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import Message, CallbackQuery
from src.bot.keyboards.inline_keyboard import (
    settings_menu,
    default_source_menu,
    change_news_on_page_keyboard
)
from src.db.models.user_model import User


class SettingsHandler:

    def __init__(self):
        self.router = Router()
        self._register_handlers()

    def _register_handlers(self):
        self.router.message.register(self.open_settings, F.text == "⚙️ Настройки")
        self.router.callback_query.register(self.exit_from_settings, F.data == "exit-from-settings")
        self.router.callback_query.register(self.back_to_settings, F.data == "back-to-settings")
        self.router.callback_query.register(self.change_default_source, F.data == "change-default-source")
        self.router.callback_query.register(self.change_source_to_kommersant, F.data == "change-source-to-kommersant")
        self.router.callback_query.register(self.change_source_to_bloomberg, F.data == "change-source-to-bloomberg")
        self.router.callback_query.register(self.change_source_to_interfax, F.data == "change-source-to-interfax")
        self.router.callback_query.register(self.change_source_to_theguardian, F.data == "change-source-to-theguardian")
        self.router.callback_query.register(self.change_news_on_page, F.data == "change-news-on-page")
        self.router.callback_query.register(self.save_news_on_page, F.data.startswith("news_on_page:"))

    async def open_settings(self, message: Message, user: User):
        await message.answer(
            text="".join(
                "<b>Выбраны следующие настройки:</b>\n"
                f"Источник по умолчанию: {user.default_news_source}\n"
                f"Количество новостей на странице: {user.news_on_page}\n\n"
                "Выберите необходимый параметр:"
            ),
            parse_mode="HTML",
            reply_markup=settings_menu()
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

    async def exit_from_settings(self, callback: CallbackQuery):
        await callback.message.edit_text(
            text="Настройки сохранены"
        )

    async def back_to_settings(self, callback: CallbackQuery, user: User):
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

    async def change_default_source(self, callback: CallbackQuery):
        await callback.message.edit_text(
            text="Выберите новый источник:",
            reply_markup=default_source_menu()
        )

    async def change_source_to_kommersant(self, callback: CallbackQuery, user: User, data: dict):
        user_service = data["user_service"]
        await user_service.patch_user_info(user=user, source="kommersant")
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
        await callback.answer("Источник успешно обновлен!")

    async def change_source_to_bloomberg(self, callback: CallbackQuery, user: User, data: dict):
        user_service = data["user_service"]
        await user_service.patch_user_info(user=user, source="bloomberg")
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
        await callback.answer("Источник успешно обновлен!")

    async def change_source_to_interfax(self, callback: CallbackQuery, user: User, data: dict):
        user_service = data["user_service"]
        await user_service.patch_user_info(user=user, source="interfax")
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
        await callback.answer("Источник успешно обновлен!")

    async def change_source_to_theguardian(self, callback: CallbackQuery, user: User, data: dict):
        user_service = data["user_service"]
        await user_service.patch_user_info(user=user, source="theguardian")
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
        await callback.answer("Источник успешно обновлен!")

    async def change_news_on_page(self, callback: CallbackQuery):
        await callback.message.edit_text(
            text="Выберите количество новостей, которое будет отображаться на одной странице:",
            reply_markup=change_news_on_page_keyboard()
        )
