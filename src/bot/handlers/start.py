from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from src.bot.keyboards.main_reply_keyboard import main_reply_keyboard

router = Router()


@router.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer("""
✨ *Привет! Я твой персональный помощник*

📰 *Возможности:*
━━━━━━━━━━━━━━━━━━━━━━━━━━━
• Мгновенные новости из первых рук
• Подписка на любимые источники

📌 *Доступные источники:*
┣ 📈 Bloomberg
┣ 📰 Коммерсантъ
┗ 🌐 Другие...
    """,
                         reply_markup=main_reply_keyboard())
