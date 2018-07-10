import abc
import requests
import logging
#import sys
from bs4 import BeautifulSoup
from pprint import pformat
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options


logger = logging.getLogger(__name__)


class PluginBase(object):
    __metaclass__ = abc.ABCMeta

    config = {}

    COLOR_WHITE = 'wit'
    COLOR_RED = 'rood'
    COLOR_ROSE = 'rose'
    COLOR_UNKNOWN = 'anders'

    def set_config(self, config):
        logger.info('[{}] Setting plugin config\n{}'.format(
            __name__,
            pformat(config)))
        self.config = config

    def get_base_product(self):
        return {
            'vendor_id': self.config['vendor_id'],
            'code': -1,
            'title': '-',
            'url': '-',
#            'winetype': '-',
#            'color': '-',
            'quantity': 1,
            'volume': 0.75,
            'price': 0.00,
        }

    def get_base_rating(self, product_id):
        return {
#            'type': 'stil',  ## TODO
            'rater_id': self.config['rater_id'],
            'product_id': product_id,
            'winery': 'unknown',
            'region': 'unknown',
            'country': 'unknown',
#            'url': self.config['base_url'],
            'url': '',
#            'keywords': '',
            'rating': 0,
            'num_ratings': 0,
        }

    @abc.abstractmethod
    def scrape_product(self, elt):
        """Scrape product from element."""
        return

    def flatten(self, lst):
        res = lst
        if not lst:
            res = ''
        elif len(lst) == 1:
            res = lst[0]
        return res

    def find_tag(self, tag, r):
        return self.flatten(
            [m.group(1) for m in (r.match(line) for line in tag) if m])

    def scrape_vendor(self, config, callback):
        self.scrape_vendor2(
            config['base_url'],
            config['page'],
            config['max_pages'],
            config['product'],
            callback,
        )

    def scrape_vendor2(self, base_uri, pages, max_pages, elt, callback):
        """ """
        logger.info('Scrape from vendor {}'.format(base_uri))
        has_results = True
        gen = (i for i in range(1, max_pages+1) if has_results)

        for i in gen:
            page_uri = pages.format(i)
            uri = '{}{}'.format(base_uri, page_uri)
            logger.info('Scraping from page {}'.format(uri))

            page = self.scrape_page(uri)
            if page:
                self.scrape_product_list(page, elt, callback)
            else:
                has_results = False  # loop should break
                logger.info('No products on page {}, exiting'.format(i))

    def scrape_page(self, uri):
        """ Scrape page """
        logger.info('Scraping page {}'.format(uri))

        soup = None
        try:
            r = requests.get(uri)
            soup = BeautifulSoup(r.content, 'html.parser')
        except requests.ConnectionError as e:
            logger.error('Connection error: {}'.format(pformat(e)))
        except requests.Timeout as e:
            logger.error('Timeout: {}'.format(pformat(e)))
        except requests.RequestException as e:
            logger.error('Request error: {}'.format(pformat(e)))
        except KeyboardInterrupt:
            logger.error('Keyboard interrupt')
        except Exception as e:
            logger.error('Unknown error: {}'.format(pformat(e)))

        return soup

    def scrape_detailpage(self, uri):
        """ Scrape page """
        logger.info('Scraping detail page {}'.format(uri))

        soup = None
        try:
#            chrome_options = Options()  
#            chrome_options.add_argument("--headless")  
#            chrome_options.binary_location = '/Applications/Google Chrome   Canary.app/Contents/MacOS/Google Chrome Canary'  
#            driver = webdriver.Chrome(
#                executable_path=os.path.abspath('chromedriver'),
#                chrome_options=chrome_options)
            chrome_options = Options()  
            chrome_options.add_argument('--headless')
#            browser = webdriver.Chrome("./chromedriver")
            browser = webdriver.Chrome(
                executable_path='./chromedriver',
                chrome_options=chrome_options)
            browser.get(uri)
            soup = BeautifulSoup(browser.page_source, 'html.parser')
            browser.close()
        except Exception as e:
            logger.error('Unknown error: {}'.format(pformat(e)))

        return soup

    def scrape_product_list(self, page, elt, callback):
        """ Scrape product list """
        logger.info('Scraping page for element {}'.format(elt))

        if page:
            for item in page.select(elt):
                callback(item)
#
#    def scrape_review(self, config, callback):
#        self.scrape_review2(
#            config['base_url'],
#            config['page'],
##            config['max_pages'],
#            config['product'],
#            callback,
#        )
#
#    def scrape_review2(self, base_uri, pages, title, elt, callback):
#        """ """
#        logger.info('Scrape from review {}'.format(base_uri))
##        has_results = True
##        gen = (i for i in range(1, max_pages+1) if has_results)
#
##        for i in gen:
#        page_uri = pages.format(title)
#        uri = '{}{}'.format(base_uri, page_uri)
#        logger.info('Scraping from page {}'.format(uri))
#
#        page = self.scrape_page(uri)
#        if page:
#            self.scrape_product_list(page, elt, callback)
#        else:
#            has_results = False  # loop should break
#            logger.info('No products on page {}, exiting'.format(title))
