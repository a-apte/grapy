import unittest
from plugins import vendor_grandcru


class VendorGrandCruTestCase(unittest.TestCase):
    def setUp(self):
        self.plugin = vendor_grandcru.GrandCru()

    def test_volume(self):
        """Volumes are correctly obtained from url"""
        urls = {
            '2015-6-mura-giba-bianco-docg-0-375-ltr': 0.375,
            '2016-paul-mas-chardonnay-0-25-ltr': 0.25,
            '2012-enate-cabernet-sauvignon-merlot-0-5-ltr': 0.5,
            'cava-pere-ventura-brut-nature-tresor-0-2-ltr': 0.2,
            '2015-almaviva-roth-schild-puente-alto-imperiale-6-liter': 6.0,
            '2000-dom-perignon-champagne-brut-rose-in-golden-bottle-methusalem': 6.0,
            '2015-emilio-moro-dubbele-magnum': 3,
            '2011-pintia-magnum': 1.5,
            '2014-aalto-5-liter': 5,
            '2013-pintia-magnum-jeroboam-3-liter': 3,
            '1990-chateau-d-yquem-0-375ltr': 0.375,
            'not-a-volume': 0.75,
            '': 0.75,
        }

        for k, v in urls.items():
            self.assertEqual(self.plugin.get_volume(k), v)
