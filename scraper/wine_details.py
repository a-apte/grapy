import logging
import logging.config
import plugins
from wines import models
from . import scraper
from pprint import pformat


logger = logging.getLogger(__name__)


class WineDetailsScraper(scraper.Scraper):

    def add(self, rating):
        """ """
        logger.info('Persisting product: {}'.format(pformat(rating)))

        wine = None
        try:
            wine = models.Wine.objects.get(pk=rating['id'])
        except models.Wine.DoesNotExist:
            logger.warning('No wine for id {}'.format(rating['id']))
            pass

        if wine:
            regional_style = None
            try:
                regional_style = rating['regionale stijlen']
            except KeyError:
                logger.warning('No style for wine {}'.format(rating['id']))
                pass

            if regional_style:
                regional_style = regional_style[0]
                style, created = models.WineStyle.objects.update_or_create(
                    name=regional_style['title'],
                    defaults={
                        'url': regional_style['url'],
                    },
                )
                style.wines.add(wine)
                logger.info('Added style {} for wine {}'.format(
                    style,
                    wine.name))

            grapes = None
            try:
                grapes = rating['druivenrassen']
            except KeyError:
                logger.warning('No grapes for wine {}'.format(rating['id']))
                pass

            if grapes:
                for g in grapes:
                    grape, created = models.Grape.objects.get_or_create(
                        name=g['title'],
                        defaults={
                            'url': g['url'],
                        },
                    )
                    grape.wines.add(wine)
                    logger.info('Added grape {} for wine {}'.format(
                        grape,
                        wine.name))

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
                        wines = [models.Wine.objects.get(pk=wine_id)]
                    except models.Wine.DoesNotExist:
                        logger.warning('No wine for id {}'.format(wine_id))
                        return
                else:
                    wines = models.Wine.objects.order_by('-modified')

                if rater.limit > 0:
                    wines = wines[:rater.limit]

                for wine in wines:
                    logger.info('Scrape rating for {}'.format(wine))

                    product = {
                        'id': wine.id,
                        'url': wine.url,
                    }
                    plugin.scrape_details(product)

            except ModuleNotFoundError as e:
                logger.error(e)
            except Exception as e:
                logger.error(e)
