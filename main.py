import asyncio
import logging
from src.bot.bot import NewsTelegramBot

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger()


async def main():
    bot = NewsTelegramBot()
    await bot.start()

if __name__ == "__main__":
    asyncio.run(main())
