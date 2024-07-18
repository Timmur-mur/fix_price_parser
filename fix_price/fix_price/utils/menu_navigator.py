import requests


class Menu:

    MENU = 'https://api.fix-price.com/buyer/v1/category/menu'

    def __init__(self):
        response = requests.get(self.MENU)
        self._menu = {}
        self._mapping(response.json())

    def get(self, key):
        return self._menu.get(key, '')

    def _mapping(self, categories, parent_url=''):

        if not categories:
            return

        for category in categories:
            url = category['url']
            name = category['title']
            if url not in self._menu:
                parent_list = self._menu.get(parent_url)
                if parent_list:
                    new_list = [name for name in parent_list]
                    new_list.append(name)
                    self._menu[url] = new_list
                else:
                    self._menu[url] = [name]

            self._mapping(category['items'], url)








