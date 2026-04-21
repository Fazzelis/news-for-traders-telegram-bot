from src.utils.uow import UnitOfWork
from logging import getLogger
from src.db.models.user_model import User


class UserService:
    def __init__(self):
        self.logger = getLogger()

    async def get_or_create_user(
            self,
            telegram_id: int,
            username: str,
            first_name: str,
            last_name: str
    ) -> User:
        uow = UnitOfWork()
        async with uow.start():
            user = await uow.users.get_by_telegram_id(telegram_id=telegram_id)
            if not user:
                self.logger.info(f"Обнаружен новый пользователь @{username}, регистрирую...")
                user = await uow.users.post(
                    telegram_id=telegram_id,
                    username=username,
                    first_name=first_name,
                    last_name=last_name
                )
                self.logger.info("Пользователь успешно зарегистрирован")

        return user

    async def patch_user_info(self, user: User, source: str = None, news_on_page: int = None) -> User:
        uow = UnitOfWork()
        async with uow.start():
            user = await uow.users.patch(user=user, source=source, news_on_page=news_on_page)
        return user
