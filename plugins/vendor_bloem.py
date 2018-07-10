from . import pluginbase
#import re
import locale
import logging

logger = logging.getLogger(__name__)


class HenriBloem(pluginbase.PluginBase):

    # Set locale
    logger.debug('Set locale')
    locale.setlocale(locale.LC_ALL, 'nl')

    def get_volume(self, url):
        # TODO: do it nicely with regex
        volume = 0.75
        if '-0375' in url:
            volume = 0.375
        elif '-05' in url:
            volume = 0.5
        elif 'magnum' in url:
            volume = 1.5
        return volume

    def scrape_product(self, elt):
        """ The function to scrape the product item """
        logger.debug('Get product from element\n{}'.format(elt))

        product = self.get_base_product()

        code = elt['id']
        if code:
            product['code'] = code

        title = elt.a['href']
        if title:
            product['url'] = '{}{}'.format(self.config['base_url'], title.lower())

        # skip codes starting with 9995 (pakketten)
        if product['code'].startswith('9995'): # or len(product['code']) > 6:
            logger.warning('Product skipped: {}'.format(product['url']))
            return

        price = elt.select('.amount')
        if price and len(price) > 0:
            product['price'] = locale.atof(price[-1].text.strip())

        brand = elt.select('.brand')
        if brand and len(brand) > 0:
            product['title'] = brand[0].text.strip()

        cat = elt.select('.category')
        if cat and len(cat) > 0:
            product['title'] = '{} {}'.format(cat[0].text.strip(), product['title'])

        product['volume'] = self.get_volume(product['url'])


#['code', 'title', 'volume', 'quantity', 'price', 'url']

#        product['volume'] = self.get_volume(product['url'])
#        product['quantity'] = self.get_quantity(product['url'])

        self.config['callback'](product)


def init(config):
    plugin = HenriBloem()
    plugin.set_config(config)

    logger.info('[{}] Plugin initialized'.format(__name__))
    plugin.scrape_vendor(config, plugin.scrape_product)
