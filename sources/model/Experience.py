from sqlalchemy import Column, Integer, VARCHAR
from sqlalchemy.orm import relationship
from sources.model.__init__ import Base


class Experience(Base):
    """Classe du modèle représentant une expérience"""
    __tablename__ = 'Experience'

    id = Column(Integer, primary_key=True)
    nom = Column(VARCHAR(100))
    conditions_coupe = relationship("ConditionsCoupe", back_populates="experience", cascade="all, delete")
    outil = relationship("Outil", back_populates="experience", cascade="all, delete")
    piece = relationship("Piece", back_populates="experience", cascade="all, delete")

    def __init__(self, *args):
        """Constructeur de la classe experience"""
        if not len(args) == 0:
            if len(args) == 1:
                self.nom = args[0]
            else:
                self.nom = args[0]
                self.conditions_coupe = args[1]
                self.outil = args[2]
                self.piece = args[3]

    def __eq__(self, other):
        """Fonction qui compare deux objets experience

        Parameters
        ----------
        other : Experience
            L'objet expérience à comparer avec self

        Returns
        -------
        Boolean
            boolean qui indique si les deux objets sont égaux ou pas
        """
        if len(self.outil) != len(other.outil):
            return False
        else:
            for i in range(len(self.outil)):
                if self.outil[i].nom != other.outil[i].nom or self.outil[i].materiau != other.outil[
                    i].materiau or self.outil[i].geometrie != other.outil[i].geometrie or self.outil[i].duree_de_vie != \
                        other.outil[i].duree_de_vie:
                    return False

        if len(self.conditions_coupe) != len(other.conditions_coupe):
            return False
        else:
            for i in range(len(self.conditions_coupe)):
                if self.conditions_coupe[i].type_lubrifiant != other.conditions_coupe[i].type_lubrifiant or self.conditions_coupe[i].vitesse_coupe != other.conditions_coupe[
                    i].vitesse_coupe or self.conditions_coupe[i].vitesse_avance != other.conditions_coupe[i].vitesse_avance or self.conditions_coupe[i].profondeur_passe != \
                        other.conditions_coupe[i].profondeur_passe or self.conditions_coupe[i].temps != other.conditions_coupe[i].temps:
                    return False

        if len(self.piece) != len(other.piece):
            return False
        else:
            for i in range(len(self.piece)):
                if self.piece[i].materiau != other.piece[i].materiau or self.piece[i].type_fabrication != other.piece[
                    i].type_fabrication or self.piece[i].fatigue != other.piece[i].fatigue or self.piece[i].durete != \
                        other.piece[i].durete or self.piece[i].contraintes_residuelles != other.piece[i].contraintes_residuelles or self.piece[i].temps != other.piece[i].temps:
                    return False

        return self.nom == other.nom

    @property
    def __nom__(self):
        return self.nom

    @__nom__.setter
    def __nom__(self, nom):
        self.nom = nom

    @property
    def __conditions_coupe__(self):
        return self.conditions_coupe

    @__conditions_coupe__.setter
    def __conditions_coupe__(self, conditions_coupe):
        self.conditions_coupe = conditions_coupe

    @property
    def __outil__(self):
        return self.outil

    @__outil__.setter
    def __outil__(self, outil):
        self.outil = outil

    @property
    def __piece__(self):
        return self.piece

    @__piece__.setter
    def __piece__(self, piece):
        self.piece = piece
