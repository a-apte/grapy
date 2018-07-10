import unittest
from plugins import vendor_wijnvoordeel


class VendorWijnvoordeelTestCase(unittest.TestCase):
    def setUp(self):
        self.plugin = vendor_wijnvoordeel.WijnVoordeel()

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
