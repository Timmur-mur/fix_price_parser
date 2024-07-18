import scrapy
from ..utils.url_provider import UrlProvider
from ..utils.menu_navigator import Menu
import re
import json
from ..items import FixPriceItemLoader, FixPriceItem


class FixPriceSpider(scrapy.Spider):
    name = "fix"

    LIMIT_ITEMS_IN_RESPONSE = 24
    URL_CATALOG = 'https://fix-price.com/catalog/'
    API_CATALOG_URL = 'https://api.fix-price.com/buyer/v1/product/in/{0}?page={1}&limit={2}&sort=sold'
    API_PAGE_URL = 'https://api.fix-price.com/buyer/v1/product/'
    VIDEO_URL = 'https://www.youtube.com/watch?v='
    REQUEST_POST = {
            "brand": [],
            "isDividedPrice": False,
            "isHit": False,
            "isNew": False,
            "isSpecialPrice": False,
            "price": []
        }

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        return cls(UrlProvider(), Menu(), crawler)

    def __init__(self, url_provider, menu, crawler, *args,  **kwargs):
        super().__init__(*args, **kwargs)
        self.url_provider = url_provider
        self.menu = menu
        self.crawler = crawler

    def start_requests(self):

        for base_url in self.url_provider:
            url = self._change_url_for_api(base_url)
            category = self._get_category_from_url(base_url)
            requests_body = self.REQUEST_POST
            requests_body['category'] = category
            cb_kwargs = {'page_number': 1, 'base_url': base_url, 'category': category}
            yield scrapy.Request(
                method='POST',
                url=url,
                callback=self.parse_catalog,
                body=json.dumps(requests_body),
                cb_kwargs=cb_kwargs
            )

    def parse_catalog(self, response, **kwargs):

        product_carts = response.json()

        if len(product_carts) == self.LIMIT_ITEMS_IN_RESPONSE:
            base_url = kwargs.get('base_url')
            next_page_number = kwargs.get('page_number') + 1
            kwargs['page_number'] = next_page_number
            url = self._change_url_for_api(base_url, page_number=next_page_number)
            requests_body = self.REQUEST_POST
            requests_body['category'] = kwargs.get('category')
            yield scrapy.Request(
                url=url,
                callback=self.parse_catalog,
                method='POST',
                body=json.dumps(requests_body),
                cb_kwargs=kwargs
            )

        for cart in product_carts:
            kwargs['in_stock'] = cart['inStock']
            kwargs['price'] = cart['price']
            kwargs['cart_category'] = cart['category']
            yield scrapy.Request(
                method='GET',
                url=self.API_PAGE_URL + cart['url'],
                callback=self.parse_page_product,
                cb_kwargs=kwargs
            )

    def parse_page_product(self, response, **kwargs):

        product_details = response.json()
        loader = FixPriceItemLoader(item=FixPriceItem(), selector=None, response=response)
        loader.context['url_catalog'] = self.URL_CATALOG
        loader.context['menu'] = self.menu
        loader.context['special_price'] = product_details.get('specialPrice')
        loader.context['image_id'] = product_details.get('image')
        loader.context['video'] = product_details.get('video')
        loader.context['video_url'] = self.VIDEO_URL
        loader.context['cart_category'] = kwargs.get('cart_category')
        loader.context['code'] = product_details.get('id')
        loader.context['product_properties'] = product_details.get('properties')

        loader.add_value(
            'RPC',
            product_details.get('id')
        )
        loader.add_value(
            'url',
            product_details.get('url')
        )
        loader.add_value(
            'section',
            kwargs.get('category')
        )
        loader.add_value(
            'brand',
            product_details.get('brand')
        )
        loader.add_value(
            'price_data',
            kwargs.get('price')
        )
        loader.add_value(
            'variants',
            product_details.get('variants')
        )
        loader.add_value(
            'stock',
            kwargs.get('in_stock')
        )
        loader.add_value(
            'assets',
            product_details.get('images')
        )
        loader.add_value(
            'metadata',
            product_details.get('description')
        )
        loader.add_value(
            'title',
            product_details.get('title')
        )

        item = loader.load_item()

        yield item

    def _change_url_for_api(self, url, page_number=1):
        catalog = re.sub(self.URL_CATALOG, '', url)
        return self.API_CATALOG_URL.format(catalog, page_number, self.LIMIT_ITEMS_IN_RESPONSE)

    def _get_category_from_url(self, url):
        return re.sub(self.URL_CATALOG, '', url)

