from sqlalchemy.ext.asyncio import AsyncSession
from src.db.models.subscription import Subscription
from sqlalchemy import select, delete
from sqlalchemy.orm import selectinload
from uuid import UUID


class SubscriptionRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def post(self, user_id: UUID, source: str) -> Subscription:
        db_subscription = Subscription(
            user_id=user_id,
            source=source
        )

        self.db.add(db_subscription)
        await self.db.flush()
        return db_subscription

    async def get_all_subscriptions(self, user_id: UUID) -> list[Subscription]:
        result = await self.db.execute(
            select(Subscription)
            .where(Subscription.user_id == user_id)
        )

        return list(result.scalars().all())

    async def get_subscribed_users(self, source: str) -> list[Subscription]:
        result = await self.db.execute(
            select(Subscription)
            .where(Subscription.source == source)
            .options(selectinload(Subscription.user))
        )

        return list(result.scalars().all())

    async def delete(self, user_id: UUID, source: str) -> int:
        result = await self.db.execute(
            delete(Subscription)
            .where(Subscription.user_id == user_id)
            .where(Subscription.source == source)
        )

        return result.rowcount
