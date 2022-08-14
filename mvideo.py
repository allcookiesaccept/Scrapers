from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains

from browser import Browser

from bs4 import BeautifulSoup
import lxml

class Mvideo(Browser):

    def __init__(self):
        super().__init__()
        self.__scrape_classes_init()
        self.actions = ActionChains(self.driver)
        self._init_dataframe_settings()
        self.open_url('https://www.mvideo.ru/')

    def __scrape_classes_init(self):

        self.view_type_switcher_class = 'button.button--light.button--only-icon.button--with-icon.ng-star-inserted'
        self.total_category_number = 'count.ng-star-inserted'
        self.minicard_class = 'product-cards-layout__item.ng-star-inserted'
        self.product_title_class = 'product-title__text'
        self.property_item_class = 'product-feature-list__item.product-feature-list__item--undefined.ng-star-inserted'
        self.property_name_class = 'product-feature-list__name'
        self.property_value_class = 'product-feature-list__value'


    def run(self):

        self._load_listings_list(f'{self.project_path}\mvideo_listings.txt')

        for listing_name, listing_url in self.listings_url_list.items():
            try:
                self.open_url(f'{listing_url}')
                self._get_page_header()
                self._get_total_category_products_number()
                self._get_product_titles()
                self._find_longest_n_shortest_titles()
                self._count_products_on_page()
                self._get_products_properties()
                self._create_annotation_from_properties()
                self.group_info.append([listing_name, listing_url, self.page_header, self.products_on_page_counter,
                                        self.total_number_of_products, self.longest_name, self.annotation_string, '-'])
            except Exception as ex:
                self.group_info.append([listing_name, listing_url, '-', '-', '-', '-', '-', str(ex)])
                print(ex)

        self._create_dataframe()
        self._write_dataframe_to_disk(site_domain='mvideo')

    def _get_product_titles(self):

        self.mini_cards = []

        try:
            self.mini_cards = self.driver.find_elements(By.CLASS_NAME, self.minicard_class)
            if len(self.mini_cards) == 0:
                self._switch_view_type()
                self._get_product_titles()

        except Exception as ex:
            print(ex)

        self.product_titles = self.driver.find_elements(By.CLASS_NAME, self.product_title_class)
        self.product_titles = [x.text for x in self.product_titles]

        return self.mini_cards, self.product_titles

    def _count_products_on_page(self):

        self.products_on_page_counter = len(self.product_titles)
        return self.products_on_page_counter

    def _get_total_category_products_number(self):

        self.total_number_of_products = self.driver.find_element(By.CLASS_NAME, self.total_category_number).text
        return self.total_number_of_products

    def _switch_view_type(self):

        self.view_type_switcher = self.driver.find_element(By.CLASS_NAME, self.view_type_switcher_class)
        self.view_type_switcher.click()

    def _get_products_properties(self):

        self.property_items = self.soup.find_all('li', class_=self.property_item_class.replace('.', ' '))
        return self.property_items

    def _create_annotation_from_properties(self):

        self.annotation_table = {}

        for item in self.property_items:
            prop_name = item.find('span', class_=self.property_name_class).get_text(strip=True)
            prop_values = item.find_all('span', class_=self.property_value_class)
            prop_value = prop_values[0].get_text(strip=True)
            if prop_name in self.annotation_table.keys():
                pass
            else:
                self.annotation_table[prop_name] = prop_value

        self.annotation_string = ' | '.join(f'{key}: {value}' for key, value in self.annotation_table.items())

        return self.annotation_table, self.annotation_string





def main():

    mv = Mvideo()

    mv.run()

if __name__ == '__main__':

    main()