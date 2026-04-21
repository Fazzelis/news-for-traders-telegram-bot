from src.db.database import Base
from sqlalchemy import (
    Column,
    UUID,
    String,
    func,
    DateTime
)


class News(Base):
    __tablename__ = "news"
    id = Column(UUID(as_uuid=True), primary_key=True, server_default=func.gen_random_uuid())
    url = Column(String, unique=True)
    source = Column(String)
    title = Column(String)
    published_at = Column(DateTime(timezone=True))
    description = Column(String)
