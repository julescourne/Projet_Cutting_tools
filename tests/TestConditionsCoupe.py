import unittest
from sources.model.ConditionsCoupe import ConditionsCoupe
from sources.model.EffortCoupe import EffortCoupe
from sources.model.Temperature import Temperature
from sources.model.Experience import Experience
from sources.model.Outil import Outil
from sources.model.Piece import Piece
from sources.model.Rugosite import Rugosite


class TestConditionsCoupe(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    @classmethod
    def setUpClass(cls):
        pass

    def test_init_no_argument(self):
        """test init sans argument"""
        cond_coupe = ConditionsCoupe()
        self.assertEqual(cond_coupe.id, None)
        self.assertEqual(cond_coupe.type_lubrifiant, None)
        self.assertEqual(cond_coupe.vitesse_coupe, None)
        self.assertEqual(cond_coupe.vitesse_avance, None)
        self.assertEqual(cond_coupe.profondeur_passe, None)
        self.assertEqual(cond_coupe.effort_coupe, None)
        self.assertEqual(cond_coupe.temperature, None)
        self.assertEqual(cond_coupe.experience, None)

    def test_init_with_one_argument(self):
        """test init"""
        cond_coupe = ConditionsCoupe("type lubr", 4.5, 3.3, 5.6, 1.0, None, None, None)
        self.assertEqual(cond_coupe.id, None)
        self.assertEqual(cond_coupe.type_lubrifiant, "type lubr")
        self.assertEqual(cond_coupe.vitesse_coupe, 4.5)
        self.assertEqual(cond_coupe.vitesse_avance, 3.3)
        self.assertEqual(cond_coupe.profondeur_passe, 5.6)
        self.assertEqual(cond_coupe.temps, 1.0)
        self.assertEqual(cond_coupe.effort_coupe, None)
        self.assertEqual(cond_coupe.temperature, None)
        self.assertEqual(cond_coupe.experience, None)
