import aiohttp
from bs4 import BeautifulSoup
from src.schemas.news_schema import NewsItem
from src.parsers.abstract_parser import Parser


class KommersantParser(Parser):

    def __init__(self):
        self.url = "https://www.kommersant.ru"
        self.source = "kommersant"

    async def get_all_news(self):
        rss_url = f"{self.url}/RSS/news.xml"

        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(rss_url, timeout=20) as response:
                    if response.status != 200:
                        print("Error")
                        return []
                    text = await response.text()
                    soup = BeautifulSoup(text, 'xml')

                    news_items = []
                    for item in soup.find_all('item'):
                        title = item.find('title')
                        link = item.find('link')
                        pub_date = item.find('pubDate')
                        description = item.find('description')

                        if not title or not link or not description:
                            continue

                        title = title.text
                        url = link.text
                        if pub_date and pub_date.text:
                            published_at = pub_date.text

                        news_items.append(NewsItem(
                            source=self.source,
                            title=title,
                            url=url,
                            description=description.text,
                            published_at=published_at
                        ))
                    return news_items
            except aiohttp.ClientError as e:
                return []
