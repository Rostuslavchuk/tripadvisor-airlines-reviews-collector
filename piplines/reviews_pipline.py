import asyncio
import argparse
import traceback
import re

from urllib.parse import urlparse

from utils.logger import logger_init
from fetcher.fetcher import Fetcher
from parser.parser import Parser
from storage.scheduler import SchedulerStorage

logger = logger_init()


async def worker(queue, fetcher, lock):
    while True:
        data = await queue.get()
        try:
            if data is None:
                return
            response_reviews = await fetcher.fetch_reviews(
                data["reviews_url"],
                data["page"],
                data["sku"],
            )
            if response_reviews is None:
                return

            parsed_reviews = await asyncio.to_thread(
                Parser().parse_reviews, response_reviews
            )
            async with lock:
                await asyncio.to_thread(
                    SchedulerStorage().set_pdp_storage, parsed_reviews
                )

            logger.info(f"Reviews collected: page {data['page']}")

        except Exception:
            logger.exception("Worker failed")
        finally:
            queue.task_done()


async def main():
    parser = argparse.ArgumentParser(description="Reviews collection")
    parser.add_argument(
        "-u",
        "--url",
        type=str,
        required=True,
        help="Reviews URL to process",
    )
    args = parser.parse_args()

    reviews_url = args.url
    sku = re.search(
        r"(?<=-)[a-zA-Z](\d+)(?=-)",
        urlparse(reviews_url).path,
        re.IGNORECASE,
    )
    sku = int(sku.group(1)) if sku else None
    total_pages = 1

    async with Fetcher() as fetcher:
        await fetcher.collect_cookies_playwright(reviews_url)

        lock = asyncio.Lock()
        queue = asyncio.Queue()

        if sku:
            response = await fetcher.fetch_reviews(reviews_url, total_pages, sku)
            if response is None:
                return

            parsed_reviews = await asyncio.to_thread(Parser().parse_reviews, response)
            async with lock:
                await asyncio.to_thread(
                    SchedulerStorage().set_pdp_storage, parsed_reviews
                )
            logger.info(f"Reviews collected: {total_pages}")
        else:
            logger.error(f"SKU does not exist for: {reviews_url}")
            return

        total_pages = Parser().parse_page_count(response)
        if total_pages > 1:
            for page in range(2, total_pages + 1):
                await queue.put(
                    {
                        "reviews_url": reviews_url,
                        "page": page,
                        "sku": sku,
                    }
                )
            workers = [
                asyncio.create_task(worker(queue, fetcher, lock)) for _ in range(5)
            ]

            await queue.join()
            for _ in workers:
                await queue.put(None)

            await asyncio.gather(*workers, return_exceptions=True)


if __name__ == "__main__":
    asyncio.run(main())
