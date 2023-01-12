from app.config import NAVER_API_ID, NAVER_API_SECRET
import aiohttp
import asyncio


class BookScraper:
    def __init__(self):
        self.id = NAVER_API_ID
        self.pw = NAVER_API_SECRET
        self.url = "https://openapi.naver.com/v1/search/book"

    async def fetch(self, session, url):
        headers = {
            "X-Naver-Client-Id": NAVER_API_ID,
            "X-Naver-Client-Secret": NAVER_API_SECRET,
        }
        async with session.get(url, headers=headers) as response:
            result = await response.json()
            items = result["items"]
            return items

    async def scraper(self, keyword, totalpage):
        urls = [
            f"{self.url}?query={keyword}&display=10&start{1 + i * 10}"
            for i in range(totalpage)
        ]
        async with aiohttp.ClientSession() as session:
            all_data = await asyncio.gather(*[self.fetch(session, url) for url in urls])
            result = []
            for data in all_data:
                if data is not None:
                    for book in data:
                        result.append(book)
        return result


if __name__ == "__main__":
    bookscraper = BookScraper()
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    print(asyncio.run(bookscraper.scraper("파이썬", 1)))
