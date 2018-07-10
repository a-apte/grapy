from . import pluginbase
import re
import locale
import logging

logger = logging.getLogger(__name__)


class GrandCru(pluginbase.PluginBase):

    # Set locale
    logger.debug('Set locale')
    locale.setlocale(locale.LC_ALL, 'nl')

    def get_volume(self, url):
        # TODO: do it nicely with regex
        volume = 0.75
        if '1-50-ltr' in url:
            volume = 1.5
        elif '0-375-ltr' in url or '0-375ltr' in url:
            volume = 0.375
        elif '0-25-ltr' in url:
            volume = 0.25
        elif '0-2-ltr' in url:
            volume = 0.2
        elif '0-5-ltr' in url:
            volume = 0.5
        elif 'dubbele-magnum' in url or 'jeroboam' in url or '3-liter' in url:
            volume = 3
        elif 'magnum' in url:
            volume = 1.5
        elif '5-liter' in url:
            volume = 5
        elif '6-liter' in url or 'methusalem' in url:
            volume = 6
        return volume


#    def get_quantity(self, url):
#        # TODO: do it nicely with regex
#        quantity = 1
#        if '-2x' in url:
#            quantity = 2
#        if '-6x' in url:
#            quantity = 6
#        return quantity

    def scrape_product(self, elt):
        """ The function to scrape the product item """
        logger.debug('Get product from element\n{}'.format(elt))

#        product = {
#            'vendor_id': self.config['vendor_id'],
#            'quantity': 1,
#            'volume': 0.75,
#            'price': 0.00,
#            'title': '',
#            'code': -1,
#            'url': '',
#        }
        product = self.get_base_product()

        title = elt.select('.product-name')
        if title and len(title) > 0:
            product['title'] = title[0].text
            product['url'] = title[0].a['href']

        price = elt.select('.price')
        if price and len(price) > 0:
            product['price'] = locale.atof(price[0].text.strip()[2:])

        idx = elt.find('span', id=re.compile('product-price'))
        if idx and idx['id']:
            m = re.match('product-price-(\d+)', idx['id'])
            if m:
                product['code'] = int(float(m.group(1)))


#['code', 'title', 'volume', 'quantity', 'price', 'url']

# 2015 Almaviva Roth­schild Puente Alto Imperiale 6 liter
#https://www.grandcruwijnen.nl/alle-wijnen/2015-almaviva-roth-schild-puente-alto-imperiale-6-liter

# 2000 Dom Pérignon Champagne Brut Rosé in Golden Bottle Methusalem
#https://www.grandcruwijnen.nl/alle-wijnen/2000-dom-perignon-champagne-brut-rose-in-golden-bottle-methusalem

#        product['title'] = self.get_title(product['title'])
        product['volume'] = self.get_volume(product['url'])
#        product['quantity'] = self.get_quantity(product['url'])

        self.config['callback'](product)


def init(config):
    plugin = GrandCru()
    plugin.set_config(config)

    logger.info('[{}] Plugin initialized'.format(__name__))
    plugin.scrape_vendor(config, plugin.scrape_product)
