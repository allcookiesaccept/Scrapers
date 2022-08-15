import pandas as pd

from browser import Browser
from selenium.webdriver.common.by import By


class Notik(Browser):

    def __init__(self):

        super().__init__()
        self._init_variables()
        self.open_url('https://www.notik.ru/')

    def run(self):

        for item in self.first_level_menu_items[:5]:

            slug = item

            try:
                self.scraped_df_item['url'] = f'{self.domain}{slug}'
                self.open_url(f'{self.domain}{slug}')
                self._get_page_header()
                self.scraped_df_item['name'] = self.page_header
                self.open_url(f'{self.domain}{slug}{self.empty_filter_request}')
                self._get_page_header()
                self.scraped_df_item['total_products'] = self.page_header.split(': ')[1]
                self._find_available_products()
                self.scraped_df_item['on_page_products'] = str(self.available_products)
                self._count_models_on_page()
                self.scraped_df_item['on_page_models'] = str(self.models_on_page)
            except Exception as ex:
                self.scraped_df_item['errors'].append(f'-----------------------\n{str(ex)}\n-----------------------')

            self.scraped_data_for_df.append(self.scraped_df_item)

        print(self.scraped_data_for_df)
        df = pd.DataFrame.from_dict(self.scraped_data_for_df)
        print(df)
        df.to_csv('notik.csv', sep=';')

    def _init_variables(self):

        self.scraped_data_for_df = []
        self.scraped_df_item = {'url': '-',
                                'header': '-',
                                'category': '-',
                                'brand': '-',
                                'total_products': '-',
                                'on_page_products': '-',
                                'on_page_models': '-',
                                'errors': []
                                }

        self.available_status_class = 'pull-left.available.size10.instock'
        self.models_on_page_class = 'glh.-.title'
        self.availability_filter = 2
        self.first_level_menu_items = ['/index/notebooks.htm',
                                       '/index/monoblocks.htm',
                                       '/index/monitors.htm',
                                       '/index/pads.htm'
                                       '/index/smarts.htm'
                                       '/index/acc.htm'
                                       '/index/mfu.htm'
                                       '/index/soft.htm'
                                       '/index/tv.htm']

        self.empty_filter_request = '?srch=true&full='
        self.domain = 'https://www.notik.ru'

    def _find_available_products(self):

        div_elements = len(self.driver.find_elements(By.CLASS_NAME, self.available_status_class))
        self.available_products = div_elements / self.availability_filter

        return self.available_products

    def _count_models_on_page(self):

        self.models_on_page = len(self.driver.find_elements(By.CLASS_NAME, self.models_on_page_class))

        return self.models_on_page


def main():
    n = Notik()

    n.run()


if __name__ == '__main__':
    main()
