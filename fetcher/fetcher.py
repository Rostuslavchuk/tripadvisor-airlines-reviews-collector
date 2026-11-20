from curl_cffi import AsyncSession
from playwright.async_api import async_playwright

from utils.logger import logger_init
from config.headers import reviews_headers, REVIEWS_URL, reviews_params

logger = logger_init()


class Fetcher:
    def __init__(self):
        self.session = None
        self.playwright = None
        self.browser = None
        self.context = None

    async def __aenter__(self):
        self.session = AsyncSession(impersonate="chrome124")

        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(headless=False)

        self.context = await self.browser.new_context()

        return self

    async def __aexit__(self, exc_type, exc_value, exc_traceback):
        if self.session:
            await self.session.close()

        if self.browser:
            await self.browser.close()

        if self.playwright:
            await self.playwright.stop()

    async def collect_cookies_playwright(self, main_url: str):
        try:
            page = await self.context.new_page()

            response = await page.goto(
                main_url, wait_until="domcontentloaded", timeout=30000
            )

            status = response.status if response else None
            logger.info(f"Playwright HTML status: {status}")

            cookies = await self.context.cookies(main_url)
            cookie_dict = {cookie["name"]: cookie["value"] for cookie in cookies}
            self.session.cookies.update(cookie_dict)
            logger.info(f"Cookies collected: {len(cookie_dict)}")

            await page.close()
            return status

        except Exception:
            logger.exception("Playwright cookie collection failed")
            return None

    async def fetch_reviews(self, main_url: str, page: int, sku: int):
        try:
            headers = reviews_headers(main_url)
            params = reviews_params(sku, page)

            response = await self.session.post(
                url=REVIEWS_URL,
                headers=headers,
                json=params,
                timeout=10,
            )

            if response.status_code == 200:
                logger.info(f"Reviews received page: {page}")
                return response.json()

            logger.error(
                "REVIEWS API response:\n"
                f"Status: {response.status_code}\n"
                f"URL: {response.url}\n"
                f"Page: {page}"
            )
            return None

        except Exception:
            logger.exception("Reviews request failed")
            return None
