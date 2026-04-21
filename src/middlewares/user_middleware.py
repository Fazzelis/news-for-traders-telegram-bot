from typing import Callable, Awaitable, Any
from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery
from src.services.user_service import UserService


class UserMiddleware(BaseMiddleware):
    def __init__(self, user_service: UserService):
        super().__init__()
        self.user_service = user_service

    async def __call__(
            self,
            handler: Callable[[Message, dict[str, Any]], Awaitable[Any]],
            event: Message | CallbackQuery,
            data: dict[str, Any]
    ) -> Any:
        user = data.get("event_from_user")
        db_user = await self.user_service.get_or_create_user(
            telegram_id=user.id,
            username=user.username,
            first_name=user.first_name,
            last_name=user.last_name
        )

        data["user"] = db_user

        return await handler(event, data)
