from sources.model.Experience import Experience
from sources.model.Outil import Outil
from sources.model.ConditionsCoupe import ConditionsCoupe
from sources.model.Piece import Piece
from sources.model import mydb


class ExperienceController:
    """Classe qui gère l'ajout d'un objet experience dans la base de données"""

    def __init__(self):
        """Constructeur de la classe experiencecontroller"""
        self.experience = Experience()

    def create_experience(self, nom):
        """fonction qui ajoute une expérience à la base de données

        Parameters
        ----------
        nom : str
            Le nom de l'expérience

        """
        self.experience.nom = nom

        mycursor = mydb.cursor()

        sql = """INSERT INTO experience (id, nom) VALUES (%s, %s)"""
        val = (None, self.experience.nom)
        mycursor.execute(sql, val)
