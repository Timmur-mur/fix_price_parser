

class UrlProvider:

    def __init__(self):
        self.urls = [
            'https://fix-price.com/catalog/letnee-nastroenie/odezhda-leto',
            'https://fix-price.com/catalog/igrushki/kukly-kukolnye-domiki-i-aksessuary',
            'https://fix-price.com/catalog/bytovaya-khimiya/universalnoe-chistyashchee-sredstvo',
            'https://fix-price.com/catalog/sad-i-ogorod/tovary-dlya-dachi-i-piknika',
            'https://fix-price.com/catalog/kosmetika-i-gigiena/ukhod-za-polostyu-rta',
            'https://fix-price.com/catalog/produkty-i-napitki/gazirovannye-napitki',
            'https://fix-price.com/catalog/sad-i-ogorod/instrumenty-dlya-raboty-v-sadu'
        ]
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.index < len(self.urls):
            url = self.urls[self.index]
            self.index += 1
            return url

        raise StopIteration
