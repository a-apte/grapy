import unittest
from plugins import vendor_bloem


class VendorBloemTestCase(unittest.TestCase):
    def setUp(self):
        self.plugin = vendor_bloem.HenriBloem()

    def test_volume(self):
        """Volumes are correctly translated"""
        volumes = {
            '174151_drappier_carte-dor-brut-magnum.html': 1.5,
            '174282_il-falchetto_moscato-dasti-0375.html': 0.375,
            '173647_bodegas-aragonesas_coto-de-hayas-moscatel-05.html': 0.5,
            'not-a-volume': 0.75,
            '': 0.75,
        }

        for k, v in volumes.items():
            self.assertEqual(self.plugin.get_volume(k), v)
