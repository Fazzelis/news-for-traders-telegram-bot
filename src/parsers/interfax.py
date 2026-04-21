import re
import html
import aiohttp
from bs4 import BeautifulSoup
from src.schemas.news_schema import NewsItem
from src.parsers.abstract_parser import Parser


class InterfaxParser(Parser):
    def __init__(self):
        self.source = "interfax"
        self.rss_url = "https://www.interfax.ru/rss"

    def clean_text(self, text: str | None) -> str:
        if not text:
            return ""
        text = re.sub(r"<.*?>", "", text)
        text = html.unescape(text)
        text = re.sub(r"\s+", " ", text).strip()
        return text

    async def get_all_news(self):
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(self.rss_url, timeout=20) as response:
                    if response.status != 200:
                        print(f"Error: {response.status}")
                        return []

                    text = await response.text()
                    soup = BeautifulSoup(text, 'xml')

                    news_items = []
                    for item in soup.find_all('item'):
                        title = item.find('title')
                        link = item.find('link')
                        pub_date = item.find('pubDate')
                        description = item.find('description')

                        if not title or not link:
                            continue

                        news_items.append(NewsItem(
                            source=self.source,
                            title=title.text,
                            url=link.text,
                            description=self.clean_text(description.text) if description else "",
                            published_at=pub_date.text if pub_date else ""
                        ))

                    return news_items

            except aiohttp.ClientError as e:
                return []
