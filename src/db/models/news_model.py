from datetime import timezone, timedelta
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

    @property
    def formatted_published_at(self):
        moscow_tz = timezone(timedelta(hours=3))
        moscow_time = self.published_at.astimezone(moscow_tz)
        return moscow_time.strftime("%d.%m.%Y в %H:%M")
