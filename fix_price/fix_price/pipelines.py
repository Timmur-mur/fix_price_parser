import json


class FixPricePipeline:

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.result = []

    def process_item(self, item, spider):
        self.result.append(dict(item))
        return item

    def close_spider(self, spider):
        with open('fix_price.json', 'w', encoding='utf-8') as f:
            json.dump(self.result, f, ensure_ascii=False, indent=4)
