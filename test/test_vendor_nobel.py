import unittest
from plugins import vendor_nobel


class VendorNobelTestCase(unittest.TestCase):
    def setUp(self):
        self.plugin = vendor_nobel.Nobel()

    def test_volume(self):
        """Volumes are correctly translated"""
        volumes = {
            '0-75-l': 0.75,
            '0-375-l': 0.375,
            '1-50-l': 1.5,
            '0500-liter': 0.5,
            'not-a-volume': 0.75,
            '': 0.75,
        }

        for k, v in volumes.items():
            self.assertEqual(self.plugin.get_volume(k), v)

#    def test_country(self):
#        """Countries are correctly translated"""
#        countries = {
#            'nieuw-zeeland-2': 'nieuw-zeeland',
#            'verenigde-staten': 'verenigde staten',
#            'nederland-2': 'nederland',
#            'zuid-afrika': 'zuid-afrika',
#            'chili': 'chili',
#            'not-a-country': 'not-a-country',
#            '': '',
#        }
#
#        for k, v in countries.items():
#            self.assertEqual(self.plugin.get_country(k), v)

    def test_title(self):
        """Titles are correctly translated"""
        titles = {
            'Bepin de Eto Prosecco Spumante Magnum': 'Bepin de Eto Prosecco Spumante',
            'Tip! Neropasso Rosso IGT Veneto': 'Neropasso Rosso IGT Veneto',
            'Zenato Ripassa Veneto 0.375': 'Zenato Ripassa Veneto',
            'Zenato Ripassa Veneto': 'Zenato Ripassa Veneto',
            '': '',
        }

        for k, v in titles.items():
            self.assertEqual(self.plugin.get_title(k), v)
