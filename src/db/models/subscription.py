from src.db.database import Base
from sqlalchemy import (
    Column,
    UUID,
    String,
    func,
    ForeignKey
)
from sqlalchemy.orm import relationship


class Subscription(Base):
    __tablename__ = "subscription"
    id = Column(UUID(as_uuid=True), primary_key=True, server_default=func.gen_random_uuid())
    user_id = Column(UUID(as_uuid=True), ForeignKey("user.id"))
    source = Column(String)

    user = relationship("User", back_populates="subscriptions")
