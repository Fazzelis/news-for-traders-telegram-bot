from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def news_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Получить новости из источника по умолчанию", callback_data="choose_day:default")],
        [InlineKeyboardButton(text="Получить новости из определенного источника", callback_data="choose_source")],
        [InlineKeyboardButton(text="Назад", callback_data="exit-from-news")]
    ])


def choose_news_source():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Все источники", callback_data="choose_day:all")],
        [InlineKeyboardButton(text="kommersant", callback_data="choose_day:kommersant")],
        [InlineKeyboardButton(text="bloomberg", callback_data="choose_day:bloomberg")],
        [InlineKeyboardButton(text="interfax", callback_data="choose_day:interfax")],
        [InlineKeyboardButton(text="theguardian", callback_data="choose_day:theguardian")],
        [InlineKeyboardButton(text="Назад", callback_data=f"exit-to-news-menu")]
    ])


def choose_day_keyboard(source: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📅 За 1 день", callback_data=f"page:1:0:{source}")],
        [InlineKeyboardButton(text="📆 За неделю", callback_data=f"page:7:0:{source}")],
        [InlineKeyboardButton(text="📆 За 2 недели", callback_data=f"page:14:0:{source}")],
        [InlineKeyboardButton(text="📆 За 4 недели", callback_data=f"page:28:0:{source}")],
        [InlineKeyboardButton(text="Назад", callback_data=f"exit-to-news-menu")]
    ])


def pagination_news_menu(current_page: int, total_pages: int, days: int, source: str) -> InlineKeyboardMarkup:
    keyboard = []
    nav_buttons = []

    nav_buttons.append(
        InlineKeyboardButton(
            text="⏮️",
            callback_data=f"page:{days}:0:{source}"
        )
    )
    nav_buttons.append(
        InlineKeyboardButton(
            text="◀️",
            callback_data=f"page:{days}:{max(0, current_page - 1)}:{source}"
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
            callback_data=f"page:{days}:{min(total_pages - 1, current_page + 1)}:{source}"
        )
    )

    nav_buttons.append(
        InlineKeyboardButton(
            text="⏭️",
            callback_data=f"page:{days}:{total_pages - 1}:{source}"
        )
    )

    keyboard.append(nav_buttons)

    keyboard.append([
        InlineKeyboardButton(
            text="🔄 Выбрать другой период",
            callback_data=f"back_to_periods:{source}"
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
        [InlineKeyboardButton(text="interfax", callback_data="change-source-to-interfax")],
        [InlineKeyboardButton(text="theguardian", callback_data="change-source-to-theguardian")],
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
