from src.db.database import async_session
from contextlib import asynccontextmanager
from src.db.repositories import *


class UnitOfWork:
    def __init__(self):
        self._session_factory = async_session
        self._session = None

    @asynccontextmanager
    async def start(self):
        async with self._session_factory() as session:
            self._session = session
            try:
                yield self
                await self._session.commit()
            except Exception as e:
                await self._session.rollback()
                raise e
            finally:
                self._session = None

    @property
    def news(self) -> NewsRepository:
        return NewsRepository(db=self._session)

    @property
    def users(self) -> UserRepository:
        return UserRepository(db=self._session)

    @property
    def subscriptions(self) -> SubscriptionRepository:
        return SubscriptionRepository(db=self._session)
