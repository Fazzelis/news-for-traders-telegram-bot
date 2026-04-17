from dotenv import load_dotenv
from pydantic_settings import BaseSettings
from pydantic import Field

load_dotenv()


class Setting(BaseSettings):
    bot_key: str = Field(..., env="BOT_TOKEN")
    database_url: str = Field(default="postgresql+asyncpg://login:password@localhost:5432/news-tg-bot", env="DATABASE_URL")

    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Setting()
