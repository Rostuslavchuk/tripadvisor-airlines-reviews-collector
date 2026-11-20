from urllib.parse import urlparse

REVIEWS_URL = "https://www.tripadvisor.com/data/graphql/ids"


def reviews_headers(main_url):
    parsed = urlparse(main_url)
    origin = f"{parsed.scheme}://{parsed.netloc}"

    return {
        "origin": origin,
        "referer": main_url,
        "accept": "*/*",
        "content-type": "application/json",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36",
        "sec-ch-ua": '"Chromium";v="146", "Not-A.Brand";v="24", "Google Chrome";v="146"',
    }


def reviews_params(sku_number, page, SIZE=5):
    return [
        {
            "variables": {
                "locationId": sku_number,
                "filters": [],
                "prefs": None,
                "initialPrefs": {},
                "offset": (page - 1) * SIZE,
                "limit": SIZE,
                "filterCacheKey": None,
                "prefsCacheKey": f"locationReviewPrefs_{sku_number}",
                "needKeywords": True,
                "keywordVariant": "location_keywords_v2_llr_order_30_en",
            },
            "extensions": {"preRegisteredQueryId": "e1ca245af416c316"},
        }
    ]


COOKIES_HEADERS = {
    "accept": (
        "text/html,application/xhtml+xml,application/xml;q=0.9,"
        "image/avif,image/webp,*/*;q=0.8"
    ),
    "accept-language": "en-US,en;q=0.9",
    "referer": "https://www.tripadvisor.com/Airlines",
}
