from logging import getLogger
from uuid import UUID
from src.utils.uow import UnitOfWork
from src.db.models.subscription import Subscription


class SubscriptionService:
    def __init__(self):
        self.logger = getLogger()

    async def subscribe(self, user_id: UUID, source: str) -> Subscription:
        uow = UnitOfWork()
        async with uow.start():
            created_subscription = await uow.subscriptions.post(
                user_id=user_id,
                source=source
            )
        self.logger.info(f"Пользователь {user_id} подписался на {source}")
        return created_subscription

    async def get_all_subscriptions(self, user_id: UUID) -> list[Subscription]:
        uow = UnitOfWork()
        async with uow.start():
            subscriptions = await uow.subscriptions.get_all_subscriptions(user_id=user_id)
        return subscriptions

    async def unsubscribe(self, user_id: UUID, source: str) -> int:
        uow = UnitOfWork()
        async with uow.start():
            rowcount = await uow.subscriptions.delete(user_id=user_id, source=source)
        return rowcount
