

BOT_NAME = "fix_price"

SPIDER_MODULES = ["fix_price.spiders"]
NEWSPIDER_MODULE = "fix_price.spiders"


ROBOTSTXT_OBEY = False
COOKIES_ENABLED = True
CLOSESPIDER_ERRORCOUNT = 0
DOWNLOAD_TIMEOUT = 40


CONCURRENT_REQUESTS = 20
CONCURRENT_ITEMS = 10
DOWNLOAD_DELAY = 1.5
CONCURRENT_REQUESTS_PER_DOMAIN = 1
RETRY_TIMES = 1

USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)' \
             ' Chrome/88.0.4324.190 Safari/537.36'

DEFAULT_REQUEST_HEADERS = {
    "Accept": "application/json, text/plain, */*",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3",
    "Connection": "keep-alive",
    "Content-Type": "application/json",
    "Host": "api.fix-price.com",
    "Origin": "https://fix-price.com",
    "Referer": "https://fix-price.com/",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-site",
    "TE": "trailers",
    "x-city": "55", #"3" за мск, # 55 отвечает за Екб
    "X-Key": "43276d5315d180d316d68561cc3dbb46",
    "x-language":  "ru"

}


REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"


DOWNLOADER_MIDDLEWARES = {
    'fix_price.middlewares.FixPriceDownloaderMiddleware': 540,
}

ITEM_PIPELINES = {
    'fix_price.pipelines.FixPricePipeline': 301,
}

