from . import pluginbase
import re
import locale
#import json
import logging
#import sys
import urllib
from pprint import pformat

logger = logging.getLogger(__name__)


class Vivino(pluginbase.PluginBase):

    def scrape_product(self, product, elt):
        """ The function to scrape the product item """
        logger.debug('Get product from element\n{}'.format(elt))

        logger.info('review for id {}'.format(pformat(product['product_id'])))

        if elt is None:
            logger.warning('No rating found for {}'.format(product['product_id']))
            self.config['callback'](product) # TODO: overwrites existing rating...
            return

        item = elt.select('.wine-card__content')[0]
        if item is None:
            logger.warning('No rating found on page {}'.format(product['product_id']))
            self.config['callback'](product)
            return

        winery = item.find('a', href=re.compile("wineries"))
        try:
            product['url'] = '{}{}'.format(self.config['base_url'], winery['href'])
            winery2 = winery.select('span')[0]
            product['winery'] = winery2.text.strip()

            winery3 = winery.select('span')[1]
            product['title'] = winery3.text.strip()
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
        expr = re.compile('(\d+) beoordeling', re.I)
        groups = re.match(expr, num_ratings.string.strip())
        logger.info('Rating {}'.format(num_ratings.string.strip()))
        if groups:
            logger.info('Rating2 {}'.format(groups.group(1)))
            product['num_ratings'] = int(float(groups.group(1)))

        logger.info('review \n{}'.format(pformat(product)))
        self.config['callback'](product)

    def scrape_product_list2(self, page, elt, product, callback):
        """ Scrape product list """
        logger.info('Scraping page for element {}'.format(elt))

        if page and len(page.select(elt)) > 0:
            item = page.select(elt)[0]
            callback(product, item)
        else:
            logger.warning('No data found on page')
            callback(product, None)

    def clean_volumes(self, title):
        # one or more digits before decimal separator, optional
        # exactly 1 to 3 digits, with no preceding digits
        # not followed by digits, or year
        # optional whitespace
        # optional volume unit (cl or ltr or liter)
        expr = re.compile(r'((?:\d+(?:,|\.))?(?<!\d)\d{1,3}(?!\d|\syear|e)\s?(?:cl|ltr|liter)?)', re.I)
        return re.sub(expr, '', title).strip()

    def clean_regional_indications(self, title):
        """ Removes any one of the listed regional indications """
        expr = re.compile(r'\s(QW|IGT|IGP|AOC|AC|AOP|DOC|DOCA|DOCG|DOP|DO)\s', re.I)
        return re.sub(expr, ' ', title).strip()

    def clean_special_characters(self, title):
        """ Removes any one of the listed special characters """
        expr = re.compile(r'[#`\.()]', re.I)
        return re.sub(expr, '', title).strip()

    def clean_bottle_sizes(self, title):
        """ Removes any one of the listed bottle sizes """
        expr = re.compile(r'Jeroboam|(Dubbele\s)?Magnum|Methusalem', re.I)
        return re.sub(expr, '', title).strip()

    def clean_misc_annotations(self, title):
        """ Removes any one of the listed bottle sizes """
        res = title
        params = {
            '(2|3|4|5)e\s': '',
            'Sauv\.': 'Sauvignon',
            'Cab\.': 'Cabernet',
            '1e(r)?': 'premier',
            'organic|fles(sen)?': '',
            'weingut|domaine|château|bodegas|cantine|celler|winery|estate|cave|quinta|tenuta': '',
            '\s(de(s|l)?|les|et|das)\s': ' ',
        }
        for k, v in params.items():
            expr = re.compile(k, re.I)
            res = re.sub(expr, v, res)
        return res

    def clean_title(self, name):
        """
        Removes special characters and keywords to build a valid query string
        """
        q = name

        # remove volumes
        q = self.clean_volumes(q)

        # remove bottle sizes
        q = self.clean_bottle_sizes(q)

        # remove regional indications
        q = self.clean_regional_indications(q)

        # remove misc annotations
        q = self.clean_misc_annotations(q)

        # remove special characters
        q = self.clean_special_characters(q)

        return q

    def build_uri(self, rating):
        """ Returns the URI to scrape """
        param = rating['name']

        product = self.get_base_rating(rating['id'])

        if not rating['keywords']:
            args = self.clean_title(param)
            logger.debug('No keywords found, using {}'.format(args))
        else:
            args = rating['keywords']
            logger.debug('Product keywords {}'.format(rating['keywords']))

        param = urllib.parse.urlencode({'q': args})
        page_uri = self.config['page'].format(param)
        uri = '{}{}'.format(self.config['base_url'], page_uri)

        return uri, product

    def scrape_details(self, product):

        soup = self.scrape_detailpage(product['url'])
        if soup:
            for fact in soup.select('div[class^=wineSummary__fact--]'):
                heading = fact.select('div[class^=wineSummary__factHeading--]')[0].text.lower()
                values = []
                for val in fact.select('div[class^=wineSummary__factValue--]'):
                    for ref in val.select('a'):
                        values.append({ 'title': ref.text, 'url': '{}{}'.format(self.config['base_url'], ref['href']) })
                product[heading] = values
        else:
            logger.info('No products on page {}, exiting'.format(product['url']))

        self.config['callback'](product)

    def search_rating(self, rating):
        logger.info('Scrape rating for {} '.format(rating['name']))

        uri, product = self.build_uri(rating)

        logger.info('Scrape page {}'.format(uri))

        page = self.scrape_page(uri)
        if page:
            self.scrape_product_list2(page, '.default-wine-card', product, self.scrape_product)
        else:
            logger.info('No products on page {}, exiting'.format(uri))

def init(config):
    plugin = Vivino()
    plugin.set_config(config)

    logger.info('Starting plugin {}'.format(__name__))
    return plugin
