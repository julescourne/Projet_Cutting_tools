from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, Float, ForeignKey
from sources.model.__init__ import Base


class Rugosite(Base):
    """Classe du modèle représentant la rugosité"""
    __tablename__ = 'Rugosite'

    id = Column(Integer, primary_key=True)
    valeur = Column(Float)
    id_piece = Column(Integer, ForeignKey('Piece.id'))
    piece = relationship("Piece", back_populates="rugosite", cascade="all, delete")

    def __init__(self, *args):
        """Constructeur de la classe rugosité"""
        if not len(args) == 0:
            self.valeur = args[0]
            self.piece = args[1]

    def __eq__(self, other):
        """Fonction qui compare deux objets rugosité

        Parameters
        ----------
        other : Rugosite
            L'objet rugosité à comparer avec self

        Returns
        -------
        Boolean
            boolean qui indique si les deux objets sont égaux ou pas
        """
        try:
            if self.piece is None:
                return self.valeur == other.valeur and other.piece is None
            else:
                return self.valeur == other.valeur and self.piece.materiau == other.piece.materiau and self.piece.type_fabrication == other.piece.type_fabrication and self.piece.fatigue == other.piece.fatigue and self.piece.durete == other.piece.durete and self.piece.contraintes_residuelles == other.piece.contraintes_residuelles and self.piece.temps == other.piece.temps
        except AttributeError:
            return False

    @property
    def __valeur__(self):
        return self.valeur

    @__valeur__.setter
    def __valeur__(self, valeur):
        self.valeur = valeur

    @property
    def __piece__(self):
        return self.piece

    @__piece__.setter
    def __piece__(self, piece):
        self.piece = piece
