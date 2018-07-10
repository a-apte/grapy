import logging
import logging.config
import plugins
from wines import models
from . import scraper


logger = logging.getLogger(__name__)


class WineScraper(scraper.Scraper):

    rating_list = []

    def get_country(self, name):
        country = models.Country.objects.filter(
            name__iexact=name
        ).first()
        logger.info('Country {}'.format(country))
        if country is None:
            logger.warning('Unknown country: {}'.format(name))
        return country

    def persist(self):
        for rating in self.rating_list:

            logger.info('Persisting product: {}'.format(rating))

            wine, created = models.Wine.objects.update_or_create(
                url=rating['url'],
                defaults={
                    'name': rating['title'],
                    'country': self.get_country(rating['country']),
                    'region': rating['region'],
                    'winery': rating['winery'],
                },
            )

            models.VendorWine.objects.filter(id=rating['product_id']).update(wine=wine.id)

            rater = models.Rater.objects.get(pk=rating['rater_id'])

            winerating, created = models.WineRating.objects.update_or_create(
                wine=wine,
                rater=rater,
                defaults={
                    'rating': rating['rating'],
                    'num_ratings': rating['num_ratings'],
                    'url': rating['url'],
                },
            )

            logger.info('Added rating {} for wine {}'.format(
                winerating.rating,
                wine.name))

    def is_valid(self, rating):
        """ Validates a product """
        valid = True

        logger.info('[{}] Validating rating {}'.format(
            rating['rater_id'],
            rating['product_id']))

        if not rating['url']:
            valid = False
            logger.warning('[{}] Skipped: no url for vendorwine {}'.format(
                rating['rater_id'],
                rating['product_id']))

        return valid

    def add(self, rating):
        """ Add the rating to the list if valid """

        if self.is_valid(rating):
            self.rating_list.append(rating)
        else:
            logger.warning('[{}] Skipped invalid rating: {}'.format(
                rating['rater_id'],
                rating['product_id']))

    def scrape(self, wine_id=None):
        """ Scrape vivino wine ratings """
        logger.debug(plugins.vendor_plugins)

        for rater in models.Rater.active.all():
            self.rating_list = []

            logger.info('[{}] Loading config...'.format(
                rater.name))

            try:
                module = plugins.rating_plugins[rater.plugin]

                config = {
                    'rater_id': rater.id,
                    'base_url': rater.url,
                    'page': rater.page,
                    'callback': self.add
                }
                plugin = module.init(config)

                if wine_id is not None:
                    try:
                        wines = [models.VendorWine.objects.get(pk=wine_id)]
                    except models.VendorWine.DoesNotExist:
                        logger.warning('No wine for id {}'.format(wine_id))
                        return
                else:
                    wines = models.VendorWine.objects.filter(
                        wine=None).order_by('-modified')

                if rater.limit > 0:
                    wines = wines[:rater.limit]

                for wine in wines:
                    logger.info('Scrape rating for {}'.format(wine))

                    product = {
                        'id': wine.id,
                        'name': wine.title,
                        'keywords': wine.keywords,
                    }
                    plugin.search_rating(product)

                logger.info('Done scraping '.format())

            except ModuleNotFoundError as e:
                logger.error(e)
            except Exception as e:
                logger.error(e)

            # scraping done, persist list
            if not rater.is_test:
                self.persist()
            else:
                path = 'rating_{}.csv'.format(rater.name)
                scraper.to_csv(path, self.rating_list)
                logger.info('[{}] Test mode: products saved to file {}'.format(
                    rater.name,
                    path))
