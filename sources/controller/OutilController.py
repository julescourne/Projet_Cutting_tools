from sources.model.Outil import Outil
from sources.model.Experience import Experience
from sources.model import session


class OutilController:
    """Classe qui gère l'ajout d'un objet outil dans la base de données"""

    def __init__(self):
        """Constructeur de la classe outilcontroller"""
        self.outil = Outil()

    def create_outil(self, nom, materiau, geometrie, duree_vie, temps, nom_experience):
        """fonction qui ajoute un outil à la base de données

        Parameters
        ----------
        nom : str
            Le nom de l'outil
        materiau : str
            Le matériau de l'outil
        geometrie : str
            La géométrie de l'outil
        duree_vie : float
            La durée de vie de l'outil
        temps : float
            Le temps associé à l'outil
        nom_experience : str
            Le nom de l'expérience en lien avec l'outil

        """
        self.outil.nom = nom
        self.outil.materiau = materiau
        self.outil.geometrie = geometrie
        self.outil.duree_de_vie = duree_vie
        self.outil.temps = temps

        if nom_experience != "":
            experience = session.query(Experience).filter_by(nom=nom_experience).all()
            if len(experience) != 0:
                self.outil.experience = experience[-1]

        else:
            self.outil.experience = None

        session.add(self.outil)
        session.commit()
        session.close()
