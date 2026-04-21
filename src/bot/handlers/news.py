from aiogram import Router, F
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import Message, CallbackQuery
from src.bot.keyboards.inline_keyboard import (
    news_menu,
    pagination_news_menu,
    settings_menu,
    default_source_menu,
    change_news_on_page_keyboard
)
from src.db.models.user_model import User


router = Router()


@router.message(F.text == "📰 Новости")
async def open_news(message: Message):
    await message.answer(
        "Выберите за сколько дней отправить новости:",
        reply_markup=news_menu()
    )


@router.message(F.text == "⚙️ Настройки")
async def open_settings(message: Message, user: User):
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


@router.callback_query(F.data == "exit-from-settings")
async def back_to_settings(callback: CallbackQuery):
    await callback.message.edit_text(
        text="Настройки сохранены"
    )


@router.callback_query(F.data == "back-to-settings")
async def back_to_settings(callback: CallbackQuery, user: User):
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


@router.callback_query(F.data == "change-default-source")
async def change_default_source(callback: CallbackQuery):
    await callback.message.edit_text(
        text="Выберите новый источник:",
        reply_markup=default_source_menu()
    )


@router.callback_query(F.data == "change-source-to-kommersant")
async def change_source_to_kommersant(callback: CallbackQuery, user: User, data: dict):
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


@router.callback_query(F.data == "change-source-to-bloomberg")
async def change_source_to_bloomberg(callback: CallbackQuery, user: User, data: dict):
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


@router.callback_query(F.data == "change-news-on-page")
async def change_news_on_page(callback: CallbackQuery):
    await callback.message.edit_text(
        text="Выберите количество новостей, которое будет отображаться на одной странице:",
        reply_markup=change_news_on_page_keyboard()
    )


@router.callback_query(F.data.startswith("news_on_page:"))
async def save_news_on_page(callback: CallbackQuery, user: User, data: dict):
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


@router.callback_query(F.data.startswith("page:"))
async def get_paginated_news(callback: CallbackQuery, user: User, data: dict):
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


@router.callback_query(F.data == "back_to_periods")
async def back_to_periods(callback: CallbackQuery):
    await callback.message.edit_text(
        text="Выберите за сколько дней отправить новости:",
        reply_markup=news_menu()
    )

    await callback.answer()


@router.callback_query(F.data == "ignore")
async def ignore_callback(callback: CallbackQuery):
    await callback.answer()


@router.callback_query(F.data == "exit-from-news")
async def exit_from_news(callback: CallbackQuery):
    await callback.message.edit_text("Вы вышли из просмотра новостей")
    await callback.answer()
