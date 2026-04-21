from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from src.bot.keyboards.inline_keyboard import (
    subscription_menu_keyboard,
    subscription_keyboard,
    unsubscription_keyboard
)
from src.db.models import User


class SubscriptionHandler:
    def __init__(self):
        self.router = Router()
        self._register_handlers()

    def _register_handlers(self):
        self.router.message.register(self.open_subscription_menu, F.text == "📫 Подписки")
        self.router.callback_query.register(self.back_to_subscription_main_menu, F.data == "back_to_subscription_main_menu")
        self.router.callback_query.register(self.exit_from_subscriptions, F.data == "exit_from_subscriptions")
        self.router.callback_query.register(self.new_subscription, F.data == "new_subscription")
        self.router.callback_query.register(self.subscribe, F.data.startswith("subscribe:"))
        self.router.callback_query.register(self.new_unsubscription, F.data == "new_unsubscription")
        self.router.callback_query.register(self.unsubscribe, F.data.startswith("unsubscribe:"))

    async def open_subscription_menu(self, message: Message, user: User, data: dict):
        subscription_service = data["subscription_service"]
        user_subscriptions = await subscription_service.get_all_subscriptions(user_id=user.id)
        subscriptions = [subscription.source for subscription in user_subscriptions]
        if len(subscriptions) == 0:
            await message.answer(
                text="У вас нет подписок.\n\nВыберите:",
                reply_markup=subscription_menu_keyboard()
            )
        else:
            text_subscription = ""
            for sub in subscriptions:
                text_subscription += "• " + sub + "\n"
            await message.answer(
                text=f"Ваши подписки:\n{text_subscription}\nВыберите:",
                reply_markup=subscription_menu_keyboard()
            )

    async def new_subscription(self, callback: CallbackQuery, user: User, data: dict):
        subscription_service = data["subscription_service"]
        user_subscriptions = await subscription_service.get_all_subscriptions(user_id=user.id)
        subscriptions = [subscription.source for subscription in user_subscriptions]
        untraceable_source = []
        if "kommersant" not in subscriptions:
            untraceable_source.append("kommersant")

        if "bloomberg" not in subscriptions:
            untraceable_source.append("bloomberg")

        if "interfax" not in subscriptions:
            untraceable_source.append("interfax")

        if "theguardian" not in subscriptions:
            untraceable_source.append("theguardian")

        await callback.message.edit_text(
            text="Доступные источники:",
            reply_markup=subscription_keyboard(available=untraceable_source)
        )

    async def subscribe(self, callback: CallbackQuery, user: User, data: dict):
        source = callback.data.split(":")[1]
        subscription_service = data["subscription_service"]
        await subscription_service.subscribe(user_id=user.id, source=source)

        user_subscriptions = await subscription_service.get_all_subscriptions(user_id=user.id)
        subscriptions = [subscription.source for subscription in user_subscriptions]
        if len(subscriptions) == 0:
            await callback.message.edit_text(
                text="У вас нет подписок.\n\nВыберите:",
                reply_markup=subscription_menu_keyboard()
            )
        else:
            text_subscription = ""
            for sub in subscriptions:
                text_subscription += "• " + sub + "\n"
            await callback.message.edit_text(
                text=f"Ваши подписки:\n{text_subscription}\nВыберите:",
                reply_markup=subscription_menu_keyboard()
            )

    async def new_unsubscription(self, callback: CallbackQuery, user: User, data: dict):
        subscription_service = data["subscription_service"]
        user_subscriptions = await subscription_service.get_all_subscriptions(user_id=user.id)
        subscriptions = [subscription.source for subscription in user_subscriptions]

        await callback.message.edit_text(
            text="Доступные источники:",
            reply_markup=unsubscription_keyboard(available=subscriptions)
        )

    async def unsubscribe(self, callback: CallbackQuery, user: User, data: dict):
        source = callback.data.split(":")[1]
        subscription_service = data["subscription_service"]
        await subscription_service.unsubscribe(user_id=user.id, source=source)

        user_subscriptions = await subscription_service.get_all_subscriptions(user_id=user.id)
        subscriptions = [subscription.source for subscription in user_subscriptions]
        if len(subscriptions) == 0:
            await callback.message.edit_text(
                text="У вас нет подписок.\n\nВыберите:",
                reply_markup=subscription_menu_keyboard()
            )
        else:
            text_subscription = ""
            for sub in subscriptions:
                text_subscription += "• " + sub + "\n"
            await callback.message.edit_text(
                text=f"Ваши подписки:\n{text_subscription}\nВыберите:",
                reply_markup=subscription_menu_keyboard()
            )

    async def back_to_subscription_main_menu(self, callback: CallbackQuery, user: User, data: dict):
        subscription_service = data["subscription_service"]
        user_subscriptions = await subscription_service.get_all_subscriptions(user_id=user.id)
        subscriptions = [subscription.source for subscription in user_subscriptions]
        if len(subscriptions) == 0:
            await callback.message.edit_text(
                text="У вас нет подписок.\n\nВыберите:",
                reply_markup=subscription_menu_keyboard()
            )
        else:
            text_subscription = ""
            for sub in subscriptions:
                text_subscription += "• " + sub + "\n"
            await callback.message.edit_text(
                text=f"Ваши подписки:\n{text_subscription}\nВыберите:",
                reply_markup=subscription_menu_keyboard()
            )

    async def exit_from_subscriptions(self, callback: CallbackQuery):
        await callback.message.edit_text("Вы вышли из подписок")
