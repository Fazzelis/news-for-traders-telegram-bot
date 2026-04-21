from sqlalchemy.ext.asyncio import AsyncSession
from src.db.models.user_model import User
from sqlalchemy import select


class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def post(
            self,
            telegram_id: int,
            username: str,
            first_name: str,
            last_name: str
    ) -> User:
        user_db = User(
            telegram_id=telegram_id,
            username=username,
            first_name=first_name,
            last_name=last_name
        )

        self.db.add(user_db)
        await self.db.flush()
        return user_db

    async def get_by_telegram_id(self, telegram_id: int) -> User | None:
        result = await self.db.execute(
            select(User)
            .where(User.telegram_id == telegram_id)
        )

        return result.scalar_one_or_none()

    async def patch(self, user: User, source: str | None, news_on_page: int | None) -> User:
        if source:
            user.default_news_source = source
        if news_on_page:
            user.news_on_page = news_on_page
        self.db.add(user)
        await self.db.flush()
        return user
