import unittest
from plugins import vendor_gall


class VendorGallTestCase(unittest.TestCase):
    def setUp(self):
        self.plugin = vendor_gall.Gall()

    def test_quantity(self):
        """Quantities are correctly obtained from url"""
        urls = {
            'https://www.gall.nl/shop/195278-drouhin-cote-de-beaune-rougeenrully-blanc14-2x75cl/': 2,
            'https://www.gall.nl/shop/308404-marques-riscal-rioja-reserva-magnum-2014-150cl/': 1,
            'https://www.gall.nl/shop/390194-catena-malbec-37-5cl/': 1,
            'not-a-volume': 1,
            '': 1,
        }

        for k, v in urls.items():
            self.assertEqual(self.plugin.get_quantity(k), v)

    def test_title(self):
        """Titles are correctly translated"""
        titles = {
            'Inycon Estate Pinot Grigio Sauvignon Blanc 75CL': 'Inycon Estate Pinot Grigio Sauvignon Blanc',
            'Kumala Chenin Chardonnay Bag in Box 2017 300CL': 'Kumala Chenin Chardonnay Bag in Box 2017',
            'Mainzer Domherr Franz von Metternich 100CL': 'Mainzer Domherr Franz von Metternich',
            'Casteñeda Sangria 150CL': 'Casteñeda Sangria',
            'Catena Malbec 37,5cl': 'Catena Malbec',
            'Domaine des Hauts Lieux 25CL': 'Domaine des Hauts Lieux',
            'Barberani Moscato Passito 2009 50CL': 'Barberani Moscato Passito 2009',
            'Faber Sparkling White Alcoholvrij 20CL': 'Faber Sparkling White Alcoholvrij',
            'Whispering Angel 2017 600CL': 'Whispering Angel 2017',
            'not-a-volume': 'not-a-volume',
            '': '',
        }

        for k, v in titles.items():
            self.assertEqual(self.plugin.get_title(k), v)

    def test_volume(self):
        """Volumes are correctly obtained from url"""
        urls = {
            'https://www.gall.nl/shop/195278-drouhin-cote-de-beaune-rougeenrully-blanc14-2x75cl/': 0.75,
            'https://www.gall.nl/shop/111988-la-roche-chablis-magnum-150cl/': 1.5,
            'https://www.gall.nl/shop/169447-la-roche-chablis-75cl/': 0.75,
            'https://www.gall.nl/shop/259667-planeta-la-segreta-rosso-375cl/': 0.375,
            'https://www.gall.nl/shop/280127-planeta-la-segreta-rosso-75cl/': 0.75,
            'https://www.gall.nl/shop/308072-conde-valdemar-rioja-crianza-magnum-150-cl-2012/': 1.5,
            'https://www.gall.nl/shop/308404-marques-riscal-rioja-reserva-magnum-2014-150cl/': 1.5,
            'https://www.gall.nl/shop/308447-chivite-coleccion-vendimia-tardia-2016-375cl/': 0.375,
            'https://www.gall.nl/shop/225428-mainzer-domherr-franz-von-metternich-100cl/': 1.00,
            'https://www.gall.nl/shop/390194-catena-malbec-37-5cl/': 0.375,
            'https://www.gall.nl/shop/159816-domaine-des-hauts-lieux-25cl/': 0.25,
            'https://www.gall.nl/shop/258164-barberani-moscato-passito-2009-50cl/': 0.5,
            'https://www.gall.nl/shop/400998-faber-sparkling-white-alcoholvrij-20cl/': 0.2,
            'https://www.gall.nl/shop/195367-whispering-angel-2017-600cl/': 6,
            'not-a-volume': 0.75,
            '': 0.75,
        }

        for k, v in urls.items():
            self.assertEqual(self.plugin.get_volume(k), v)
