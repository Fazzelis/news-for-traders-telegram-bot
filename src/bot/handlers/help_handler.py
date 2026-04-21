from aiogram import Router, F
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from src.bot.keyboards.inline_keyboard import (
    news_menu,
    settings_menu, pagination_news_menu
)
from src.bot.keyboards.main_reply_keyboard import main_reply_keyboard
from src.db.models.user_model import User


class HelpHandler:
    def __init__(self):
        self.router = Router()
        self._register_handlers()

    def _register_handlers(self):
        self.router.message.register(self.cmd_start, Command("start"))
        self.router.message.register(self.cmd_start, Command("help"))

    async def cmd_start(self, message: Message):
        await message.answer(
            text="".join(
                "✨ *Привет! Я твой персональный помощник*\n\n"
                "📰 *Возможности:*\n"
                "• Просмотр новостей за определенное время\n"
                "• Подписка на любимые источники\n"
                "• Просмотр определенного источника\n\n"
                "📌 *Доступные источники:*\n"
                "• bloomberg\n"
                "• Коммерсантъ\n\n"
                "*Как пользоваться ?*\n"
                "• С помощью команды /start или /help можно увидеть это сообщение.\n"
                "• Основное взаимодействие с ботом происходит через кнопки под строкой ввода сообщения и кнопки у самого сообщения."
            ),
            reply_markup=main_reply_keyboard()
        )
