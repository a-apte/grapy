import logging
import logging.config
import plugins
from wines import models
from . import scraper


logger = logging.getLogger(__name__)


class RatingScraper(scraper.Scraper):

    rating_list = []

    def get_country(self, name):
        # TODO: ignore ' ' and '-' and digits and upper/lower
        country = models.Country.objects.filter(
            name__iexact=name
        ).first()
        logger.info('Country {}'.format(country))
        if country is None:
            logger.warning('Unknown country: {}'.format(name))
        return country

    def persist(self):
        for rating in self.rating_list:
            wine = models.Wine.objects.get(pk=rating['product_id'])
            wine.country = self.get_country(rating['country'])
            wine.region = rating['region']
            wine.winery = rating['winery']
            wine.save()

            rater = models.Rater.objects.get(pk=rating['rater_id'])

            try:
                # Get or create the rating
                winerating, created = models.WineRating.objects.get_or_create(
                    wine=wine,
                    rater=rater
                )

                # Update rating details
                winerating.rating = rating['rating']
                winerating.num_ratings = rating['num_ratings']
                winerating.url = rating['url']
                winerating.save()

                logger.info('Added rating {} for wine {}'.format(
                    winerating.rating,
                    wine.name))
            except KeyError as e:
                logger.error('KeyError creating {}: {}, see {}'.format(
                    rating['product_id'],
                    e,
                    rating['url']))
            except Exception as e:
                logger.error('Error creating {}: {}, see {}'.format(
                    rating['product_id'],
                    e,
                    rating['url']))

        self.rating_list = []

    def is_valid(self, rating):
        """ Validates a product """
        valid = True

        logger.info('[{}] Validating rating {}'.format(
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
                rating['id']))

    def scrape(self, wine_id=None):
        """ Scrape ratings for wines, or for a specific wine, if specified """
        logger.debug(plugins.vendor_plugins)

        for rater in models.Rater.active.all():
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

                try:
                    wines = [models.Wine.objects.get(pk=wine_id)]
                except models.Wine.DoesNotExist:
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
            if not rater.is_test:
                self.persist()
            else:
                path = 'rating_{}.csv'.format(rater.name)
                scraper.to_csv(path, self.rating_list)
                logger.info('[{}] Test mode: products saved to file {}'.format(
                    rater.name,
                    path))
