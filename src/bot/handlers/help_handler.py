from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from src.bot.keyboards.main_reply_keyboard import main_reply_keyboard


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
                "✨ <b>Привет! Я твой персональный помощник</b> ✨\n\n"
                "<b>Возможности:</b>\n\n"
                "• Просмотр новостей за определенное время из выбранного источника\n"
                "• Просмотр новостей за определенное время из источника по умолчанию\n"
                "• Подписка на любимые источники\n"
                "• Выбор источника по умолчанию\n"
                "• Выбор количества отображаемых новостей на одной странице\n\n"
                "<b>Доступные источники:</b>\n\n"
                "• Bloomberg\n"
                "• Коммерсантъ\n"
                "• TheGuardian\n"
                "• Interfax\n\n"
                "<b>Как пользоваться ?</b>\n\n"
                "• С помощью команды /start или /help можно увидеть это сообщение.\n"
                "• Основное взаимодействие с ботом происходит через кнопки."
            ),
            parse_mode="HTML",
            reply_markup=main_reply_keyboard()
        )
