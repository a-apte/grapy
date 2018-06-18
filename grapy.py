import csv
import sys
import os
import re
import json
import logging
import logging.config
import plugins
import django
from pprint import pformat



__version__ = '0.0.1'

#
# Initialize logging
#
if os.path.exists('logging.json'):
    with open('logging.json', 'rt') as f:
        config = json.load(f)
        logging.config.dictConfig(config)
else:
    logging.basicConfig(level=logging.INFO)

logger = logging.getLogger('grapy')


#
# Init complete
#
logger.info('Initialized {} version {}'.format(__name__, __version__))


#python manage.py createsuperuser
#admin
#grapy@hugojanssen.nl
#ww: nl-grapy123


def to_csv(path, dict_data):
    if not (dict_data and len(dict_data) > 0):
        logger.error('No data to export')
        return
    try:
        with open(path, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=dict_data[0].keys())
            writer.writeheader()
#            for data in dict_data:
            writer.writerows(dict_data)
    except IOError as e:
        logger.error('IO Error: {}'.format(e))
    except Exception as e:
        logger.error('Unknown error: {}'.format(e))
    return


#
# Initialize django
# 
logger.debug("Starting Django population script...")
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'grapy.settings')
django.setup()

#
# only after django setup, we can import models
#
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from wines import models
#

product_list = []

#
# Wines
#
def save_products():

    logger.info('Persisting {} products as test: {}'.format(len(product_list)))

    # the wines
#    models.Wine.objects.bulk_create(wine_list)
    # add product to Django
    # bulk_create won't work, since it doesn't check primary keys

    for product in product_list:

        vendor = models.Vendor.objects.get(pk=product['vendor_id'])

        logger.info('[{}] Add product:\n{}'.format(
            vendor.name,
            pformat(product)))


        wine, created = models.Wine.objects.get_or_create(
            name=product['title'],
        )
        logger.info('[{}] {} wine: {}'.format(
            vendor.name,
            'Created' if created else 'Updated',
            wine.name))

        try:
            vendorwine, created = models.VendorWine.objects.get_or_create(
                vendor=vendor,
                wine=wine,
                vendor_code=product['code'],
                volume=product['volume'],
                quantity=product['quantity'],
                price=product['price'],
                url=product['url']
            )
            logger.info('[{}] {} vendorwine: {}'.format(
                vendor.name,
                'Created' if created else 'Updated',
                wine.name))
        except KeyError as e:
            logger.error('KeyError creating {}: {}, see {}'.format(
                product['title'],
                e,
                product['url']))
        except Exception as e:
            logger.error('Error creating {}: {}, see {}'.format(
                product['title'],
                e,
                product['url']))


def is_valid_product(vendor, product):
    """ Validates a product """
    valid = True

    logger.info('Stopwords: {}'.format(vendor.stopwords))
    logger.info('[{}] Validating product {}'.format(
        vendor.name,
        product['title']))

    if vendor.stopwords != '':
        regex = re.compile(vendor.stopwords, re.I)
        match = re.search(regex, product['title'])

        if match:
            valid = False
            logger.warning('[{}] Skipped: product matches stopword {}'.format(
                vendor.name,
                vendor.stopwords))

    # TODO: check if all mandatory fields are provided

    if product['code'] is None or product['code'] == 'unknown':
        valid = False
    return valid


def add_product(product):
    # validate product

    # valid vendor id
    try:
        vendor = models.Vendor.objects.get(pk=product['vendor_id'])
    except models.Vendor.DoesNotExist as e:
        logger.warning('Unable to add product: {} {}'.format(
            e,
            product['vendor_id']))
        return
    except Exception as e:
        logger.warning('Unable to add product: {} {}'.format(
            e,
            product['vendor_id']))
        return

    if is_valid_product(vendor, product):
        product_list.append(product)
    else:
        logger.warning('[{}] Skipped invalid product: {}'.format(
            vendor.name,
            product['title']))


def scrape_vendors(as_test=False):
    logger.debug(plugins.vendor_plugins)

    for vendor in models.Vendor.active.all():
        print('active vendor {}'.format(vendor))
        print('active vendor {}'.format(vendor.plugin))

        logger.info('[{}] Loading config...'.format(
            vendor.name))

        try:
            module = plugins.vendor_plugins[vendor.plugin]
        except ModuleNotFoundError as e:
            logger.error(e)

        if module:
            config = {
                'vendor_id': vendor.id,
                'base_url': vendor.url,
                'page': vendor.page,
                'max_pages': vendor.max_pages,
                'product': vendor.product,
                'callback': add_product
            }
            logger.info('[{}] Starting plugin {}...'.format(
                vendor.name,
                module))
            module.init(config)

    to_csv('products.csv', product_list)

    # scraping done, persist list
    if not as_test:
        save_products()
    else:
        # save to file?
        logger.info('Testrun; not saving list')


# kick-off the scraping
#scrape_vendors()


#
# Ratings
#

rating_list = []


def get_country(name):
    # TODO: ignore ' ' and '-' and digits and upper/lower
    country = models.Country.objects.filter(
        name__iexact=name
    ).first()
    logger.info('Country {}'.format(country))
    if country is None:
        logger.warning('Unknown country: {}'.format(name))
    return country



def is_valid_rating(rating):
    """ Validates a rating """
    valid = True

#    logger.info('[{}] Validating rating for {}'.format(
#        rater.name,
#        product['title']))

    return valid


def add_rating(rating):
    logger.info('[{}] Add rating:\n{}'.format('', pformat(rating)))

    # TODO: add to Django repo
#    country=
#    print(country)

    if is_valid_rating(rating):
        rating_list.append(rating)


def save_ratings():

    logger.info('Persisting ratings list: {}'.format(len(rating_list)))

    for rating in rating_list:

        wine = models.Wine.objects.get(pk=rating['product_id'])
        wine.country = get_country(rating['country'])
        wine.region = rating['region']
        wine.winery = rating['winery']
        wine.save()

        rater = models.Rater.objects.get(pk=rating['rater_id'])

        try:
            winerating, created = models.WineRating.objects.get_or_create(
                wine=wine,
                rater=rater,
                rating=rating['rating'],
                num_ratings=rating['num_ratings'],
                url=rating['url'],
            )
            logger.info('Added rating {} for wine {}'.format(
                winerating.rating,
                wine.name))
        except KeyError as e:
            logger.error('KeyError creating {}: {}, see {}'.format(
                rating['title'],
                e,
                rating['url']))
        except Exception as e:
            logger.error('Error creating {}: {}, see {}'.format(
                rating['title'],
                e,
                rating['url']))
#    clear_ratings()

#    rating_list = []


#def clear_ratings():
#    rating_list = []



def scrape_ratings(as_test=False):
    logger.debug(plugins.rating_plugins)

    for rater in models.Rater.active.all():
        logger.info('[{}] Loading config...'.format(
            rater.name))

        try:
            module = plugins.rating_plugins[rater.plugin]

            config = {
                'rater_id': rater.id,
                'base_url': rater.url,
                'page': rater.page,
                'callback': add_rating
            }
            plugin = module.init(config)

            # TODO: order should take current rater into account only
            wines = models.Wine.objects.all().order_by('ratings__modified')

            if rater.limit > 0:
                wines = wines[:rater.limit]

            for wine in wines:
                logger.info('Scrape rating for {}'.format(wine))
                plugin.build_uri(wine.id, wine.name)

        except ModuleNotFoundError as e:
            logger.error(e)
        except Exception as e:
            logger.error(e)

    # scraping done, persist list
    if not as_test:
        save_ratings()
        to_csv('ratings.csv', rating_list)
    else:
        # save to file?
        to_csv('ratings.csv', rating_list)
        logger.info('Testrun; not saving list')
    # scraping done, persist list


scrape_ratings(False)


# TODO: code cleanup raters
# TODO: validate ratings
# TODO: get color
# TODO: get winetype
# TODO: implement grandcruwijnen
# TODO: check unknowns
# TODO: more tests
# TODO: test function that prints the properties / saves to csv, not to db
# TODO: to class vendor/rating scaper -- list as class property
# TODO: scrape single wine rating only
# TODO: drf security / read only
# ----
# TODO: django on postgres
# ----
# TODO: chart price vs ratings (filter: color, min_rating_num, region, etc.)

