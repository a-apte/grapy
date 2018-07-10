from . import pluginbase
import re
import locale
import logging

logger = logging.getLogger(__name__)


class Nobel(pluginbase.PluginBase):

    # Set locale
    logger.debug('Set locale')
    locale.setlocale(locale.LC_ALL, 'nl')

    def get_volume(self, volume):
        if volume == '0-75-l':
            return 0.75
        elif volume == '0-375-l':
            return 0.375
        elif volume == '1-50-l':
            return 1.5
        elif volume == '0500-liter':
            return 0.5
        else:
            return 0.75

    def scrape_product(self, elt):
        """ The function to scrape the product item """
        logger.debug('Get product from element\n{}'.format(elt))

        product = self.get_base_product()

        product_desc = {
            'winetype': 'pa_wijntype',
            'color': 'pa_color',
#            'country': 'pa_herkomst',
#            'region': 'pa_streek',
#            'winery': 'pa_wijnhuis',
#            'grapes': 'pa_druivenras',
#            'vintage': 'pa_oogstjaar',  # vreemde waarden: 666
#            'serving_temp': 'pa_serveertemperatuur',
            'volume': 'pa_inhoud',
#            'aroma': 'pa_smaaktype',
            'code': 'post',
        }

        for key, value in product_desc.items():
            product[key] = self.find_tag(
                elt.attrs['class'],
                re.compile('{}-([\w-]+)'.format(value)))

        url = elt.select('.product-meta-wrapper')
        if url and len(url) > 0:
            product['url'] = url[0].a['href']

        title = elt.select('.product-title')
        if title and len(title) > 0:
            product['title'] = title[0].get_text()

        price = elt.select('.amount')
        if price and len(price) > 0:
            # the last price
            product['price'] = locale.atof(price[-1].get_text()[2:])

        product['volume'] = self.get_volume(product['volume'])

        self.config['callback'](product)


def init(config):
    plugin = Nobel()
    plugin.set_config(config)

    logger.info('[{}] Plugin initialized'.format(__name__))
    plugin.scrape_vendor(config, plugin.scrape_product)
