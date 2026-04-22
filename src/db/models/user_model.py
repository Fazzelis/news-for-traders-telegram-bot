from src.db.database import Base
from sqlalchemy import (
    Column,
    UUID,
    String,
    func,
    Integer
)
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "user"
    id = Column(UUID(as_uuid=True), primary_key=True, server_default=func.gen_random_uuid())
    telegram_id = Column(Integer, unique=True, nullable=False)
    username = Column(String, unique=True)
    first_name = Column(String)
    last_name = Column(String)
    default_news_source = Column(String, nullable=False, server_default="kommersant")
    news_on_page = Column(Integer, server_default="20")

    subscriptions = relationship("Subscription", back_populates="user")
