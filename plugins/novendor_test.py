import logging
logger = logging.getLogger(__name__)

config = {
    "name": "testvendor",
    "version": "0.0.1",
    "base_url": "http://localhost:8080",
    "page": "/page/{}/",
    "product": ".product",
    "callback": "scrape_product",
}


def scrape_product(elt):

    logger.info('scrape_product from {}'.format(elt))

    print('***')
    print(elt)

    product = {
        'title': 'testproduct'
    }

    print(product)
    return product
