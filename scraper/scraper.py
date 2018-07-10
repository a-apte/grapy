import csv
#import sys
#import os
#import re
#import json
import logging
import logging.config
#import plugins
#import django
#from pprint import pformat
#from . import pluginbase


#
#__version__ = '0.0.1'
#
##
## Initialize logging
##
#if os.path.exists('logging.json'):
#    with open('logging.json', 'rt') as f:
#        config = json.load(f)
#        logging.config.dictConfig(config)
#else:
#    logging.basicConfig(level=logging.INFO)
#
#logger = logging.getLogger('grapy')


#
# Init complete
#
#logger.info('Initialized {} version {}'.format(__name__, __version__))


#python manage.py createsuperuser
#admin
#grapy@hugojanssen.nl
#ww: nl-grapy123





#
# Initialize django
# 
#logger.debug("Starting Django population script...")
#os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'grapy.settings')
#django.setup()

#
# only after django setup, we can import models
#
#from django.db import IntegrityError
#from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
#from wines import models
#


import abc

logger = logging.getLogger(__name__)


class Scraper(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def add(self, obj):
        """Add object to list"""
        return

    @abc.abstractmethod
    def persist(self):
        """Save object list to db"""
        return

    @abc.abstractmethod
    def scrape(self, obj):
        """Scrape"""
        return

    @staticmethod
    def to_csv(path, dict_data):
        if not (dict_data and len(dict_data) > 0):
            logger.error('No data to export')
            return
        try:
            with open(path, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=dict_data[0].keys())
                writer.writeheader()
    #            for data in dict_data:
                writer.writerows(dict_data)
        except IOError as e:
            logger.error('IO Error: {}'.format(e))
        except Exception as e:
            logger.error('Unknown error: {}'.format(e))
        return
