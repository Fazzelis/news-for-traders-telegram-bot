import aiohttp
import re
import html
from bs4 import BeautifulSoup
from src.schemas.news_schema import NewsItem
from src.parsers.abstract_parser import Parser


class BloombergParser(Parser):

    def __init__(self):
        self.source = "bloomberg"

        self.rss_urls = [
            'https://feeds.bloomberg.com/markets/news.rss',
            'https://feeds.bloomberg.com/technology/news.rss',
            'https://feeds.bloomberg.com/politics/news.rss',
            'https://feeds.bloomberg.com/business/news.rss',
            'https://feeds.bloomberg.com/wealth/news.rss',
        ]

    def clean_text(self, text: str | None) -> str:
        if not text:
            return ""
        text = re.sub(r"<.*?>", "", text)
        text = html.unescape(text)
        text = re.sub(r"Source:\s*Bloomberg.*", "", text)
        text = re.sub(r"\s+", " ", text).strip()
        return text

    async def get_all_news(self):
        result = []

        async with aiohttp.ClientSession() as session:
            try:
                for url in self.rss_urls:
                    async with session.get(url, timeout=20) as response:
                        if response.status != 200:
                            continue

                        text = await response.text()
                        soup = BeautifulSoup(text, "xml")

                        for item in soup.find_all("item"):
                            title = item.find("title")
                            description = item.find("description")
                            link = item.find("link")
                            pub_date = item.find("pubDate")

                            if not title or not link:
                                continue

                            result.append(
                                NewsItem(
                                    source=self.source,
                                    title=self.clean_text(title.text),
                                    url=link.text,
                                    description=self.clean_text(description.text) if description else "Нет описания",
                                    published_at=pub_date.text if pub_date else None
                                )
                            )

                return result

            except aiohttp.ClientError as e:
                print(e)
                return []
