from . import pluginbase
import re
import locale
import json
import logging

logger = logging.getLogger(__name__)


class Gall(pluginbase.PluginBase):

    # Set locale
    logger.debug('Set locale')
    locale.setlocale(locale.LC_ALL, 'nl')

    def get_volume(self, url):
        # TODO: do it nicely with regex
        volume = 0.75
        if '150cl' in url or '150-cl' in url:
            volume = 1.5
        elif '375cl' in url or '37-5cl' in url:
            volume = 0.375
        elif '25cl' in url:
            volume = 0.25
        elif '20cl' in url:
            volume = 0.2
        elif '50cl' in url:
            volume = 0.5
        elif '100cl' in url:
            volume = 1
        elif '600cl' in url:
            volume = 6
        return volume

#    def get_title(self, title):
#        expr = re.compile(r'\d{1,3}\s?cl|Magnum|2X75CL|37.5CL|37,5cl', re.I)
#        return re.sub(expr, '', title).strip()

    def get_quantity(self, url):
        # TODO: do it nicely with regex
        quantity = 1
        if '-2x' in url:
            quantity = 2
        if '-6x' in url:
            quantity = 6
        return quantity

#    def get_color(self, category):
#        color = 'Overig'
#        if re.search('rood|rode', category, flags=re.I) is not None:
#            color = 'Rood'
#        elif re.search('wit', category, flags=re.I) is not None:
#            color = 'Wit'
#        elif re.search('rosé|rose', category, flags=re.I) is not None:
#            color = 'Rosé'
#        return color

#    def get_type(self, category):
#        res = 'Overig'
#        if re.search('dessert', category, flags=re.I) is not None:
#            res = 'Dessertwijn'
#        elif re.search('mousserend', category, flags=re.I) is not None:
#            res = 'Mousserend'
#        elif re.search('port', category, flags=re.I) is not None:
#            res = 'Port'
#        elif re.search('wijn', category, flags=re.I) is not None:
#            res = 'Wijn'
#        return res

    def scrape_product(self, elt):
        """ The function to scrape the product item """
        logger.debug('Get product from element\n{}'.format(elt))

        product = self.get_base_product()

        product_desc = {
            'price': 'price',
            'title': 'name',
            'code': 'id',
#            'category': 'category',
#            'type': 'category',
        }

        try:
            attr = json.loads(elt.attrs['data-tracking-impression'])
        except json.JSONDecodeError as e:
            logger.error(e)
            return

        for key, value in product_desc.items():
            product[key] = attr[value]

        # Skip unavailable products
        if len(elt.select('.not-available')) > 0:
            logger.warning('Skip product {}: not available'.format(
                product['title']))
            return

        product['url'] = '{}{}'.format(
            self.config['base_url'],
            elt.select('.link-overlay')[0]['href'])
        logger.info('** url: {}'.format(product['url']))

        prices = elt.select('.price')
        if prices and len(prices) > 1:
            product['price'] = prices[:-1][0].get_text()
        logger.info('** price: {}'.format(product['price']))

        try:
            product['price'] = float(product['price'])
        except Exception as e:
            logger.error(e)
            pass

#        product['color'] = self.get_color(product['category'])
#        product['winetype'] = self.get_type(product['category'])
#        product['title'] = self.get_title(product['title'])
        product['volume'] = self.get_volume(product['url'])
        product['quantity'] = self.get_quantity(product['url'])

        self.config['callback'](product)


def init(config):
    plugin = Gall()
    plugin.set_config(config)

    logger.info('[{}] Plugin initialized'.format(__name__))
    plugin.scrape_vendor(config, plugin.scrape_product)
