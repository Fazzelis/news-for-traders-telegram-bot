import asyncio
from src.services.news_service import NewsService
from src.parsers import *
from src.config import settings
import logging
from src.bot.bot import NewsTelegramBot

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger()


async def check_and_save_new_news(news_service: NewsService):
    while True:
        try:
            logger.info("Сохранение новостей...")
            await news_service.save_new_news()
            logger.info("Сохранение новостей завершено")
        except Exception as e:
            logger.error(f"Ошибка сохранения новостей: {e}")
        logger.info("Ожидание 5 минут")
        await asyncio.sleep(settings.save_new_news_delay * 60)


async def main():
    parsers = [KommersantParser(), BloombergParser(), InterfaxParser(), TheGuardianParser()]
    news_service = NewsService(parsers=parsers)
    asyncio.create_task(check_and_save_new_news(news_service=news_service))

    bot = NewsTelegramBot()
    await bot.start()

if __name__ == "__main__":
    asyncio.run(main())
