from . import pluginbase
import re
import locale
import logging

logger = logging.getLogger(__name__)


class WijnVoordeel(pluginbase.PluginBase):

    # Set locale
    logger.debug('Set locale')
    locale.setlocale(locale.LC_ALL, 'nl')

    def get_quantity(self, title):
        res = 1
        expr = re.compile(r'\((\d)+ fles', re.I)
        match = re.search(expr, title)
        if match:
            try:
                res = int(float(match.group(1)))
            except Exception as e:
                logger.error('Error getting quantity from title {}: {}, see {}'.format(
                    title,
                    e,
                    match.group(1)))
        return res

    def scrape_product(self, elt):
        """ The function to scrape the product item """
        logger.debug('scrape_product from \n{}'.format(elt))

        product = self.get_base_product()

        # TODO: volume??
        title = elt.select('.produkt_name')
        if title and len(title) > 0:
            product['url'] = title[0]['href']
            product['title'] = title[0].get_text().rstrip().lstrip()
            code = re.search(r'::(\d+).html', product['url'])
            if code:
                product['code'] = code.group(1)

        price = elt.select('.price')
        if price and len(price) > 0:
            try:
                product['price'] = float(price[0].meta['content'])
            except TypeError:
                product['price'] = locale.atof(price[0].text[2:].strip())
            except Exception as e:
                logger.error(e)

        product['quantity'] = self.get_quantity(product['title'])

        self.config['callback'](product)


def init(config):
    plugin = WijnVoordeel()
    plugin.set_config(config)

    logger.info('[{}] Plugin initialized'.format(__name__))
    plugin.scrape_vendor(config, plugin.scrape_product)
