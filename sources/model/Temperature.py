from sqlalchemy.orm import relationship
from sources.model.__init__ import Base
from sqlalchemy import Column, Integer, Float, ForeignKey


class Temperature(Base):
    """Classe du modèle représentant la température"""
    __tablename__ = 'Temperature'

    id = Column(Integer, primary_key=True)
    valeur = Column(Float)
    id_conditions_coupe = Column(Integer, ForeignKey('ConditionsCoupe.id'))
    conditions_coupe = relationship("ConditionsCoupe", back_populates="temperature", cascade="all, delete")

    def __init__(self, *args):
        """Constructeur de la classe température"""
        if not len(args) == 0:
            self.valeur = args[0]
            self.conditions_coupe = args[1]

    def __eq__(self, other):
        """Fonction qui compare deux objets température

        Parameters
        ----------
        other : Temperature
            L'objet température à comparer avec self

        Returns
        -------
        Boolean
            boolean qui indique si les deux objets sont égaux ou pas
        """
        try:
            if self.conditions_coupe is None:
                return self.valeur == other.valeur and other.conditions_coupe is None
            else:
                return self.valeur == other.valeur and self.conditions_coupe.type_lubrifiant == other.conditions_coupe.type_lubrifiant and self.conditions_coupe.vitesse_coupe == other.conditions_coupe.vitesse_coupe and self.conditions_coupe.vitesse_avance == other.conditions_coupe.vitesse_avance and self.conditions_coupe.profondeur_passe == other.conditions_coupe.profondeur_passe and self.conditions_coupe.temps == other.conditions_coupe.temps
        except AttributeError:
            return False

    @property
    def __valeur__(self):
        return self.valeur

    @__valeur__.setter
    def __valeur__(self, valeur):
        self.valeur = valeur

    @property
    def __conditions_coupe__(self):
        return self.conditions_coupe

    @__conditions_coupe__.setter
    def __conditions_coupe__(self, conditions_coupe):
        self.conditions_coupe = conditions_coupe
