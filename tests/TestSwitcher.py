import unittest
from sources.controller.Switcher import Switcher
from sources.model import session
from sources.model.Experience import Experience
from sources.model.Temperature import Temperature
from sources.model.EffortCoupe import EffortCoupe
from sources.model.ConditionsCoupe import ConditionsCoupe
from sources.model.Outil import Outil
from sources.model.Piece import Piece
from sources.model.Rugosite import Rugosite


class TestSwitcher(unittest.TestCase):

    def setUp(self):
        self.switcher = Switcher()

    def tearDown(self):
        pass

    @classmethod
    def setUpClass(cls):
        pass

    def test_vitesse_coupe(self):
        """test vitesse_coupe"""
        res = self.switcher.vitesse_coupe()
        experiences = session.query(Experience).all()
        experience = None
        if len(experiences) != 0:
            experience = experiences[-1]

        result = []
        if experience is not None:
            for i in range(len(experience.conditions_coupe)):
                result.append(experience.conditions_coupe[i].vitesse_coupe)
        self.assertEqual(res, result)
