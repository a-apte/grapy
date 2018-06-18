#import csv
#import sys
import os
#import re
import json
import logging
import logging.config
#import plugins
import django
from pprint import pformat
from scraper import vendor, rating



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


#
# Initialize django
#
logger.debug("Starting Django population script...")
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'grapy.settings')
django.setup()

#
# only after django setup, we can import models
#
#from django.db import IntegrityError
#from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
#from wines import models
#



vd = vendor.VendorScraper()
vd.scrape()


rt = rating.RatingScraper()
rt.scrape()




# TODO: code cleanup raters
# TODO: validate ratings
# TODO: get color
# TODO: get winetype
# TODO: implement grandcruwijnen
# TODO: check unknowns
# TODO: more tests
# TODO: drf security / read only
# ----
# TODO: django on postgres
# ----
# TODO: chart price vs ratings (filter: color, min_rating_num, region, etc.)

