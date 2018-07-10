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
