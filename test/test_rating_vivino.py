import unittest
import urllib
from plugins import rating_vivino


class RaterVivinoTestCase(unittest.TestCase):
    config = {
        'rater_id': 99,
        'base_url': '',
        'page': '/search?{}',
        'callback': None
    }

    def setUp(self):
        self.plugin = rating_vivino.Vivino()
        self.plugin.set_config(self.config)

    def get_uri(self, arg):
        param = urllib.parse.urlencode({'q': arg})
        page = self.config['page'].format(param)
        return '{}{}'.format(self.config['base_url'], page)

    def test_build_uri_with_keywords(self):
        """URIs are correctly formatted from product keywords."""
        k = {
            'id': 1,
            'name': 'JC Chenet',
            'keywords': 'Jean Claude Chenet',
        }
        res, prod = self.plugin.build_uri(k)
        self.assertEqual(res, self.get_uri(k['keywords']))

    def test_build_uri(self):
        """URIs are correctly formatted from product name."""
        k = {
            'id': 1,
            'name': 'JC Chenet',
            'keywords': '',
        }
        res = self.plugin.build_uri(k)
        self.assertEqual(res[0], self.get_uri(k['name']))

    def test_clean_title(self):
        """Querystrings are correctly formatted from product name."""
        urls = {
            'Château Haut-Brion 1e Grand Cru Classé': 'Haut-Brion premier Grand Cru Classé',
            'Drappier Carte d\'Or Brut Jeroboam': 'Drappier Carte d\'Or Brut',
            'Rey Fernando de Castilla Palo Cortado Antique (0.5ltr.)': 'Rey Fernando Castilla Palo Cortado Antique',
            'Barao de Vilar 40 Years old Port (1 fles)': 'Barao Vilar 40 Years old Port',
            '2014 Emilio Moro 5 liter Methusalem': '2014 Emilio Moro',
            '2016 Gianfranco Fino Salento Negramaro Jo Jeroboam (3 liter)': '2016 Gianfranco Fino Salento Negramaro Jo',
            'Celler de Capçanes Pansal del Calas (0,5)': 'Capçanes Pansal Calas'
        }

        for k, v in urls.items():
            url = self.plugin.clean_title(k)
            self.assertEqual(url, v)

    def test_clean_volumes(self):
        """Volume indications are correctly cleaned from product name."""
        urls = {
            'Vin Santo del Chianti Classico 2009 37.5CL': 'Vin Santo del Chianti Classico 2009',
            'Catena Malbec 37,5cl': 'Catena Malbec',
            '2016 Paul Mas Chardonnay 0.25 ltr': '2016 Paul Mas Chardonnay',
            'Cava Pere Ventura Brut Nature Tresor 0.2 ltr': 'Cava Pere Ventura Brut Nature Tresor',
            'Rey Fernando de Castilla Palo Cortado Antique (0.5ltr.)': 'Rey Fernando de Castilla Palo Cortado Antique (.)',
            'Duval-Leroy Brut Premier Cru -Fleur de Champagne (0,375)': 'Duval-Leroy Brut Premier Cru -Fleur de Champagne ()',
            'Ürziger Würzgarten Riesling Kabinett 2016 75CL': 'Ürziger Würzgarten Riesling Kabinett 2016',
            'Conde Valdemar Rioja Crianza Magnum 150 cl 2012': 'Conde Valdemar Rioja Crianza Magnum  2012',
            'Barao de Vilar - Rosé Port (50cl)': 'Barao de Vilar - Rosé Port ()',
            '2014 Emilio Moro 5 liter Methusalem': '2014 Emilio Moro  Methusalem',
            'Barao de Vilar 40 Years old Port (1 fles)': 'Barao de Vilar 40 Years old Port (fles)',
            'Château Cos d\'Estournel 2e Grand Cru Classé': 'Château Cos d\'Estournel 2e Grand Cru Classé',
        }

        for k, v in urls.items():
            url = self.plugin.clean_volumes(k)
            self.assertEqual(url, v)

    def test_clean_regional_indications(self):
        """Regional indications are correctly cleaned from product name."""
        urls = {
            'Weingut Johannes B Riesling Junge Reben QW Württemberg 2016': 'Weingut Johannes B Riesling Junge Reben Württemberg 2016',
            '2015 Tenuta di Ghizzano Nambrot Igt Costa Toscana': '2015 Tenuta di Ghizzano Nambrot Costa Toscana',
            'Domaine 3 Momes Coteaux Varois en Provence AOP 2017': 'Domaine 3 Momes Coteaux Varois en Provence 2017',
            '\'Toos\' AOC Luberon Rose 75CL': '\'Toos\' Luberon Rose 75CL',
            'Tenimenti Migliara Cortona DOC 2012 75CL': 'Tenimenti Migliara Cortona 2012 75CL',
            'Pinot Noir doc \'Andrian\' 2016 75CL': 'Pinot Noir \'Andrian\' 2016 75CL',
            'Château David Médoc 37,5CL': 'Château David Médoc 37,5CL',
            'Castello di Brolio docg 2013 75CL': 'Castello di Brolio 2013 75CL',
            'Faustino Rivero - Rioja Reserva DOCa 2013': 'Faustino Rivero - Rioja Reserva 2013',
            'Mazzei Zisola Doppiozeta 2015 75CL': 'Mazzei Zisola Doppiozeta 2015 75CL',
            'Edoardo Miroglio Pinot noir dop \'EM\' 2015 75CL': 'Edoardo Miroglio Pinot noir \'EM\' 2015 75CL',
            'Paolo Scavino Barolo': 'Paolo Scavino Barolo',
        }

        for k, v in urls.items():
            url = self.plugin.clean_regional_indications(k)
            self.assertEqual(url, v)

    def test_clean_special_characters(self):
        """Special characters are correctly cleaned from product name."""
        urls = {
            '94Wines #8 Glorious': '94Wines 8 Glorious',
            'Il Falchetto Moscato d\'Asti (0,375)': 'Il Falchetto Moscato d\'Asti 0,375',
        }

        for k, v in urls.items():
            url = self.plugin.clean_special_characters(k)
            self.assertEqual(url, v)

    def test_clean_bottle_sizes(self):
        """Bottle sizes are correctly cleaned from product name."""
        urls = {
            'Chapin & Landais Le Grand Saumur Magnum': 'Chapin & Landais Le Grand Saumur',
            '2015 Paganos La Nieta Dubbele Magnum': '2015 Paganos La Nieta',
            '2015 Paganos La Nieta Jeroboam': '2015 Paganos La Nieta',
            '2014 Emilio Moro 5 liter Methusalem': '2014 Emilio Moro 5 liter',
        }

        for k, v in urls.items():
            url = self.plugin.clean_bottle_sizes(k)
            self.assertEqual(url, v)

    def test_clean_misc_annotations(self):
        """Special characters are correctly cleaned from product name."""
        urls = {
            'Château Cos d\'Estournel 2e Grand Cru Classé': ' Cos d\'Estournel Grand Cru Classé',
        }

        for k, v in urls.items():
            url = self.plugin.clean_misc_annotations(k)
            self.assertEqual(url, v)
