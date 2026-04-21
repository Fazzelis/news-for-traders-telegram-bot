from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def main_reply_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📰 Новости")],
            [KeyboardButton(text="⚙️ Настройки")],
            [KeyboardButton(text="📫 Подписки")],
        ],
        resize_keyboard=True,
        persistent=True
    )
