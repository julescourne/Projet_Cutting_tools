from sources.model.Rugosite import Rugosite
from sources.model.Piece import Piece
from sources.model import session


class RugositeController:
    """Classe qui gère l'ajout d'un objet rugosité dans la base de données"""

    def __init__(self):
        """Constructeur de la classe rugositecontroller"""
        self.rugosite = Rugosite()

    def create_rugosite(self, valeur, materiau_piece):
        """fonction qui ajoute un objet rugosité à la base de données

        Parameters
        ----------
        valeur : float
            La valeur de la rugosité
        materiau_piece : str
            Le matériau de la pièce en lien avec la rugosité

        """
        self.rugosite.valeur = valeur

        if materiau_piece != "":
            piece = session.query(Piece).filter_by(materiau=materiau_piece).all()
            if len(piece) != 0:
                self.rugosite.piece = piece[-1]

        else:
            self.rugosite.piece = None

        session.add(self.rugosite)
        session.commit()
        session.close()

