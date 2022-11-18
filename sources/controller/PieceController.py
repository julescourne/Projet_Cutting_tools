from sources.model.Piece import Piece
from sources.model.Experience import Experience
from sources.model.Rugosite import Rugosite
from sources.model import session


class PieceController:
    """Classe qui gère l'ajout d'une pièce dans la base de données"""

    def __init__(self):
        """Constructeur de la classe piececontroller"""
        self.piece = Piece()

    def create_piece(self, materiau, type_fabrication, fatigue, durete, contraintes_residuelles, temps, rugosite_valeur, nom_experience):
        """fonction qui ajoute une pièce à la base de données

        Parameters
        ----------
        materiau : str
            Le matériau de la pièce
        type_fabrication : str
            Le type de fabrication de la pièce
        fatigue : float
            La fatigue de la pièce
        durete : float
            La dureté de la pièce
        contraintes_residuelles : float
            Les contraintes résiduelles de la pièce
        temps : float
            Le temps associé à la pièce
        rugosite_valeur : float
            La valeur de l'objet rugosité en lien avec la pièce
        nom_experience : str
            Le nom de l'expérience en lien avec la pièce

        """
        self.piece.materiau = materiau
        self.piece.type_fabrication = type_fabrication
        self.piece.fatigue = fatigue
        self.piece.durete = durete
        self.piece.contraintes_residuelles = contraintes_residuelles
        self.piece.temps = temps

        if nom_experience != "":
            experience = session.query(Experience).filter_by(nom=nom_experience).all()
            if len(experience) != 0:
                self.piece.experience = experience[-1]

        else:
            self.piece.experience = None

        if rugosite_valeur is not None:
            rugosites = session.query(Rugosite).filter_by(valeur=rugosite_valeur).all()
            if len(rugosites) != 0:
                self.piece.rugosite = rugosites[-1]
        else:
            self.piece.rugosite = None

        session.add(self.piece)
        session.commit()
        session.close()

    def get_manufacturing_types(self):
        """Renvoie une liste des différents types de fabrication de pièce présent dans la base de données cutting"""

        type_fabrications = [type_fab[0] for type_fab in session.query(Piece.type_fabrication).distinct()]
        session.close()
        return type_fabrications

    def get_materials_types(self):
        """Renvoie une liste des différents types de matériaux des pièces présentes dans la base de données cutting"""

        type_materiaux = [type_mat[0] for type_mat in session.query(Piece.materiau).distinct()]
        session.close()
        return type_materiaux
