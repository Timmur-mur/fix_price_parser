

class ProcessUrl:

    def __call__(self, url, loader_context):
        url_catalog = loader_context.get('url_catalog')
        return url_catalog + url


class ProcessSection:

    def __call__(self, catalog_url, loader_context):
        sections = loader_context.get('menu')
        return sections.get(catalog_url)


class ProcessBrand:

    def __call__(self, brand):
        if not brand:
            return ''

        return '' if brand.get('title') is None else brand.get('title')


class ProcessPrice:

    def __call__(self, price, loader_context):
        special_price = loader_context.get('special_price')
        if not special_price:
            return {
                'current': price,
                'original': price,
                'sale_tag': ''
            }
        else:
            discount = float(price) - float(special_price.get('price'))
            percent_discount = round(discount * 100 / float(price), 2)
            return {
                'current': special_price.get('price'),
                'original': price,
                'sale_tag': f'Скидка {percent_discount}%'
            }


class ProcessVariant:

    BAD_VARIANTS = ['size', 'fake']

    def __call__(self, variant):
        count = 0
        if variant:
            properties = variant.get('properties')
            if properties:
                for record in properties:
                    if record.get('alias') not in self.BAD_VARIANTS:
                        count += 1

        return count


class ProcessVariantOut:

    def __call__(self, items):
        variants = sum([int(item) for item in items])
        return variants if variants > 0 else 1


class ProcessStock:

    def __call__(self, stock):
        if stock:
            return {
                'in_stock': True,
                'count': stock
            }
        return {
            'in_stock': False,
            'count': 0
        }


class ProcessAssets:

    def __call__(self, asset, loader_context):
        id_main_image = loader_context.get('image_id')
        if id_main_image == asset.get('id'):
            return {
                'main': True,
                'asset': asset
            }
        return {
            'main': False,
            'asset': asset
        }


class ProcessAssetsOut:

    def __call__(self, assets, loader_context):
        result = {}
        for asset in assets:

            if asset.get('main'):
                result['main_image'] = asset.get('asset').get('src')

            result.setdefault('set_images', []).append(asset.get('asset').get('src'))

        result['video'] = []
        video = loader_context.get('video')
        if video:
            video_url = loader_context.get('video_url')
            result['video'] = [video_url + video]

        result['view360'] = []  # ?

        return result


class ProcessMetadata:

    COUNTRY_KEY = 'prodCountry'

    def __call__(self, metadata, loader_context):
        return {
            '__description': metadata,
            'code': loader_context['code'],
            'category_name': loader_context['cart_category'].get('title', ''),
            'category_id': loader_context['cart_category'].get('id', ''),
            'country': self.get_country(loader_context['product_properties'])
        }

    def get_country(self, properties):
        if properties:
            for record in properties:
                if record.get('alias') == self.COUNTRY_KEY:
                    return record['value']

        return ''
