import unittest
from sources.controller.DeleteExperience import DeleteExperience
from sources.model import session
from sources.model.Experience import Experience
from sources.model.EffortCoupe import EffortCoupe
from sources.model.ConditionsCoupe import ConditionsCoupe
from sources.model.Outil import Outil
from sources.model.Piece import Piece
from sources.model.Temperature import Temperature
from sources.model.Rugosite import Rugosite


class TestDeleteExperience(unittest.TestCase):
    def setUp(self):
        self.delete_experience_object = DeleteExperience()

    def tearDown(self):
        pass

    @classmethod
    def setUpClass(cls):
        pass

