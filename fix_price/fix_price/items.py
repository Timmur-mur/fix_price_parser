import scrapy
from datetime import datetime
from itemloaders.processors import TakeFirst, MapCompose
from itemloaders import ItemLoader
from .utils.processors import (
        ProcessUrl,
        ProcessSection,
        ProcessBrand,
        ProcessPrice,
        ProcessVariant,
        ProcessStock,
        ProcessAssets,
        ProcessMetadata,
        ProcessVariantOut,
        ProcessAssetsOut
    )


class FixPriceItem(scrapy.Item):
    timestamp = scrapy.Field()
    RPC = scrapy.Field()
    url = scrapy.Field()
    section = scrapy.Field()
    brand = scrapy.Field()
    price_data = scrapy.Field()
    variants = scrapy.Field()
    stock = scrapy.Field()
    assets = scrapy.Field()
    metadata = scrapy.Field()
    title = scrapy.Field()
    # marketing_tags = scrapy.Field() ?


class FixPriceItemLoader(ItemLoader):

    default_item_class = FixPriceItem

    RPC_in = MapCompose(str)
    url_in = MapCompose(ProcessUrl())
    section_in = MapCompose(ProcessSection())
    brand_in = MapCompose(ProcessBrand())
    price_data_in = MapCompose(ProcessPrice())
    variants_in = MapCompose(ProcessVariant())
    stock_in = MapCompose(ProcessStock())
    assets_in = MapCompose(ProcessAssets())
    metadata_in = MapCompose(ProcessMetadata())

    RPC_out = TakeFirst()
    url_out = TakeFirst()
    brand_out = TakeFirst()
    price_data_out = TakeFirst()
    variants_out = ProcessVariantOut()
    stock_out = TakeFirst()
    assets_out = ProcessAssetsOut()
    metadata_out = TakeFirst()
    title_out = TakeFirst()

    def load_item(self):
        item = super().load_item()
        if item.get('brand') is None:
            item['brand'] = ''

        if item.get('timestamp') is None:
            item['timestamp'] = int(datetime.now().timestamp())

        return item

