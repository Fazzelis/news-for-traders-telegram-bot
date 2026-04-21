from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def news_menu() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📅 За 1 день", callback_data="page:1:0")],
        [InlineKeyboardButton(text="📆 За неделю", callback_data="page:7:0")],
        [InlineKeyboardButton(text="📆 За 2 недели", callback_data="page:14:0")],
        [InlineKeyboardButton(text="📆 За 4 недели", callback_data="page:28:0")],
        [InlineKeyboardButton(text="Назад", callback_data="exit-from-news")]
    ])


def pagination_news_menu(current_page: int, total_pages: int, days: int) -> InlineKeyboardMarkup:
    keyboard = []
    nav_buttons = []

    nav_buttons.append(
        InlineKeyboardButton(
            text="⏮️",
            callback_data=f"page:{days}:0"
        )
    )
    nav_buttons.append(
        InlineKeyboardButton(
            text="◀️",
            callback_data=f"page:{days}:{max(0, current_page - 1)}"
        )
    )

    nav_buttons.append(
        InlineKeyboardButton(
            text=f"{current_page + 1}/{total_pages}",
            callback_data="ignore"
        )
    )

    nav_buttons.append(
        InlineKeyboardButton(
            text="▶️",
            callback_data=f"page:{days}:{min(total_pages - 1, current_page + 1)}"
        )
    )

    nav_buttons.append(
        InlineKeyboardButton(
            text="⏭️",
            callback_data=f"page:{days}:{total_pages - 1}"
        )
    )

    keyboard.append(nav_buttons)

    keyboard.append([
        InlineKeyboardButton(
            text="🔄 Выбрать другой период",
            callback_data="back_to_periods"
        )
    ])

    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def settings_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Изменить источник новостей по умолчанию", callback_data="change-default-source")],
        [InlineKeyboardButton(text="Изменить количество новостей на странице", callback_data="change-news-on-page")],
        [InlineKeyboardButton(text="Назад", callback_data="exit-from-settings")]
    ])


def default_source_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="kommersant", callback_data="change-source-to-kommersant")],
        [InlineKeyboardButton(text="bloomberg", callback_data="change-source-to-bloomberg")],
        [InlineKeyboardButton(text="Назад", callback_data="back-to-settings")]
    ])


def change_news_on_page_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="1", callback_data="news_on_page:1")],
        [InlineKeyboardButton(text="5", callback_data="news_on_page:5")],
        [InlineKeyboardButton(text="10", callback_data="news_on_page:10")],
        [InlineKeyboardButton(text="20", callback_data="news_on_page:20")],
        [InlineKeyboardButton(text="Назад", callback_data="back-to-settings")]
    ])
