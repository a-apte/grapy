import os
import json
import logging
import logging.config
import django


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
logger.info('Initialized {} version {}'.format(__name__, __version__))


#
# Initialize django
#
logger.debug("Starting Django population script...")
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'grapy.settings')

django.setup()
logger.info('Django version {}'.format(django.__version__))
logger.info('Apps ready? {} '.format(django.apps.apps.ready))
logger.info('App name {} '.format(django.apps.apps.get_app_config('wines')))


# do not import earlier, since Django should load first
from scraper import vendor, wine, wine_details, wine_style

# vendors
vendor.VendorScraper().scrape()


# wines
import time
for i in range(4300, 4400):
    wine.WineScraper().scrape(i) # Amaurigue+Cotes+de+Provence+Rose
    time.sleep(0.3)

w = [3802,3726,3122,2876]
for i in w:
    wine.WineScraper().scrape(i) # Amaurigue+Cotes+de+Provence+Rose


wine.WineScraper().scrape(4310) # Amaurigue+Cotes+de+Provence+Rose
wine.WineScraper().scrape() # Amaurigue+Cotes+de+Provence+Rose


# ratings
#rating.RatingScraper().scrape(8139) # Amaurigue+Cotes+de+Provence+Rose
#rating.RatingScraper().scrape(9080) # 94Wines #1
for i in range(200, 500):
    wine_details.WineDetailsScraper().scrape(i) # 94Wines #2
    time.sleep(0.3)

wine_details.WineDetailsScraper().scrape(69) # 94Wines #2

for i in range(1, 100):
    wine_style.WineStyleScraper().scrape(i) # 94Wines #2

wine_style.WineStyleScraper().scrape(15) # 94Wines #2

#rating.RatingScraper().scrape()
