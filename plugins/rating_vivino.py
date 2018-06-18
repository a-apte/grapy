from . import pluginbase
import re
import locale
#import json
import logging
#import sys
from pprint import pformat

logger = logging.getLogger(__name__)


class Vivino(pluginbase.PluginBase):

    # Set locale
    logger.debug('Set locale')
#    locale.setlocale(locale.LC_ALL, 'nl')

    def scrape_product(self, product_id, elt):
        """ The function to scrape the product item """
        logger.debug('Get product from element\n{}'.format(elt))

        product = self.get_base_rating(product_id)

        logger.info('review for id {}'.format(pformat(product_id)))

        if elt is None:
            logger.warning('No rating found for {}'.format(product_id))
            self.config['callback'](product)
            return

        item = elt.select('.wine-card__content')[0]
        if item is None:
            logger.warning('No rating found on page {}'.format(product_id))
            self.config['callback'](product)
            return

        winery = item.find('a', href=re.compile("wineries"))
        try:
            product['url'] = '{}{}'.format(self.config['base_url'], winery['href'])
            winery2 = winery.select('span')[0]
            product['winery'] = winery2.text.strip()
        except:
            logger.error('Error getting winery from {}'.format(winery))

        region = item.find('a', href=re.compile("wine-regions"))
        try:
            product['region'] = region.text
        except:
            logger.error('Error getting region from {}'.format(region))

        country = item.find('a', href=re.compile("wine-countries"))
        try:
            product['country'] = country.text
        except:
            logger.error('Error getting country from {}'.format(country))

        rating = item.select('.average__number')[0]
        logger.info('Rating {}'.format(rating.text.strip()))
        product['rating'] = locale.atof(rating.text.strip())

        num_ratings = item.select('.text-micro')[0]
        expr = re.compile('(\d+) beoordeling', re.I)  # TODO: locale specific?
        groups = re.match(expr, num_ratings.string.strip())
        logger.info('Rating {}'.format(num_ratings.string.strip()))
        if groups:
            logger.info('Rating2 {}'.format(groups.group(1)))
    #        print(groups.group(1))
            product['num_ratings'] = int(float(groups.group(1)))

        logger.info('review \n{}'.format(pformat(product)))
        self.config['callback'](product)

    def scrape_product_list2(self, page, elt, product_id, callback):
        """ Scrape product list """
        logger.info('Scraping page for element {}'.format(elt))

        if page and len(page.select(elt)) > 0:
            item = page.select(elt)[0]
            callback(product_id, item)
        else:
            logger.warning('No data found on page')
            callback(product_id, None)

    def build_uri(self, product_id, title):
        logger.info('Scrape rating for {}'.format(title))

        # TODO: remove other special characters: ' é #
        # 94 wines
        param = title.replace(' ', '+')

        page_uri = self.config['page'].format(param)
        uri = '{}{}'.format(self.config['base_url'], page_uri)
        logger.info('Scrape page {}'.format(uri))

        page = self.scrape_page(uri)
        if page:
            self.scrape_product_list2(page, '.default-wine-card', product_id, self.scrape_product)
        else:
            logger.info('No products on page {}, exiting'.format(uri))

def init(config):
    plugin = Vivino()
    plugin.set_config(config)

    logger.info('Starting plugin {}'.format(__name__))
    return plugin

