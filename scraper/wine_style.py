import logging
import logging.config
import plugins
from wines import models
from . import scraper
from pprint import pformat


logger = logging.getLogger(__name__)


class WineStyleScraper(scraper.Scraper):

    def add(self, res):
        """ """
        logger.info('Persisting style: {}'.format(pformat(res)))

        style = None
        try:
            style = models.WineStyle.objects.get(pk=res['id'])
        except models.WineStyle.DoesNotExist:
            logger.warning('No style for id {}'.format(res['id']))
            pass

        if style:
            try:
                style.body = res['body']
                style.acidity = res['acidity']
                style.color = res['color']
                style.save()

                logger.info('Update winestyle {}'.format(
                    style.name))
            except KeyError as e:
                logger.error('{}'.format(e))
                pass

    def scrape(self, wine_style_id=None):
        """ Scrape vivino wine ratings """
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

                if wine_style_id is not None:
                    try:
                        styles = [models.WineStyle.objects.get(pk=wine_style_id)]
                    except models.WineStyle.DoesNotExist:
                        logger.warning('No wine for id {}'.format(wine_style_id))
                        return
                else:
                    styles = models.WineStyle.objects.order_by('-modified')

                if rater.limit > 0:
                    styles = styles[:rater.limit]

                for style in styles:
                    logger.info('Scrape details for wine style {}'.format(style))

                    product = {
                        'id': style.id,
                        'url': style.url,
                    }
                    plugin.scrape_wine_style(product)

            except ModuleNotFoundError as e:
                logger.error(e)
            except Exception as e:
                logger.error(e)
