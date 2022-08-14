from webdriver_manager.chrome import ChromeDriverManager

# selenium imports to remember
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import selenium.common.exceptions as selex
from selenium.webdriver.support.ui import Select

import os
import time
import datetime
import random
import pathlib

import pandas as pd

from bs4 import BeautifulSoup
import lxml


class Browser:

    def __init__(self):

        self.headers = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36'
        self.options = webdriver.ChromeOptions()
        self.options.add_argument(f'user-agent={self.headers}')
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=self.options)
        self.project_path = pathlib.Path.cwd()

    def open_url(self, url: str = 'https://www.google.ru'):

        self.driver.get(url)
        print(f'\nOpening {url}:')
        time.sleep(random.randint(10, 16))

        self.url = url
        self.page_source = self.driver.page_source

        return self.url, self.page_source

    def create_soup_object(self):

        self.soup = BeautifulSoup(self.page_source, 'lxml')
        return self.soup

    def _get_page_header(self):

        self.page_header = self.driver.find_element(By.TAG_NAME, 'h1').text
        return self.page_header

    def scrape_page_urls(self):

        self.page_urls = self.driver.find_elements(By.TAG_NAME, 'a')
        self.page_urls = [x.get_attribute('href') for x in self.page_urls]
        self.page_urls = set(filter(None, self.page_urls))
        self._base_url_filter()

        return self.page_urls

    def _base_url_filter(self):

        filtered_url_set = set()

        for url in self.page_urls:
            if url.find('?') > -1:
                filtered_url_set.add(url.split('?')[0])
            elif url.find('#') > -1:
                filtered_url_set.add(url.split('#')[0])
            else:
                filtered_url_set.add(url)

        self.page_urls = filtered_url_set

        return self.page_urls


    def get_catalog_urls(self):

        self.catalog_urls = set()

        for url in self.page_urls:
            if url.find('/catalog') > -1 :
                self.catalog_urls.add(url)

        return self.catalog_urls

    def get_product_urls(self):

        self.product_urls = set()

        for url in self.page_urls:
            if url.find('/product') > -1 :
                self.catalog_urls.add(url)

        return self.product_urls



    def _init_dataframe_settings(self):

        self.group_info = []
        self.group_columns = ['name', 'url', 'header', 'products', 'longest_name', 'annotations', 'errors']

        return self.group_columns, self.group_info

    def _create_dataframe(self, type: str = 'listing'):

        if type == 'listing':
            self.df = pd.DataFrame(self.group_info, columns=self.group_columns)

        return self.df

    def _write_dataframe_to_disk(self, type: str = 'listing'):

        print('\n-----------------------------------\nWrite to disk\n-----------------------------------\n')
        self.df.to_csv(f'{datetime.date.today()}-{type}.csv')

    # listing features, some variables appears in child classes
    def _find_longest_n_shortest_titles(self):

        self.longest_name = max(self.product_titles, key=len)
        self.shortest_name = min(self.product_titles, key=len)

        return self.longest_name, self.shortest_name

    def _load_listings_list(self, file: str = 'citilink_listings2.txt'):

        print('\n-----------------------------------\nLoading urls list\n-----------------------------------\n')

        self.listings_url_list = {}

        with open(file, 'r') as file:
            lines = file.read().splitlines()
            for line in lines:
                group_name = line.split(';')[0]
                group_url = line.split(';')[1]
                self.listings_url_list[group_name] = group_url

        return self.listings_url_list



def main():

    b = Browser()

    b.open_url()

if __name__ == '__main__':

    main()