import unittest
from plugins import vendor_wijnvoordeel


class VendorWijnvoordeelTestCase(unittest.TestCase):
    def setUp(self):
        self.plugin = vendor_wijnvoordeel.WijnVoordeel()

    def test_title(self):
        """ Titles are correctly formatted """
        titles = {
            'Familie Pos Collection Merlot (1 fles) 2017': 'Familie Pos Collection Merlot 2017',
            'Familie Pos Collection Merlot (3 flessen) 2017': 'Familie Pos Collection Merlot 2017',
            'Familie Pos Collection Sparkling Wine Brut (3 flessen)': 'Familie Pos Collection Sparkling Wine Brut',
            'not-a-volume': 'not-a-volume',
            '': '',
        }

        for k, v in titles.items():
            self.assertEqual(self.plugin.get_title(k), v)

    def test_quantity(self):
        """ Quantity is correctly obtained from title """
        titles = {
            'Familie Pos Collection Merlot (1 fles) 2017': 1,
            'Familie Pos Collection Merlot (3 flessen) 2017': 3,
            'Familie Pos Collection Sparkling Wine Brut (3 flessen)': 3,
            'not-a-volume': 1,
            '': 1,
        }

        for k, v in titles.items():
            self.assertEqual(self.plugin.get_quantity(k), v)

#        Familie Pos Collection Merlot (1 fles) 2017
#        Familie Pos Collection Merlot (3 flessen) 2017
#        Familie Pos Collection Merlot (6 flessen) 2017

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
#Zuid-Afrika Stellenbosch
#Spanje Penedes
#unknown
#Italië Ligurië
#Ooostenrijk
#Frankrijk Nuits-Saint-Georges
#Italiè
#Chili Maule Valley
#
#        for k, v in countries.items():
#            self.assertEqual(self.plugin.get_country(k), v)
#
#    def test_title(self):
#        """Titles are correctly translated"""
#        titles = {
#            'Bepin de Eto Prosecco Spumante Magnum': 'Bepin de Eto Prosecco Spumante',
#            'Tip! Neropasso Rosso IGT Veneto': 'Neropasso Rosso IGT Veneto',
#            'Zenato Ripassa Veneto 0.375': 'Zenato Ripassa Veneto',
#            'Zenato Ripassa Veneto': 'Zenato Ripassa Veneto',
#            '': '',
#        }
#
#        for k, v in titles.items():
#            self.assertEqual(self.plugin.get_title(k), v)
