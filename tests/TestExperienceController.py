import unittest

from sources.controller.ExperienceController import ExperienceController
from sources.model.ConditionsCoupe import ConditionsCoupe
from sources.model.EffortCoupe import EffortCoupe
from sources.model.Experience import Experience
from sources.model.Outil import Outil
from sources.model.Piece import Piece
from sources.model.Rugosite import Rugosite
from sources.model.Temperature import Temperature
from sources.model import session, mydb


class TestExperienceController(unittest.TestCase):

    def setUp(self):
        self.exp_controller = ExperienceController()

    def tearDown(self):
        session.query(ConditionsCoupe).delete()
        session.query(EffortCoupe).delete()
        session.query(Experience).delete()
        session.query(Outil).delete()
        session.query(Piece).delete()
        session.query(Rugosite).delete()
        session.query(Temperature).delete()
        session.commit()

        self.nom = "exp1"
        self.list_outil = []
        self.list_type_lubrifiant_conditions_coupe = ["MQL"]
        self.list_materiau_piece = ["Inconel"]

    @classmethod
    def setUpClass(cls):
        cls.nom = "exp1"
        cls.list_outil = []
        cls.list_type_lubrifiant_conditions_coupe = ["MQL"]
        cls.list_materiau_piece = ["Inconel"]

    def test_create_experience_only_experience(self):
        """test sans outil, conditions coupe et piece"""
        self.exp_controller.create_experience(self.nom)
        mydb.commit()
        mycursor = mydb.cursor()
        mycursor.execute("""select * from experience order by id desc limit 1""")
        experience = mycursor.fetchall()

        experience2 = Experience("exp1", [], [], [])
        self.assertEqual(experience[0][1].__eq__(experience2.nom), True)
