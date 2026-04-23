from typing import Optional

from dotenv import load_dotenv
from pydantic_settings import BaseSettings
from pydantic import Field


class Setting(BaseSettings):
    bot_token: str = Field(..., env="BOT_TOKEN")
    database_url: str = Field(default="postgresql+asyncpg://login:password@localhost:5432/news-tg-bot", env="DATABASE_URL")
    save_new_news_delay: int = 5 # в минутах
    proxy_url: Optional[str] = Field(default=None, env="PROXY_URL")

    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Setting()
