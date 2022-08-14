from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains

from browser import Browser

from bs4 import BeautifulSoup
import lxml



class Citilink(Browser):

    def __init__(self):
        super().__init__()
        self.__scrape_classes_init()
        self.actions = ActionChains(self.driver)
        self._init_dataframe_settings()
        self.open_url('https://www.citilink.ru')

    def __scrape_classes_init(self):

        self.listing_view_type = '?view_type=list'
        self.product_title_class = 'ProductCardHorizontal__title.Link.js--Link.Link_type_default'
        self.property_item_class = 'ProductCardHorizontal__properties_item'
        self.property_name_class = 'ProductCardHorizontal__properties_name'
        self.property_value_class = 'ProductCardHorizontal__properties_value'
        self.minicard_class = 'product_data__gtm-js.product_data__pageevents-js.ProductCardHorizontal.js--ProductCardInListing.js--ProductCardInWishlist'
        self.menu_button_class = 'js--PopupCatalogMenu__button-open.PopupCatalogMenu__button-open.Button.jsButton.Button_theme_primary-transparent.Button_size_m.Button_with-icon'
        self.total_category_products_class = 'Subcategory__count.js--Subcategory__count'



    def run(self):

        self._load_listings_list(f'{self.project_path}\citilink_listings.txt')

        for listing_name, listing_url in self.listings_url_list.items():

            try:
                self.open_url(f'{listing_url}{self.listing_view_type}')
                self._get_page_header()
                self._get_product_titles()
                self._find_longest_n_shortest_titles()
                self._count_products_on_page()
                self._find_properties_in_soup()
                self._form_annotation()
                self.group_info.append([listing_name, listing_url, self.page_header, self.product_counter,
                                        self.total_products, self.longest_name, self.annotation_string, '-'])
            except Exception as ex:
                self.group_info.append([listing_name, listing_url, '-', '-', '-', '-', '-', str(ex)])
                print(ex)

        self._create_dataframe()
        self._write_dataframe_to_disk(site_domain='citilink')

    def _get_product_titles(self):

        print(f'\t - Extracting titles')
        self.product_titles = self.driver.find_elements(By.CLASS_NAME, self.product_title_class)
        self.product_titles = [x.text for x in self.product_titles]

        return self.product_titles

    def _find_properties(self):
        print(f'\t - Extracting properties')
        self.page_properties = self.driver.find_elements(By.CLASS_NAME, self.property_name_class)
        self.page_properties = {x.text for x in self.page_properties}
        self.page_properties_string = ' | '.join(self.page_properties)

        return self.page_properties, self.page_properties_string

    def _count_products_on_page(self):

        self.product_counter = len(self.product_titles)
        return self.product_counter

    def _get_total_number_of_products_in_category(self):

        self.total_products = self.driver.find_element(By.CLASS_NAME, self.total_category_products_class).text
        self.total_products = self.total_products.split(' ')[0]

        return self.total_products


    def _get_page_links(self):

        burger_menu_button = self.driver.find_element(By.CLASS_NAME, self.menu_button_class)
        burger_menu_button.click()
        self.scrape_page_urls()
        self.get_catalog_urls()
        self.get_product_urls()

    def _find_properties_in_soup(self):

        self.soup_properties = self.soup.find_all('li', self.property_item_class)
        return self.soup_properties

    def _form_annotation(self):

        annotation_table = {}

        for item in self.soup_properties:
            item_name = item.find('span', self.property_name_class).get_text(strip=True).replace('"', '')
            item_value = item.find('span', self.property_value_class).get_text(strip=True).replace('"', '')
            if item_name in annotation_table.keys():
                pass
            else:
                annotation_table[item_name] = item_value

        self.annotation_string = ' | '.join(f'{name}: {value}' for name, value in annotation_table.items())

        return self.annotation_string

def main():

    cl = Citilink()

    cl.run()
    # cl.open_url()

if __name__ == '__main__':

    main()